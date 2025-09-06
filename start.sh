#!/bin/bash

# Azure FastAPI Fetch Proxy - Enhanced Version Demo Script

echo "🚀 Azure FastAPI Fetch Proxy - Enhanced Version"
echo "=============================================="
echo

# Check if conda environment "proxy" exists
if conda env list | grep -q "proxy"; then
    echo "📦 Using conda environment 'proxy'..."
    echo "   Dependencies already installed in conda environment"
else
    echo "📦 Installing dependencies with pip..."
    pip install -r requirements.txt
fi

echo
echo "🧪 Running tests..."
if conda env list | grep -q "proxy"; then
    conda run -n proxy pytest tests/ -v
else
    pytest tests/ -v
fi

echo
echo "🔧 Configuration Options:"
echo "- API_KEY: Set to require API key authentication"
echo "- ALLOWED_HOSTS: Comma-separated list of allowed hostnames" 
echo "- BLOCKED_HOSTS: Comma-separated list of blocked hostnames"
echo

echo "🌟 New Features Added:"
echo "✅ 1. API key authentication via x-api-key header"
echo "✅ 2. HEAD/POST method support via 'method' query parameter"
echo "✅ 3. In-memory LRU cache (128 items, 120s TTL) with X-Cache headers"
echo "✅ 4. Selected header forwarding with safelist protection"
echo "✅ 5. Host allowlist/blocklist support"
echo "✅ 6. Enhanced IPv6 SSRF protection"
echo "✅ 7. Better AMP heuristics (?output=amp support)"
echo "✅ 8. Auto Content-Disposition for PDFs and images"
echo "✅ 9. Structured logging with loguru + Prometheus metrics"
echo "✅ 10. Comprehensive test suite with pytest"
echo

echo "📊 Available Endpoints:"
echo "- GET /          - Documentation and usage"
echo "- GET /healthz   - Health check"
echo "- GET /metrics   - Prometheus metrics"
echo "- GET /robots.txt - Robots.txt"
echo "- GET|HEAD|POST /fetch - Main proxy endpoint"
echo

echo "🔗 Example Usage:"
echo "# Basic fetch"
echo "curl 'http://localhost:8003/fetch?url=https://httpbin.org/get'"
echo
echo "# With API key (if API_KEY env var is set)"
echo "curl -H 'x-api-key: your-key' 'http://localhost:8003/fetch?url=https://httpbin.org/get'"
echo
echo "# POST method with body"
echo "curl -X POST 'http://localhost:8003/fetch?url=https://httpbin.org/post&method=POST' -d 'test data'"
echo
echo "# Mobile user agent"
echo "curl 'http://localhost:8003/fetch?url=https://httpbin.org/get&ua=mobile'"
echo
echo "# Forward specific headers"
echo "curl -H 'If-None-Match: \"abc123\"' 'http://localhost:8003/fetch?url=https://httpbin.org/get&forward_headers=if-none-match'"
echo
echo "# Try AMP variant"
echo "curl 'http://localhost:8003/fetch?url=https://example.com/article&try_amp=true'"
echo
echo "# Test with Amazon URL (should work in browser too)"
echo "curl 'http://localhost:8003/fetch?url=https://amzn.eu/d/6TXZZ6k'"
echo

echo "🚀 Starting server on port 8003..."
echo "   Navigate to: http://localhost:8003/"
echo "   Health check: http://localhost:8003/healthz"  
echo "   Use Ctrl+C to stop"
echo

# Start the server
if conda env list | grep -q "proxy"; then
    conda run -n proxy uvicorn main:app --host 0.0.0.0 --port 8003 --reload
else
    uvicorn main:app --host 0.0.0.0 --port 8003 --reload
fi
