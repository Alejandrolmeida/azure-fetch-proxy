# Development Setup

## Prerequisites
- Python 3.11+
- Docker
- Azure CLI (for deployment)

## Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alejandrolmeida/azure-fetch-proxy.git
   cd azure-fetch-proxy
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the server:**
   ```bash
   python secure_proxy.py
   ```

6. **Test the proxy:**
   ```bash
   curl "http://localhost:8000/health"
   curl "http://localhost:8000/fetch?url=https://httpbin.org/headers&api_key=your-api-key"
   ```

## Testing

Run tests with pytest:
```bash
python -m pytest tests/ -v
```

## Docker Development

1. **Build image:**
   ```bash
   docker build -t azure-fetch-proxy .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 -e API_KEY="your-api-key" azure-fetch-proxy
   ```

## Code Style

This project follows PEP 8 and uses:
- Type hints where applicable
- Docstrings for all functions
- Comments for complex logic
- Consistent naming conventions

## Security Considerations

- Always use strong API keys in production
- Never commit sensitive information to git
- Review rate limiting settings for your use case
- Monitor logs for suspicious activity

## Deployment

See `deploy_container.sh` for automated Azure deployment or follow the manual steps in the main README.
