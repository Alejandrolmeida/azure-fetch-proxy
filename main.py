
import asyncio
import hashlib
import ipaddress
import os
import re
import socket
import time
from datetime import datetime, timedelta
from typing import Iterable, List, Optional, Dict, Any, Tuple
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

import httpx
from cachetools import TTLCache
from fastapi import FastAPI, HTTPException, Query, Response, Request, Depends, status
from fastapi.responses import StreamingResponse, PlainTextResponse, JSONResponse, HTMLResponse
from fastapi.security import APIKeyHeader
from loguru import logger
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.cors import CORSMiddleware

APP_NAME = "Azure FastAPI Fetch Proxy"
VERSION = "1.0.0"

# Configuration from environment
API_KEY = os.getenv("API_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else None
BLOCKED_HOSTS = set(host.strip() for host in os.getenv("BLOCKED_HOSTS", "").split(",") if host.strip())

# Enhanced security configuration for Azure
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
MAX_REQUESTS_PER_HOUR = int(os.getenv("MAX_REQUESTS_PER_HOUR", "1000"))
MAX_RESPONSE_SIZE_MB = int(os.getenv("MAX_RESPONSE_SIZE_MB", "10"))
CUSTOM_USER_AGENT = os.getenv("CUSTOM_USER_AGENT", "AzureProxyService/1.0")

# Add critical infrastructure IPs to blocked hosts
BLOCKED_HOSTS.update({
    "169.254.169.254",  # AWS metadata
    "metadata.google.internal",  # GCP metadata
    "metadata.azure.com",  # Azure metadata
    "localhost", "127.0.0.1", "::1",  # Localhost variants
    "0.0.0.0", "10.0.0.1", "192.168.1.1"  # Common gateway IPs
})

# Security
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Rate limiting storage (in production, use Redis or similar)
rate_limit_store = {
    "minute": {},  # {client_ip: [(timestamp, count), ...]}
    "hour": {}
}

# Cache setup
response_cache = TTLCache(maxsize=128, ttl=120)

# Metrics
request_counter = Counter("proxy_requests_total", "Total requests", ["method", "status"])
request_duration = Histogram("proxy_request_duration_seconds", "Request duration")
cache_counter = Counter("proxy_cache_operations_total", "Cache operations", ["operation"])
active_connections = Gauge("proxy_active_connections", "Active connections")

# Configure logging
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

app = FastAPI(title=APP_NAME, version=VERSION)

# CORS: allow all by default (you can restrict via env or edit here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple desktop UA string to reduce bot-blocking
DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
MOBILE_UA = (
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
)

# Denylist for SSRF protection - Enhanced IPv6 support
DENY_IPS = {
    ipaddress.ip_address("169.254.169.254"),  # cloud metadata
}

def _is_private_ip(ip: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj in DENY_IPS:
            return True
        
        # Handle IPv6-mapped IPv4 addresses
        if isinstance(ip_obj, ipaddress.IPv6Address):
            if ip_obj.ipv4_mapped:
                ipv4_part = ip_obj.ipv4_mapped
                return (
                    ipv4_part.is_private
                    or ipv4_part.is_loopback
                    or ipv4_part.is_link_local
                    or ipv4_part.is_reserved
                    or ipv4_part.is_multicast
                )
            # Check IPv6 unique local addresses (fc00::/7)
            if ip_obj.is_private or ip_obj.is_site_local:
                return True
        
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
            or ip_obj.is_multicast
            or ip_obj.is_unspecified
        )
    except ValueError:
        return True

def _resolve_host_ips(host: str) -> List[str]:
    try:
        infos = socket.getaddrinfo(host, None)
        ips = []
        for info in infos:
            sockaddr = info[4]
            ip = sockaddr[0]
            ips.append(ip)
        # deduplicate
        return list(dict.fromkeys(ips))
    except socket.gaierror:
        return []

def _check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limits"""
    import time
    now = time.time()
    
    # Clean old entries
    for period in ["minute", "hour"]:
        if client_ip in rate_limit_store[period]:
            cutoff = now - (60 if period == "minute" else 3600)
            rate_limit_store[period][client_ip] = [
                (ts, count) for ts, count in rate_limit_store[period][client_ip] 
                if ts > cutoff
            ]
    
    # Check minute limit
    minute_requests = sum(
        count for ts, count in rate_limit_store["minute"].get(client_ip, [])
        if ts > now - 60
    )
    if minute_requests >= MAX_REQUESTS_PER_MINUTE:
        return False
    
    # Check hour limit  
    hour_requests = sum(
        count for ts, count in rate_limit_store["hour"].get(client_ip, [])
        if ts > now - 3600
    )
    if hour_requests >= MAX_REQUESTS_PER_HOUR:
        return False
    
    # Record this request
    for period in ["minute", "hour"]:
        if client_ip not in rate_limit_store[period]:
            rate_limit_store[period][client_ip] = []
        rate_limit_store[period][client_ip].append((now, 1))
    
    return True

def verify_api_key(
    api_key_header: Optional[str] = Depends(api_key_header),
    api_key_query: Optional[str] = Query(None, alias="api_key")
) -> bool:
    """Verify API key if one is configured (accepts header or query parameter)"""
    if API_KEY is None:
        return True  # No API key required
    
    # Check both header and query parameter
    provided_key = api_key_header or api_key_query
    
    if provided_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return True

def check_host_permissions(hostname: str) -> bool:
    """Check if hostname is allowed based on allowlist/blocklist"""
    if hostname in BLOCKED_HOSTS:
        return False
    
    if ALLOWED_HOSTS is not None:
        return hostname in ALLOWED_HOSTS
    
    return True

def _make_cache_key(method: str, url: str, ua: str, accept: str, lang: str) -> str:
    """Generate cache key from request parameters"""
    key_data = f"{method}:{url}:{ua}:{accept}:{lang}"
    return hashlib.md5(key_data.encode()).hexdigest()

def _get_filename_from_path(url_path: str) -> str:
    """Extract filename from URL path for Content-Disposition"""
    if not url_path or url_path == "/" or url_path.endswith("/"):
        return "download"
    segments = url_path.strip("/").split("/")
    filename = segments[-1] if segments and segments[-1] else "download"
    return filename

def _clean_hop_by_hop(headers: dict) -> dict:
    hop_by_hop = {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
    }
    return {k: v for k, v in headers.items() if k.lower() not in hop_by_hop}

def _pick_headers_for_response(upstream_headers: dict) -> dict:
    allowed = {
        "content-type",
        "content-length",
        "etag",
        "last-modified",
        "cache-control",
        "expires",
        "date",
        "server",
        "content-disposition",
        "accept-ranges",
        "content-encoding",
        "vary",
    }
    out = {}
    for k, v in upstream_headers.items():
        kl = k.lower()
        if kl in allowed:
            out[k] = v
    return out

def _get_forwarded_headers(request: Request, forward_headers: List[str] = None) -> dict:
    """Get headers to forward from the incoming request"""
    # Safelist of headers we allow forwarding
    safelist = {
        "if-none-match",
        "if-modified-since",
        "if-match",
        "if-unmodified-since",
        "if-range",
        "range",
        "authorization",
        "cookie",
    }
    
    headers = {}
    if forward_headers:
        for header in forward_headers:
            header_lower = header.lower()
            if header_lower in safelist and header_lower in request.headers:
                headers[header] = request.headers[header_lower]
    
    return headers

@app.get("/", response_class=HTMLResponse)
async def root():
    security_status = "🔒 SECURED" if API_KEY else "⚠️ OPEN"
    allowed_info = f"Allowlist: {len(ALLOWED_HOSTS)} domains" if ALLOWED_HOSTS else "No domain restrictions"
    
    return f"""
    <html>
      <head><title>{APP_NAME}</title></head>
      <body>
        <h1>{APP_NAME} v{VERSION}</h1>
        <div style="background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px;">
          <h3>🛡️ Security Status: {security_status}</h3>
          <ul>
            <li>API Key Required: {'✅ YES' if API_KEY else '❌ NO'}</li>
            <li>Rate Limiting: {MAX_REQUESTS_PER_MINUTE}/min, {MAX_REQUESTS_PER_HOUR}/hour</li>
            <li>Max Response Size: {MAX_RESPONSE_SIZE_MB}MB</li>
            <li>{allowed_info}</li>
            <li>Blocked Hosts: {len(BLOCKED_HOSTS)} entries</li>
          </ul>
        </div>
        <p>Usage: <code>/fetch?url=https://example.com</code></p>
        <p>Optional query params:</p>
        <ul>
          <li><code>method=GET|HEAD|POST</code> (default: GET)</li>
          <li><code>ua=mobile|desktop</code> (default: desktop)</li>
          <li><code>timeout=</code> seconds (default: 15)</li>
          <li><code>max_redirects=</code> (default: 5)</li>
          <li><code>try_amp=true</code> (attempt to load AMP variant if available)</li>
          <li><code>accept=</code> custom Accept header</li>
          <li><code>lang=</code> Accept-Language header (e.g., es-ES, en-US;q=0.9)</li>
          <li><code>forward_headers=</code> comma-separated list of headers to forward</li>
        </ul>
        <p>Endpoints: <code>/healthz</code> | <code>/metrics</code> | <code>/security-info</code></p>
      </body>
    </html>
    """

@app.get("/healthz", response_class=PlainTextResponse)
async def healthz():
    return "ok"

@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/security-info")
async def security_info():
    """Security configuration information (for debugging)"""
    return JSONResponse({
        "api_key_required": API_KEY is not None,
        "allowed_hosts": ALLOWED_HOSTS,
        "blocked_hosts_count": len(BLOCKED_HOSTS),
        "rate_limits": {
            "max_requests_per_minute": MAX_REQUESTS_PER_MINUTE,
            "max_requests_per_hour": MAX_REQUESTS_PER_HOUR,
            "max_response_size_mb": MAX_RESPONSE_SIZE_MB
        },
        "user_agent": CUSTOM_USER_AGENT,
        "cache_size": len(response_cache),
        "version": VERSION
    })

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /\n"

@app.get("/fetch")
@app.head("/fetch")
@app.post("/fetch")
async def fetch(
    request: Request,
    url: str = Query(..., description="Absolute URL to fetch (http/https)."),
    method: str = Query("GET", pattern="^(GET|HEAD|POST)$"),
    ua: str = Query("desktop", pattern="^(desktop|mobile)$"),
    timeout: float = Query(15.0, ge=1.0, le=60.0),
    max_redirects: int = Query(5, ge=0, le=10),
    try_amp: bool = Query(False),
    accept: Optional[str] = Query(None),
    lang: Optional[str] = Query(None),
    forward_headers: Optional[str] = Query(None, description="Comma-separated list of headers to forward"),
    _: bool = Depends(verify_api_key),
):
    # Rate limiting check
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded. Max {MAX_REQUESTS_PER_MINUTE}/min or {MAX_REQUESTS_PER_HOUR}/hour"
        )
    
    start_time = time.time()
    request_id = hashlib.md5(f"{time.time()}{url}".encode()).hexdigest()[:8]
    
    logger.info(f"[{request_id}] {method} {url} - Starting request")
    
    # Basic URL validation
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only http/https URLs are allowed.")
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL.")

    # Check host permissions (allowlist/blocklist)
    if not check_host_permissions(parsed.hostname):
        raise HTTPException(status_code=403, detail="Host not allowed")

    # Prevent infinite loops by blocking calls to ourselves
    host_header = request.headers.get("host", "")
    if parsed.netloc == host_header:
        raise HTTPException(status_code=400, detail="Refusing to fetch this host (loop protection).")

    # SSRF protection: resolve and block private IPs
    ips = _resolve_host_ips(parsed.hostname)
    if not ips:
        raise HTTPException(status_code=502, detail="DNS resolution failed for target host.")
    if any(_is_private_ip(ip) for ip in ips):
        raise HTTPException(status_code=400, detail="Refusing to access private or disallowed IP ranges.")

    # Check cache for GET requests
    cache_key = None
    if method == "GET":
        cache_key = _make_cache_key(method, url, ua, accept or "*/*", lang or "es-ES,es;q=0.9,en;q=0.8")
        cached_response = response_cache.get(cache_key)
        if cached_response:
            cache_counter.labels(operation="hit").inc()
            logger.info(f"[{request_id}] Cache HIT")
            cached_response["headers"]["X-Cache"] = "HIT"
            return StreamingResponse(
                iter([cached_response["content"]]),
                status_code=cached_response["status"],
                headers=cached_response["headers"]
            )
        cache_counter.labels(operation="miss").inc()

    # Prepare headers
    base_ua = MOBILE_UA if ua == "mobile" else DESKTOP_UA
    custom_ua = f"{CUSTOM_USER_AGENT} ({base_ua})" if CUSTOM_USER_AGENT != "AzureProxyService/1.0" else base_ua
    headers = {
        "User-Agent": custom_ua,
        "Accept": accept or "*/*",
        "Accept-Language": lang or "es-ES,es;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    # Add forwarded headers
    if forward_headers:
        header_list = [h.strip() for h in forward_headers.split(",")]
        forwarded = _get_forwarded_headers(request, header_list)
        headers.update(forwarded)

    # Get request body for POST requests
    body = None
    if method == "POST":
        body = await request.body()
        content_type = request.headers.get("content-type")
        if content_type:
            headers["Content-Type"] = content_type

    limits = httpx.Limits(max_connections=50, max_keepalive_connections=20)
    timeout_cfg = httpx.Timeout(connect=10.0, read=timeout, write=10.0, pool=10.0)

    async def attempt_fetch(target_url: str, http_method: str) -> httpx.Response:
        active_connections.inc()
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(timeout, read=timeout*2),
                follow_redirects=True,
                max_redirects=max_redirects,
                http2=False,  # Temporarily disable HTTP/2 due to h2 import issues
                verify=True
            ) as client:
                # Basic retry loop for transient 5xx / network errors
                last_exc = None
                for i in range(3):
                    try:
                        if http_method == "GET":
                            resp = await client.get(target_url)
                        elif http_method == "HEAD":
                            resp = await client.head(target_url)
                        elif http_method == "POST":
                            resp = await client.post(target_url, content=body)
                        
                        if resp.status_code >= 500:
                            await asyncio.sleep(0.5 * (i + 1))
                            continue
                        return resp
                    except (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError) as e:
                        last_exc = e
                        await asyncio.sleep(0.5 * (i + 1))
                if last_exc:
                    raise last_exc
                return resp  # type: ignore
        finally:
            active_connections.dec()

    # Try primary URL
    try:
        upstream = await attempt_fetch(url, method)
    except Exception as e:
        request_counter.labels(method=method, status="error").inc()
        logger.error(f"[{request_id}] Upstream error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=502, detail=f"Upstream error: {type(e).__name__}: {e}")

    # Enhanced AMP handling
    if try_amp and upstream.status_code in (403, 404) and method == "GET":
        amp_url = None
        
        # Try /amp path
        if parsed.path.endswith("/"):
            amp_url = urlunparse(parsed._replace(path=parsed.path + "amp"))
        else:
            amp_url = urlunparse(parsed._replace(path=parsed.path + "/amp"))
        
        try:
            upstream2 = await attempt_fetch(amp_url, method)
            if upstream2.status_code < 400:
                upstream = upstream2
                logger.info(f"[{request_id}] AMP variant found at {amp_url}")
        except Exception:
            pass
        
        # Try ?output=amp parameter
        if upstream.status_code >= 400:
            query_params = parse_qsl(parsed.query)
            query_params.append(("output", "amp"))
            new_query = urlencode(query_params)
            amp_url = urlunparse(parsed._replace(query=new_query))
            
            try:
                upstream3 = await attempt_fetch(amp_url, method)
                if upstream3.status_code < 400:
                    upstream = upstream3
                    logger.info(f"[{request_id}] AMP variant found with ?output=amp")
            except Exception:
                pass

    # Process response
    status_code = upstream.status_code
    resp_headers = _pick_headers_for_response(_clean_hop_by_hop(dict(upstream.headers)))
    
    # Remove content-encoding headers to avoid double-encoding issues
    # httpx automatically decompresses, so we shouldn't forward compression headers
    resp_headers.pop("content-encoding", None)
    resp_headers.pop("content-length", None)  # Let FastAPI calculate the correct length
    
    # Add Content-Disposition for PDFs and images
    content_type = resp_headers.get("content-type", "").lower()
    if ("pdf" in content_type or content_type.startswith("image/")) and "content-disposition" not in resp_headers:
        filename = _get_filename_from_path(parsed.path)
        resp_headers["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Add cache header
    resp_headers["X-Cache"] = "MISS"
    
    # Metrics and logging
    request_counter.labels(method=method, status=str(status_code)).inc()
    duration = time.time() - start_time
    request_duration.observe(duration)
    
    content_length = resp_headers.get("content-length", "unknown")
    
    # Check response size limit
    if content_length != "unknown":
        try:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > MAX_RESPONSE_SIZE_MB:
                raise HTTPException(
                    status_code=413, 
                    detail=f"Response too large: {size_mb:.1f}MB (max: {MAX_RESPONSE_SIZE_MB}MB)"
                )
        except ValueError:
            pass  # Ignore invalid content-length values
    
    logger.info(f"[{request_id}] {status_code} - {content_length} bytes in {duration:.2f}s")

    # Cache successful GET responses
    if method == "GET" and cache_key and status_code in (200, 304):
        try:
            # For small responses, cache the content
            # httpx automatically decompresses content, so we work with raw decompressed bytes
            content = await upstream.aread()
            if len(content) < 1024 * 1024:  # 1MB limit for caching
                cached_data = {
                    "status": status_code,
                    "headers": dict(resp_headers),
                    "content": content,
                }
                response_cache[cache_key] = cached_data
                cache_counter.labels(operation="store").inc()
                
                # Return cached content
                return StreamingResponse(
                    iter([content]),
                    status_code=status_code,
                    headers=resp_headers
                )
        except Exception as e:
            logger.warning(f"[{request_id}] Failed to cache response: {e}")

    # Stream the body for non-cached responses
    # httpx handles decompression automatically
    async def body_iter():
        async for chunk in upstream.aiter_bytes():
            yield chunk

    return StreamingResponse(body_iter(), status_code=status_code, headers=resp_headers)
