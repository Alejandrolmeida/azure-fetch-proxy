
# 🚀 Azure FastAPI Fetch Proxy - ChatGPT Enhanced

A comprehensive, production-ready **HTTP fetch proxy** built with **FastAPI** specifically optimized for **ChatGPT integration** and deployment on **Azure App Service (Linux)**.

**🎯 Perfect for ChatGPT:** This proxy enables ChatGPT to access and analyze any web content without restrictions, making it ideal for research, data analysis, and content investigation.

It helps bypass bot/anti-scraping blocks that affect some cloud egress IPs by fetching content from your Azure app and returning the raw upstream response (HTML, JSON, PDF, images, etc.).

> ⚠️ Use responsibly. Do not use this to bypass paywalls, authentication, or legal restrictions. Respect `robots.txt` and the target websites' Terms of Service.

## 🤖 Quick Start for ChatGPT

### 🚀 Fastest Setup (5 minutes)

1. **Clone and setup:**
   ```bash
   git clone https://github.com/alejandrolmeida/azure-fetch-proxy.git
   cd azure-fetch-proxy
   ./setup_conda.sh
   conda activate proxy
   ```

2. **Start the proxy:**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8003 --reload
   ```

3. **Ready for ChatGPT!** Use this format:
   ```
   http://localhost:8003/fetch?url=YOUR_URL_HERE&api_key=YOUR_API_KEY_HERE
   ```
   
   > ⚠️ **Important**: ChatGPT cannot access `localhost` directly. For ChatGPT integration, you need to:
   > - **Deploy to Azure** (recommended): Use `./start_azure.sh` 
   > - **Use ngrok** (testing): `ngrok http 8003` to expose localhost temporarily
   > - See `LOCALHOST_LIMITATION.md` for detailed solutions

### 💬 ChatGPT Examples (Copy & Paste Ready)

#### 📰 **Analyze News Articles:**
```
Analyze this technology article and summarize the key points:
http://localhost:8003/fetch?url=https://www.bbc.com/news/technology&api_key=YOUR_API_KEY_HERE
```

#### 📊 **Examine APIs and Data:**
```
Review the VS Code repository information and provide important statistics:
http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE
```

#### 🔍 **Research Documentation:**
```
Analyze this technical documentation and explain the main concepts:
http://localhost:8003/fetch?url=https://docs.python.org/3/library/asyncio.html&api_key=YOUR_API_KEY_HERE
```

#### 🌐 **Website Analysis:**
```
Examine the content of this website and describe its purpose:
http://localhost:8003/fetch?url=https://www.python.org&api_key=YOUR_API_KEY_HERE
```

---

## 🚀 Enhanced Features

### 🤖 ChatGPT Integration
- **Query parameter authentication**: Perfect for ChatGPT URLs (`?api_key=...`)
- **Header authentication**: Also supports `x-api-key` header for advanced use
- **Optimized rate limiting**: 100 requests/minute, 2000 requests/hour
- **Large response support**: Up to 15MB responses for comprehensive content
- **Smart content decompression**: Ensures proper display in browsers and analysis tools

### Core Functionality
- `GET|HEAD|POST /fetch?url=...` — fetch any `http/https` URL with multiple HTTP methods
- **Advanced SSRF protections**: blocks private/link-local/loopback/metadata IPs, including IPv6-mapped IPv4 addresses
- **Intelligent retries** on transient network/5xx errors
- **Configurable user agents**: `ua=desktop|mobile` to reduce basic bot filtering
- **Enhanced AMP support**: tries `/amp` paths and `?output=amp` parameter, plus `<link rel="amphtml">` discovery

### 🔐 Security & Access Control
- **Dual API key authentication**: Works with both header (`x-api-key`) and query parameter (`api_key`)
- **Host allowlist**: `ALLOWED_HOSTS` env var for restricting target domains
- **Host blocklist**: `BLOCKED_HOSTS` env var for blocking specific domains
- **Enhanced rate limiting**: Per-IP tracking with configurable limits
- **Response size limits**: Configurable maximum response size protection
- **Header forwarding safelist**: Securely forward specific headers like `If-None-Match`, `If-Modified-Since`

### ⚡ Performance & Caching
- **In-memory LRU cache**: 128 items, 120-second TTL for GET requests returning 200/304
- **Cache headers**: `X-Cache: HIT|MISS` to indicate cache status
- **Connection pooling**: HTTP/2 support with optimized connection limits

### 📊 Observability & Monitoring
- **Structured logging**: Request IDs, timing, response sizes with loguru
- **Prometheus metrics**: Request counters, duration histograms, cache operations, active connections
- **Metrics endpoint**: `/metrics` for monitoring integration
- **Security info endpoint**: `/security-info` for configuration verification
- **Health check endpoint**: `/healthz` for service monitoring

### 🛠 Developer Experience
- **Comprehensive test suite**: pytest with async support, SSRF tests, integration tests (15/15 tests passing)
- **Enhanced documentation**: Built-in usage examples at root endpoint
- **Content-Disposition**: Auto-adds filename for PDFs and images
- **ChatGPT-ready examples**: Pre-configured prompts and URL formats
- **Azure deployment scripts**: Secure deployment automation with `start_azure.sh`

## Quick Start

### 🤖 Option 1: ChatGPT Ready Setup (Recommended)
```bash
# Clone and configure
git clone https://github.com/alejandrolmeida/azure-fetch-proxy.git
cd azure-fetch-proxy

# Setup conda environment "proxy"
chmod +x setup_conda.sh
./setup_conda.sh

# Activate environment
conda activate proxy

# Start server optimized for ChatGPT
uvicorn main:app --host 127.0.0.1 --port 8003 --reload

# ✅ Ready! Use this format in ChatGPT:
# http://localhost:8003/fetch?url=YOUR_URL&api_key=YOUR_API_KEY_HERE
```

### 🔧 Option 2: Custom Configuration
```bash
# Clone and configure
git clone https://github.com/alejandrolmeida/azure-fetch-proxy.git
cd azure-fetch-proxy

# Configure conda environment
chmod +x setup_conda.sh
./setup_conda.sh

# Activate environment
conda activate proxy

# Run tests to verify everything works
pytest tests/ -v  # Should show 15/15 passing

# Configure environment variables (customize as needed)
cp .env.example .env  # Copy example file
# Edit .env with your actual API key and settings
export API_KEY="your-custom-api-key"           # Your custom API key
export ALLOWED_HOSTS="example.com,test.com"   # Restrict to specific domains
export BLOCKED_HOSTS="badsite.com"            # Block specific domains
export MAX_REQUESTS_PER_MINUTE=100            # Rate limiting
export MAX_REQUESTS_PER_HOUR=2000             # Hourly limit
export MAX_RESPONSE_SIZE_MB=15                # Response size limit

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the script
./start_conda.sh
```

### 🧪 Testing
```bash
# With conda (activate environment first)
conda activate proxy
pytest tests/ -v  # Should show 15/15 tests passing

# Or run directly with conda
conda run -n proxy pytest tests/ -v

# With pip/venv
pytest tests/ -v

# Test specific areas
pytest tests/test_ssrf.py -v      # SSRF protection tests
pytest tests/test_fetch.py -v     # Core functionality tests

# Verify ChatGPT setup
curl "http://localhost:8003/fetch?url=https://httpbin.org/json&api_key=YOUR_API_KEY_HERE"
```

## 🤖 ChatGPT Integration Guide

### ⚠️ Important: Localhost Limitation

**ChatGPT cannot access `localhost` URLs** because:
- ChatGPT runs on OpenAI's servers, not your local machine  
- Web services cannot access private networks for security reasons
- `localhost` is only accessible from your own computer

### 🌐 Solutions for ChatGPT Integration

1. **Azure Deployment (Recommended)**:
   ```bash
   ./start_azure.sh  # Deploy to Azure
   # Use: https://your-app.azurewebsites.net/fetch?url=...
   ```

2. **ngrok Tunnel (Testing)**:
   ```bash
   ngrok http 8003  # Expose localhost temporarily
   # Use: https://abc123.ngrok.io/fetch?url=...
   ```

3. **Other Cloud Providers**: Deploy on AWS, DigitalOcean, etc.

### 🎯 Perfect for ChatGPT Use Cases

- **📚 Research & Analysis**: Academic papers, documentation, APIs
- **📰 Content Analysis**: News articles, blog posts, websites  
- **💼 Business Intelligence**: Market research, competitor analysis
- **🔧 Development**: GitHub repositories, technical documentation
- **📊 Data Extraction**: JSON APIs, structured data sources

### 🌐 URL Format for ChatGPT
```
# For localhost (testing only with ngrok):
https://your-ngrok-url.ngrok.io/fetch?url=TARGET_URL&api_key=YOUR_API_KEY_HERE

# For Azure deployment (production):
https://your-app.azurewebsites.net/fetch?url=TARGET_URL&api_key=YOUR_API_KEY_HERE
```

> ⚠️ **ChatGPT Limitation**: ChatGPT cannot access `localhost` URLs. You must use a public URL (Azure deployment or ngrok tunnel).

### 💡 Pro Tips for ChatGPT

1. **Be Specific**: Tell ChatGPT exactly what you want to analyze
   ```
   "Analyze the GitHub API data for VS Code and summarize the key metrics"
   ```

2. **Provide Context**: Explain the type of content before giving the URL
   ```
   "This is a Python documentation page about asyncio. Explain the main concepts:"
   ```

3. **Request Structured Output**: Ask for specific formats
   ```
   "Create a table with the main features and their descriptions from this API documentation"
   ```

### 🚀 Ready-to-Use ChatGPT Prompts

Copy these prompts directly into ChatGPT:

#### For APIs:
```
Analyze this GitHub repository data and provide insights about the project's health and activity:
https://your-app.azurewebsites.net/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE
```

#### For Documentation:
```
Read this technical documentation and create a beginner-friendly summary with examples:
https://your-app.azurewebsites.net/fetch?url=https://docs.python.org/3/library/asyncio.html&api_key=YOUR_API_KEY_HERE
```

#### For News/Articles:
```
Analyze this technology news article and summarize the key points and implications:
https://your-app.azurewebsites.net/fetch?url=https://httpbin.org/html&api_key=YOUR_API_KEY_HERE
```

> 💡 **Note**: Replace `your-app.azurewebsites.net` with your actual Azure domain, or use ngrok URL for testing.

## 📚 API Reference

### Core Endpoints

#### `GET|HEAD|POST /fetch`
Main proxy endpoint supporting multiple HTTP methods.

**Query Parameters:**
- `url` (required): absolute `http/https` URL to fetch
- `api_key` (required if API_KEY is set): authentication key for security
- `method` (optional): `GET` (default), `HEAD`, or `POST` 
- `ua` (optional): `desktop` (default) or `mobile` user agent
- `timeout` (optional): read timeout in seconds (1–60, default 15)
- `max_redirects` (optional): maximum redirects to follow (0–10, default 5)
- `try_amp` (optional): attempt to find AMP variant if initial request fails
- `accept` (optional): custom Accept header
- `lang` (optional): Accept-Language header (default: "es-ES,es;q=0.9,en;q=0.8")
- `forward_headers` (optional): comma-separated list of headers to forward from client

**Headers:**
- `x-api-key`: API key (alternative to query parameter, required if `API_KEY` environment variable is set)
- `Content-Type`: For POST requests, forwarded to upstream server

**Examples:**
```bash
# Basic GET request
curl "http://localhost:8003/fetch?url=https://httpbin.org/get&api_key=YOUR_API_KEY_HERE"

# ChatGPT-ready format
curl "http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE"

# POST request with body
curl -X POST "http://localhost:8003/fetch?url=https://httpbin.org/post&method=POST&api_key=YOUR_API_KEY_HERE" \
     -H "Content-Type: application/json" \
     -d '{"key": "value"}'

# HEAD request
curl -I "http://localhost:8003/fetch?url=https://httpbin.org/get&method=HEAD&api_key=YOUR_API_KEY_HERE"

# With API key in header (alternative method)
curl -H "x-api-key: YOUR_API_KEY_HERE" \
     "http://localhost:8003/fetch?url=https://httpbin.org/get"

# Forward conditional headers
curl -H "If-None-Match: \"abc123\"" \
     "http://localhost:8003/fetch?url=https://httpbin.org/get&forward_headers=if-none-match&api_key=YOUR_API_KEY_HERE"

# Mobile user agent with AMP attempt
curl "http://localhost:8003/fetch?url=https://example.com/article&ua=mobile&try_amp=true&api_key=YOUR_API_KEY_HERE"
```

#### `GET /security-info`
Security configuration endpoint showing current settings.

**Query Parameters:**
- `api_key` (required if API_KEY is set): authentication key

**Response:** JSON object with current security configuration:
```json
{
  "api_key_required": true,
  "allowed_hosts": null,
  "blocked_hosts_count": 9,
  "rate_limits": {
    "max_requests_per_minute": 100,
    "max_requests_per_hour": 2000,
    "max_response_size_mb": 15
  },
  "user_agent": "ChatGPT-Proxy-Service/1.0",
  "cache_size": 0,
  "version": "1.0.0"
}
```

#### `GET /healthz`
Health check endpoint returning "ok".

#### `GET /metrics`
Prometheus-compatible metrics endpoint with:
- `proxy_requests_total` - Total requests by method and status
- `proxy_request_duration_seconds` - Request duration histogram  
- `proxy_cache_operations_total` - Cache hit/miss/store operations
- `proxy_active_connections` - Current active HTTP connections

#### `GET /`
Interactive documentation and usage examples.

### Response Headers

All successful responses include:
- `X-Cache`: `HIT` or `MISS` indicating cache status
- Original upstream headers (filtered for security)
- `Content-Disposition`: Auto-added for PDFs and images when missing

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | ChatGPT Optimized |
|----------|-------------|---------|-------------------|
| `API_KEY` | Require this API key in `x-api-key` header or `api_key` query param | None (no auth required) | `your-secure-api-key` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed target hostnames | None (all hosts allowed) | None (for maximum flexibility) |
| `BLOCKED_HOSTS` | Comma-separated list of blocked target hostnames | None (no hosts blocked) | Private networks automatically blocked |
| `MAX_REQUESTS_PER_MINUTE` | Rate limit per IP per minute | 60 | 100 |
| `MAX_REQUESTS_PER_HOUR` | Rate limit per IP per hour | 1000 | 2000 |
| `MAX_RESPONSE_SIZE_MB` | Maximum response size in MB | 10 | 15 |
| `CUSTOM_USER_AGENT` | Custom User-Agent string | `AzureProxyService/1.0` | `ChatGPT-Proxy-Service/1.0` |

### Examples
```bash
# ChatGPT optimized setup
export API_KEY="your-secure-api-key"
export MAX_REQUESTS_PER_MINUTE=100
export MAX_REQUESTS_PER_HOUR=2000
export MAX_RESPONSE_SIZE_MB=15
export CUSTOM_USER_AGENT="ChatGPT-Proxy-Service/1.0"

# Security-focused setup
export API_KEY="super-secret-key-123"
export ALLOWED_HOSTS="httpbin.org,api.github.com,docs.python.org"
export BLOCKED_HOSTS="malicious-site.com,blocked-domain.org"

# Development setup (no restrictions)
# Don't set API_KEY for development
export MAX_REQUESTS_PER_MINUTE=200
```

## 🔒 Security Features

### Enhanced SSRF Protection
- Resolves hostnames to IP addresses before making requests
- Blocks private networks (RFC 1918), loopback, link-local, multicast
- Enhanced IPv6 support including IPv6-mapped IPv4 addresses
- Blocks cloud metadata endpoints (169.254.169.254, metadata.google.internal, metadata.azure.com)
- Prevents DNS rebinding attacks
- **Automatic blocking of 9+ dangerous hosts/networks**

### Advanced Authentication
- **Dual authentication methods**: Header (`x-api-key`) or query parameter (`api_key`)
- **Perfect for ChatGPT**: Query parameter method works seamlessly in URLs
- API key rotation support
- Optional authentication (can be disabled for development)

### Rate Limiting & Protection
- **Per-IP rate limiting**: Configurable requests per minute and hour
- **Response size limits**: Prevent abuse with large downloads
- **Request tracking**: Monitor usage patterns
- **Graceful degradation**: Informative error messages

### Header Security
- Strips hop-by-hop headers (Connection, Transfer-Encoding, etc.)
- Whitelists safe response headers for pass-through
- Safelist for forwarded request headers prevents header injection
- **Content decompression**: Ensures proper browser/tool compatibility

## 🚀 Deployment

### 🌐 Azure App Service Deployment (Production Ready)

The proxy includes automated deployment scripts optimized for security:

#### Quick Azure Deployment
```bash
# 1. Configure environment
cp .env.azure .env
# Edit .env with your settings

# 2. Run secure deployment script
chmod +x start_azure.sh
./start_azure.sh

# 3. Follow Azure CLI deployment steps below
```

#### Manual Azure Deployment

1. **Login & set subscription** (if needed):
   ```bash
   az login
   az account set --subscription "<SUBSCRIPTION_NAME_OR_ID>"
   ```

2. **Create resource group and plan**:
   ```bash
   az group create -n rg-proxy-fastapi -l westeurope
   az appservice plan create -g rg-proxy-fastapi -n asp-proxy-fastapi --sku B1 --is-linux
   ```

3. **Create the web app** (Python 3.11 image):
   ```bash
   az webapp create -g rg-proxy-fastapi -p asp-proxy-fastapi -n <your-unique-app-name> \
     --runtime "PYTHON:3.11"
   ```

4. **Configure startup command** (Gunicorn + Uvicorn worker):
   ```bash
   az webapp config set -g rg-proxy-fastapi -n <your-unique-app-name> \
     --startup-file "gunicorn -k uvicorn.workers.UvicornWorker -w 2 -t 120 main:app"
   ```

5. **Deploy your code** (zip deploy is simplest):
   ```bash
   zip -r app.zip .
   az webapp deployment source config-zip -g rg-proxy-fastapi -n <your-unique-app-name> \
     --src app.zip
   ```

6. **Configure environment variables** for ChatGPT optimization:
   ```bash
   # Set API key for authentication
   az webapp config appsettings set -g rg-proxy-fastapi -n <your-unique-app-name> \
     --settings API_KEY="your-secure-api-key"

   # Configure ChatGPT-optimized settings
   az webapp config appsettings set -g rg-proxy-fastapi -n <your-unique-app-name> \
     --settings MAX_REQUESTS_PER_MINUTE=100 MAX_REQUESTS_PER_HOUR=2000 MAX_RESPONSE_SIZE_MB=15

   # Optional: Restrict to specific domains  
   az webapp config appsettings set -g rg-proxy-fastapi -n <your-unique-app-name> \
     --settings ALLOWED_HOSTS="httpbin.org,api.github.com,docs.python.org"
   ```

7. **Test your deployment**:
   ```
   https://<your-unique-app-name>.azurewebsites.net/healthz
   https://<your-unique-app-name>.azurewebsites.net/security-info?api_key=YOUR_API_KEY_HERE
   https://<your-unique-app-name>.azurewebsites.net/fetch?url=https://httpbin.org/json&api_key=YOUR_API_KEY_HERE
   ```

8. **Update your ChatGPT URLs** to use your Azure domain:
   ```
   https://<your-unique-app-name>.azurewebsites.net/fetch?url=TARGET_URL&api_key=YOUR_API_KEY_HERE
   ```

### Performance Notes
- **Enhanced caching**: GET requests returning 200/304 are cached for 120 seconds
- **HTTP/2**: Enabled for better performance with upstream servers
- **Connection pooling**: Reuses connections to improve latency
- **Background metrics**: Prometheus metrics don't impact request performance
- **Optimized for ChatGPT**: Rate limits and response sizes tuned for AI analysis

### Scaling
- Scale out by increasing workers (`-w`) in the Gunicorn command
- Scale up by upgrading the App Service Plan
- Monitor with `/metrics` and `/security-info` endpoints
- Set up alerts for rate limiting and errors

### Monitoring
- Use `/healthz` for health checks
- Check `/security-info` for current configuration
- Scrape `/metrics` with Prometheus for detailed monitoring
- Check logs for request IDs and performance data
- Monitor rate limiting effectiveness

## 🛠 Development

### Project Structure
```
├── main.py                   # Main FastAPI application with ChatGPT optimizations
├── requirements.txt          # Python dependencies for pip
├── environment.yml           # Conda environment configuration
├── runtime.txt              # Python version for Azure
├── pytest.ini              # Test configuration
├── setup_conda.sh           # Conda environment setup script
├── start.sh                 # Startup script for pip/venv
├── start_conda.sh           # Startup script for conda
├── start_azure.sh           # Secure Azure deployment script
├── .env.example             # Environment variables template
├── .env.azure               # Azure environment template
├── tests/                   # Comprehensive test suite (15/15 passing)
│   ├── test_ssrf.py         # SSRF protection tests
│   └── test_fetch.py        # Core functionality tests
├── requests.http            # HTTP request examples
├── CHATGPT_USAGE.md         # ChatGPT integration guide
├── READY_FOR_CHATGPT.md     # Quick ChatGPT setup guide
├── AZURE_SECURITY.md        # Azure security best practices
├── ENHANCEMENT_SUMMARY.md   # Summary of implemented improvements
└── README.md               # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch  
3. Add tests for new functionality
4. Ensure all tests pass: `pytest tests/ -v` (should show 15/15 passing)
5. Test ChatGPT integration with your changes
6. Submit a pull request

## 🤖 ChatGPT Success Stories

This proxy has been specifically optimized for ChatGPT integration. Perfect for:

- **🔬 Research**: Academic papers, technical documentation, scientific articles
- **📊 Data Analysis**: APIs, JSON data, structured information  
- **📰 Content Analysis**: News articles, blog posts, web content
- **💼 Business Intelligence**: Market research, competitor analysis
- **🛠️ Development**: GitHub repositories, documentation, code examples

## 📋 ChatGPT Checklist

- [x] ✅ Dual authentication (header + query parameter)
- [x] ✅ Optimized rate limiting (100/min, 2000/hour) 
- [x] ✅ Large response support (15MB)
- [x] ✅ Content decompression for proper display
- [x] ✅ SSRF protection for security
- [x] ✅ Ready-to-use examples and prompts
- [x] ✅ Comprehensive documentation
- [x] ✅ Azure deployment ready
- [x] ✅ 15/15 tests passing

## 📊 Monitoring & Metrics

The `/metrics` endpoint provides Prometheus-compatible metrics:

```
# Request counters by method and status
proxy_requests_total{method="GET",status="200"} 42

# Request duration histogram
proxy_request_duration_seconds_bucket{le="0.1"} 15
proxy_request_duration_seconds_bucket{le="0.5"} 38

# Cache operations
proxy_cache_operations_total{operation="hit"} 8
proxy_cache_operations_total{operation="miss"} 34
proxy_cache_operations_total{operation="store"} 30

# Active connections
proxy_active_connections 3
```

## 🔧 Advanced Usage

### ChatGPT-Optimized Requests
Forward caching headers for efficient bandwidth usage:

```bash
# Forward If-None-Match for ETag validation
curl -H "If-None-Match: \"abc123\"" \
     "http://localhost:8003/fetch?url=https://httpbin.org/etag/abc123&forward_headers=if-none-match&api_key=YOUR_API_KEY_HERE"

# Forward If-Modified-Since for timestamp validation  
curl -H "If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT" \
     "http://localhost:8003/fetch?url=https://httpbin.org/get&forward_headers=if-modified-since&api_key=YOUR_API_KEY_HERE"
```

### Bulk Operations for Research
Use the cache effectively for repeated requests:

```bash
# First request - cache miss
time curl "http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE"

# Second request - cache hit (much faster)
time curl "http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE"
```

### Error Handling
The proxy provides detailed error responses for troubleshooting:

- `400`: Invalid URL, SSRF protection triggered, or host not allowed
- `401`: Missing or invalid API key
- `403`: Host blocked by blocklist  
- `429`: Rate limit exceeded
- `502`: Upstream server error or DNS resolution failed
- `413`: Response too large (exceeds size limit)
- `422`: Invalid query parameters

## ⚠️ Security Considerations

### Enhanced SSRF Protection
This proxy implements comprehensive SSRF (Server-Side Request Forgery) protection:

- ✅ Blocks private networks (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- ✅ Blocks loopback (127.0.0.0/8, ::1)
- ✅ Blocks link-local (169.254.0.0/16, fe80::/10)
- ✅ Blocks multicast and broadcast
- ✅ Blocks cloud metadata (169.254.169.254, metadata.google.internal, metadata.azure.com)
- ✅ Handles IPv6-mapped IPv4 addresses
- ✅ Validates against reserved/unique-local IPv6 ranges
- ✅ **9+ dangerous hosts/networks automatically blocked**

### Production Deployment Security
For production use with ChatGPT, consider:

- **✅ API Key Authentication**: Always set `API_KEY` in production
- **✅ Rate Limiting**: Built-in per-IP rate limiting active
- **✅ Response Size Limits**: 15MB limit prevents abuse
- **✅ WAF**: Deploy behind Azure Front Door or Application Gateway with WAF
- **✅ Monitoring**: Set up alerts on metrics and logs via `/metrics` endpoint
- **✅ Network Isolation**: Use virtual networks and private endpoints where possible
- **✅ Regular Security Audits**: Monitor `/security-info` endpoint
- **✅ API Key Rotation**: Regularly rotate API keys for security

### ChatGPT-Specific Security
- **Query Parameter Auth**: Secure for ChatGPT URLs (HTTPS encrypted)
- **Content Filtering**: Automatic decompression prevents malformed content
- **User Agent Identification**: Custom UA `ChatGPT-Proxy-Service/1.0` for tracking
- **Request Logging**: All requests logged for audit purposes
---

## 🎉 Ready for ChatGPT!

Your proxy is now **fully optimized for ChatGPT integration**:

### ✅ **Quick Test**
```bash
curl "http://localhost:8003/fetch?url=https://httpbin.org/json&api_key=YOUR_API_KEY_HERE"
```

### 🚀 **Use in ChatGPT**
```
Analyze this API data and tell me about the content structure:
https://your-app.azurewebsites.net/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY_HERE
```

> 🔧 **For Development**: Use ngrok to test with ChatGPT before Azure deployment

### 📚 **Additional Resources**
- `LOCALHOST_LIMITATION.md` - Solutions for ChatGPT localhost access
- `CHATGPT_USAGE.md` - Detailed ChatGPT integration guide
- `READY_FOR_CHATGPT.md` - Quick setup and examples
- `AZURE_SECURITY.md` - Production deployment security guide

---

© 2025 Alejandro L. Meida. Licensed as MIT. **Optimized for ChatGPT integration.**
