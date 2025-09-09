# 🚀 AzureBrains Fetch Proxy

[![Azure Container Instances](https://img.shields.io/badge/Azure-Container%20Instances-blue)](https://azure.microsoft.com/en-us/services/container-instances/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![AzureBrains](https://img.shields.io/badge/AzureBrains-proxy.azurebrains.com-orange)](https://proxy.azurebrains.com)

A production-ready HTTP fetch proxy with **Spanish geolocation simulation**, built with Python's BaseHTTPServer and deployed at **proxy.azurebrains.com**.

**Perfect for ChatGPT**: This proxy enables AI assistants to access and analyze web content by simulating Spanish geolocation and providing realistic headers to bypass common bot restrictions.

🇪🇸 **Spanish Geolocation Simulation**: Automatically adds Spanish headers including realistic ISP information, regional data, and client location to appear as if requests are coming from Spain.

> ⚠️ **Use Responsibly**: Do not use this to bypass paywalls, authentication, or legal restrictions. Respect robots.txt and target websites' Terms of Service.

## ✨ Features

### 🔐 Security First
- **API Key Authentication**: Dual method support (header + query parameter)
- **Advanced SSRF Protection**: Blocks private networks, cloud metadata endpoints
- **Rate Limiting**: 100 requests/minute, 2000 requests/hour per IP
- **Response Size Limits**: Configurable maximum response size (15MB default)

### 🇪🇸 Spanish Geolocation Features
- **Realistic Spanish ISPs**: Rotates between Telefónica, Orange, Vodafone, Euskaltel, Jazztel
- **Regional Simulation**: Madrid, Barcelona, Valencia, Sevilla, Bilbao locations
- **Spanish Headers**: Adds X-Spanish-Region, X-Client-Location, X-ISP headers
- **Anti-Bot Evasion**: Realistic User-Agent and Accept-Language headers

### ⚡ Performance & Reliability  
- **HTTP/2 Support**: Modern protocol support with optimized connections
- **Intelligent Retries**: Automatic retry on transient failures with backoff
- **Content Processing**: Proper encoding handling and content decompression
- **Connection Reuse**: Efficient session management for better performance

### 📊 Monitoring & Observability
- **Health Checks**: `/health` endpoint for container monitoring
- **Request Logging**: Detailed logging with timing and response information
- **Error Tracking**: Comprehensive error handling and reporting
- **Security Auditing**: API key validation and rate limiting logs

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
   python secure_proxy.py
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

#### 🌐 Custom Domain Setup (proxy.azurebrains.com)

After deployment, you can configure the custom domain:

1. **Basic DNS Setup** (HTTP only):
   ```bash
   # Add CNAME record in your DNS:
   # proxy.azurebrains.com -> your-container-url.westeurope.azurecontainer.io
   ```

2. **Azure Front Door** (HTTPS + CDN - Recommended):
   See detailed instructions in `CUSTOM_DOMAIN_SETUP.md`

3. **Test your custom domain**:
   ```bash
   curl "https://proxy.azurebrains.com/healthz"
   ```

> 📋 **Complete Guide**: Check `CUSTOM_DOMAIN_SETUP.md` for detailed custom domain configuration.

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
# Production security settings for proxy.azurebrains.com
export API_KEY="super-secure-key-123"
export ALLOWED_HOSTS="api.github.com,docs.python.org,httpbin.org"
export MAX_REQUESTS_PER_MINUTE=50
export MAX_RESPONSE_SIZE_MB=10
export CUSTOM_DOMAIN="proxy.azurebrains.com"
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
https://proxy.azurebrains.com/fetch?url=TARGET_URL&api_key=YOUR_API_KEY
```

### Example ChatGPT Prompts

**Analyze GitHub Repository:**
```
Analyze this GitHub repository and summarize its key information:
https://proxy.azurebrains.com/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY
```

**Research Documentation:**
```
Read this Python documentation and explain the main concepts:
https://proxy.azurebrains.com/fetch?url=https://docs.python.org/3/library/asyncio.html&api_key=YOUR_API_KEY
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
├── CUSTOM_DOMAIN_SETUP.md  # Custom domain configuration guide
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
- Visit [proxy.azurebrains.com](https://proxy.azurebrains.com) for live service

---

**Made with ❤️ by AzureBrains - Powering the AI community**  
🌐 **Live at**: [proxy.azurebrains.com](https://proxy.azurebrains.com)
