# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email security issues to: [your-email@domain.com]
3. Include a detailed description of the vulnerability
4. Provide steps to reproduce if possible
5. Include any relevant logs or screenshots

We will respond to security reports within 48 hours and provide regular updates on the progress.

## Security Features

### Authentication & Authorization
- **API Key Validation**: All requests require valid API key authentication
- **Rate Limiting**: 30 requests per minute per IP address to prevent abuse
- **Input Validation**: All URLs and parameters are validated before processing

### Network Security
- **SSRF Protection**: Blocks requests to private networks and cloud metadata endpoints
- **Request Filtering**: Validates and sanitizes all outbound requests
- **Timeout Protection**: Configurable timeouts prevent hanging connections

### Data Protection
- **No Data Persistence**: Proxy doesn't store or log sensitive request data
- **Memory Management**: Efficient memory usage with automatic cleanup
- **Secure Headers**: Adds security headers while maintaining Spanish geolocation simulation

### Infrastructure Security
- **Container Isolation**: Runs in isolated Docker containers
- **Minimal Dependencies**: Uses only essential Python packages
- **Regular Updates**: Dependencies are regularly updated for security patches

## Security Best Practices

### For Users
1. **Use Strong API Keys**: Generate cryptographically secure API keys
2. **Rotate Keys Regularly**: Change API keys periodically
3. **Monitor Usage**: Keep track of your proxy usage patterns
4. **Secure Storage**: Never commit API keys to version control
5. **Network Security**: Use HTTPS when available (proxy.azurebrains.com)

### For Administrators
1. **Environment Security**: Secure your .env files and environment variables
2. **Access Control**: Limit who has access to API keys and deployment credentials
3. **Monitoring**: Set up alerts for unusual usage patterns
4. **Updates**: Keep the proxy software and dependencies updated
5. **Backup**: Maintain secure backups of configuration

## Security Considerations

### Geolocation Simulation
- The Spanish geolocation simulation is for legitimate testing purposes only
- Headers are added transparently and don't hide the proxy's identity completely
- This tool should not be used to circumvent geographic restrictions illegally

### Responsible Use
- Respect target websites' robots.txt and Terms of Service
- Don't use for bypassing paywalls or authentication systems
- Ensure compliance with local laws and regulations
- Use reasonable rate limits to avoid overloading target servers

## Security Updates

We regularly update this project to address security vulnerabilities:
- Dependencies are reviewed monthly for security updates
- Security patches are applied promptly
- Breaking changes are documented in the CHANGELOG.md

## Contact

For security-related questions or concerns:
- Create a GitHub issue (for non-sensitive matters)
- Email: [your-email@domain.com] (for security vulnerabilities)
- Review our code: All code is open source and available for audit
