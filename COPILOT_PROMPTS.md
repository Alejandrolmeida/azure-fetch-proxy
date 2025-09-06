
# GitHub Copilot Prompts for Enhancing the Azure FastAPI Proxy

Paste these into a new file or directly into the editor to guide Copilot. Adjust to your style.

## 1) Add API key auth
> In `main.py`, add simple API key auth: read an environment variable `API_KEY`. If set, require header `x-api-key` to match. Return 401 otherwise.

## 2) Add HEAD/POST forwarding
> Extend `/fetch` to support HEAD and POST: detect method via `method` query param (`GET` default). For POST, accept raw body and forward `Content-Type`.

## 3) Add basic response caching
> Implement in-memory LRU cache (capacity 128) keyed by (method,url,ua,accept,lang). Cache 200/304 for up to 120 seconds. Include `X-Cache: HIT|MISS` header.

## 4) Support forwarding selected headers
> Allow passing selected request headers (e.g., `If-None-Match`, `If-Modified-Since`) via query or by mirroring from incoming request, with a safelist to avoid abuse.

## 5) Blocklist & allowlist
> Add optional allowlist of domains via env var `ALLOWED_HOSTS` (comma-separated). If set, only allow those hostnames. Also add `BLOCKED_HOSTS` to deny specific hosts.

## 6) IPv6 tightening
> Update SSRF check to handle IPv6-mapped IPv4 and future-proof special ranges; add tests for reserved/unique-local IPv6.

## 7) Better AMP heuristics
> If `try_amp=true`, also try appending `?output=amp` and checking for `<link rel="amphtml">` in upstream HTML to follow that URL if present.

## 8) PDF & image Content-Disposition
> If upstream `Content-Type` is PDF or an image and there's no `Content-Disposition`, add one using the last path segment as filename.

## 9) Observability
> Add structured logging (uvicorn logging config + loguru). Log request id, target URL, status, bytes, and latency. Include an `/metrics` endpoint compatible with Prometheus.

## 10) Unit tests (pytest)
> Create `tests/test_ssrf.py` and `tests/test_fetch.py` using `httpx.AsyncClient` + `asgi-lifespan`. Test SSRF protections and happy-path streaming.
