# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-09-09

### Added
- 🇪🇸 **Spanish Geolocation Simulation**: Complete Spanish ISP and location simulation
- **Realistic Spanish Headers**: X-Spanish-Region, X-Client-Location, X-ISP headers
- **Multi-ISP Rotation**: Telefónica, Orange, Vodafone, Euskaltel, Jazztel simulation
- **Regional Coverage**: Madrid, Barcelona, Valencia, Sevilla, Bilbao locations
- **Anti-Bot Features**: Realistic User-Agent and Accept-Language headers for Spain
- **Health Monitoring**: `/health` endpoint for container health checks
- **Azure Container Deployment**: Complete containerization with Azure Container Instances
- **Front Door Integration**: SSL termination and custom domain support
- **Security Enhancements**: API key validation and rate limiting

### Changed
- **Architecture Migration**: From FastAPI to BaseHTTPServer for better container compatibility
- **Deployment Strategy**: Moved to Azure Container Instances with automated deployment
- **Request Processing**: Enhanced with Spanish geolocation headers injection
- **Error Handling**: Improved error responses and logging
- **Configuration**: Environment-based configuration with .env support

### Fixed
- **Container Compatibility**: Resolved uvicorn compatibility issues in Azure containers
- **Header Injection**: Fixed Spanish header addition for all outbound requests
- **Rate Limiting**: Corrected per-IP rate limiting implementation
- **SSL Handling**: Improved HTTPS request processing

### Security
- **API Key Protection**: Enhanced API key validation system
- **Rate Limiting**: 30 requests per minute per IP protection
- **SSRF Protection**: Enhanced security against Server-Side Request Forgery
- **Input Validation**: Improved URL and parameter validation

## [1.0.0] - 2024-08-15

### Added
- Initial release with basic HTTP proxy functionality
- FastAPI-based implementation
- Basic rate limiting
- Docker container support
- Azure deployment scripts

---

## Deployment Information

### Current Production Environment
- **URL**: https://proxy.azurebrains.com
- **Health Check**: https://proxy.azurebrains.com/health
- **Azure Container**: azurebrains-proxy (West Europe)
- **Registry**: fetchproxyregistry1757181743.azurecr.io
- **Resource Group**: rg-fetch-proxy

### Usage
```bash
curl "https://proxy.azurebrains.com/fetch?url=https://httpbin.org/headers&api_key=YOUR_API_KEY"
```

The response will include Spanish geolocation headers:
- `X-Spanish-Region`: Regional location in Spain
- `X-Client-Location`: City and country 
- `X-Isp`: Spanish ISP information
