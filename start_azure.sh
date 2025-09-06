#!/bin/bash

# Azure Deployment Script for Enhanced FastAPI Fetch Proxy

echo "🔒 Azure FastAPI Fetch Proxy - SECURE DEPLOYMENT"
echo "==============================================="
echo

# Check required security settings
echo "🛡️ Security Pre-flight Check..."
if [ -z "$API_KEY" ]; then
    echo "❌ ERROR: API_KEY environment variable is required for Azure deployment"
    echo "   Set it with: export API_KEY='your-super-secure-random-key'"
    exit 1
fi

if [ -z "$ALLOWED_HOSTS" ]; then
    echo "⚠️  WARNING: ALLOWED_HOSTS not set - proxy will accept requests to ANY domain"
    echo "   Consider setting: export ALLOWED_HOSTS='trusted-domain1.com,trusted-domain2.com'"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ API_KEY is configured"
echo "✅ Rate limiting: ${MAX_REQUESTS_PER_MINUTE:-60}/min, ${MAX_REQUESTS_PER_HOUR:-1000}/hour"
echo "✅ Max response size: ${MAX_RESPONSE_SIZE_MB:-10}MB"

if [ -n "$ALLOWED_HOSTS" ]; then
    echo "✅ Domain allowlist: $ALLOWED_HOSTS"
else
    echo "⚠️  No domain restrictions"
fi

echo

# Check if conda environment exists
if conda env list | grep -q "proxy"; then
    echo "📦 Using conda environment 'proxy'..."
    PYTHON_CMD="conda run -n proxy"
else
    echo "📦 Using system Python..."
    PYTHON_CMD=""
    pip install -r requirements.txt
fi

echo
echo "🧪 Running security-focused tests..."
$PYTHON_CMD pytest tests/ -v -k "test_api_key or test_ssrf or test_host"

echo
echo "🔧 Azure-specific Configuration:"
echo "- API_KEY: ✅ REQUIRED (configured)"
echo "- ALLOWED_HOSTS: ${ALLOWED_HOSTS:-'⚠️ NOT SET (allows all domains)'}"
echo "- BLOCKED_HOSTS: Includes cloud metadata endpoints"
echo "- Rate Limits: ${MAX_REQUESTS_PER_MINUTE:-60}/min, ${MAX_REQUESTS_PER_HOUR:-1000}/hour"
echo "- Max Response: ${MAX_RESPONSE_SIZE_MB:-10}MB"
echo

echo "🌟 Azure Security Features:"
echo "✅ 1. MANDATORY API key authentication"
echo "✅ 2. Rate limiting (per-IP based)"
echo "✅ 3. Response size limits"
echo "✅ 4. Cloud metadata endpoint blocking"
echo "✅ 5. Enhanced SSRF protection"
echo "✅ 6. Domain allowlist/blocklist support"
echo "✅ 7. Security monitoring endpoints"
echo "✅ 8. Request logging and metrics"
echo

echo "📊 Available Endpoints:"
echo "- GET /               - Main page with security status"
echo "- GET /healthz        - Health check"
echo "- GET /metrics        - Prometheus metrics"
echo "- GET /security-info  - Security configuration"
echo "- GET /robots.txt     - Robots.txt"
echo "- GET|HEAD|POST /fetch - Main proxy endpoint (requires API key)"
echo

echo "🔗 Secure Usage Examples:"
echo "# All requests require API key header"
echo "curl -H 'x-api-key: $API_KEY' 'http://localhost:8003/fetch?url=https://httpbin.org/get'"
echo
echo "# Check security configuration"
echo "curl 'http://localhost:8003/security-info'"
echo

echo "🚀 Starting SECURE server on port 8003..."
echo "   🔒 API Key authentication: ENABLED"
echo "   🚧 Rate limiting: ENABLED"
echo "   🛡️ SSRF protection: ENABLED"
echo "   📊 Security monitoring: http://localhost:8003/security-info"
echo "   Use Ctrl+C to stop"
echo

# Start the server with security-hardened settings
$PYTHON_CMD uvicorn main:app --host 0.0.0.0 --port 8003 --workers 1 --access-log
