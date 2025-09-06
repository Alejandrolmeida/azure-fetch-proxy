# 🚀 Azure FastAPI Fetch Proxy

[![Azure Container Instances](https://img.shields.io/badge/Azure-Container%20Instances-blue)](https://azure.microsoft.com/en-us/services/container-instances/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A production-ready HTTP fetch proxy built with FastAPI, optimized for ChatGPT integration and deployed on Azure Container Instances.

**Perfect for ChatGPT**: This proxy enables AI assistants to access and analyze web content by bypassing common bot restrictions and providing a secure, rate-limited endpoint.

> ⚠️ **Use Responsibly**: Do not use this to bypass paywalls, authentication, or legal restrictions. Respect robots.txt and target websites' Terms of Service.

## ✨ Features

### 🔐 Security First
- **API Key Authentication**: Dual method support (header + query parameter)
- **Advanced SSRF Protection**: Blocks private networks, cloud metadata endpoints
- **Rate Limiting**: 100 requests/minute, 2000 requests/hour per IP
- **Response Size Limits**: Configurable maximum response size (15MB default)

### ⚡ Performance & Reliability
- **Smart Caching**: In-memory LRU cache with 120-second TTL
- **Connection Pooling**: HTTP/2 support with optimized connections
- **Intelligent Retries**: Automatic retry on transient failures
- **Content Decompression**: Ensures proper display in browsers

### 📊 Monitoring & Observability
- **Health Checks**: `/healthz` endpoint for monitoring
- **Prometheus Metrics**: `/metrics` endpoint with detailed statistics
- **Structured Logging**: Request IDs, timing, response sizes
- **Security Info**: `/security-info` endpoint for configuration verification

## 🚀 Quick Start

### Local Development

1. **Clone and setup environment:**
   ```bash
   git clone https://github.com/alejandrolmeida/azure-fetch-proxy.git
   cd azure-fetch-proxy
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API key and settings
   export API_KEY="your-secure-api-key"
   ```

3. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Test the proxy:**
   ```bash
   curl "http://localhost:8000/fetch?url=https://httpbin.org/json&api_key=your-secure-api-key"
   ```

### 🐳 Docker Deployment

```bash
# Build the image
docker build -t azure-fetch-proxy .

# Run the container
docker run -p 8000:8000 -e API_KEY="your-secure-api-key" azure-fetch-proxy
```

### ☁️ Azure Container Instances Deployment

The included deployment script automates the entire Azure deployment process:

```bash
chmod +x deploy_container.sh
./deploy_container.sh
```

This script will:
1. Create an Azure Container Registry
2. Build and push the Docker image
3. Deploy to Azure Container Instances
4. Configure environment variables
5. Provide the public endpoint URL

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Required API key for authentication | None |
| `MAX_REQUESTS_PER_MINUTE` | Rate limit per IP per minute | 100 |
| `MAX_REQUESTS_PER_HOUR` | Rate limit per IP per hour | 2000 |
| `MAX_RESPONSE_SIZE_MB` | Maximum response size in MB | 15 |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | None (all allowed) |
| `BLOCKED_HOSTS` | Comma-separated blocked hostnames | None |

### Example Configuration

```bash
# Production security settings
export API_KEY="super-secure-key-123"
export ALLOWED_HOSTS="api.github.com,docs.python.org,httpbin.org"
export MAX_REQUESTS_PER_MINUTE=50
export MAX_RESPONSE_SIZE_MB=10
```

## 📚 API Reference

### Main Endpoint: `/fetch`

Supports GET, HEAD, and POST methods.

**Parameters:**
- `url` (required): Target URL to fetch
- `api_key` (required): Authentication key
- `method` (optional): HTTP method (GET, HEAD, POST)
- `timeout` (optional): Request timeout in seconds (1-60)
- `ua` (optional): User agent type (desktop, mobile)

**Example Requests:**
```bash
# Basic GET request
curl "http://localhost:8000/fetch?url=https://httpbin.org/json&api_key=your-key"

# POST request with data
curl -X POST "http://localhost:8000/fetch?url=https://httpbin.org/post&method=POST&api_key=your-key" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello World"}'

# Using header authentication
curl -H "x-api-key: your-key" \
     "http://localhost:8000/fetch?url=https://httpbin.org/get"
```

### Monitoring Endpoints

- `GET /healthz` - Health check (returns "ok")
- `GET /metrics` - Prometheus metrics
- `GET /security-info` - Current security configuration
- `GET /` - API documentation and examples

## 🤖 ChatGPT Integration

This proxy is specifically optimized for AI assistants like ChatGPT:

### Usage Format
```
https://your-container-url.westeurope.azurecontainer.io/fetch?url=TARGET_URL&api_key=YOUR_API_KEY
```

### Example ChatGPT Prompts

**Analyze GitHub Repository:**
```
Analyze this GitHub repository and summarize its key information:
https://your-container-url.westeurope.azurecontainer.io/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY
```

**Research Documentation:**
```
Read this Python documentation and explain the main concepts:
https://your-container-url.westeurope.azurecontainer.io/fetch?url=https://docs.python.org/3/library/asyncio.html&api_key=YOUR_API_KEY
```

## 🛡️ Security Features

### SSRF Protection
- Blocks private networks (RFC 1918)
- Prevents access to cloud metadata endpoints
- Validates IPv6 and IPv4 addresses
- DNS rebinding attack prevention

### Authentication & Authorization
- API key validation (header or query parameter)
- Host allowlist/blocklist support
- Per-IP rate limiting with sliding window
- Request size limitations

### Monitoring & Auditing
- All requests logged with unique IDs
- Failed authentication attempts tracked
- Rate limit violations recorded
- Response time and size metrics

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_ssrf.py -v      # SSRF protection tests
pytest tests/test_fetch.py -v     # Core functionality tests
```

## 📁 Project Structure

```
├── main.py                 # FastAPI application
├── Dockerfile             # Container configuration
├── deploy_container.sh     # Azure deployment script
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version specification
├── .env.example           # Environment variables template
├── tests/                 # Test suite
│   ├── test_fetch.py      # Core functionality tests
│   └── test_ssrf.py       # Security tests
└── requests.http          # API examples
```

## 🚀 Production Deployment

For production use, consider:

1. **Security Hardening:**
   - Use strong API keys with regular rotation
   - Implement host allowlists for known domains
   - Monitor failed authentication attempts

2. **Scaling:**
   - Use Azure Container Instances with auto-scaling
   - Implement load balancing for high availability
   - Monitor resource usage via `/metrics`

3. **Monitoring:**
   - Set up alerts for rate limit violations
   - Monitor response times and error rates
   - Track cache hit ratios for optimization

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For issues and questions:
- Open a GitHub issue
- Check the `/security-info` endpoint for configuration
- Review logs for detailed error information

---

**Made with ❤️ for the AI community**
