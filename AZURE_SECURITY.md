# Azure Security Hardening Guide

## Pre-deployment Security Checklist

### 🔐 MANDATORY Security Settings

1. **Enable API Key Authentication**
   ```bash
   export API_KEY="your-super-secure-random-key-here"
   ```

2. **Configure Host Allowlist** (Whitelist only trusted domains)
   ```bash
   export ALLOWED_HOSTS="httpbin.org,jsonplaceholder.typicode.com,api.github.com"
   ```

3. **Set Blocked Hosts** (Block known problematic domains)
   ```bash
   export BLOCKED_HOSTS="localhost,127.0.0.1,metadata.google.internal"
   ```

### 🚧 Additional Rate Limiting

Add these environment variables:
```bash
export MAX_REQUESTS_PER_MINUTE=60
export MAX_REQUESTS_PER_HOUR=1000
export MAX_RESPONSE_SIZE_MB=10
```

### 🛡️ Azure-specific Security

1. **Enable Azure Application Insights** for monitoring
2. **Configure Azure Web Application Firewall**
3. **Set up Azure Key Vault** for API keys
4. **Enable Azure DDoS Protection**
5. **Configure custom domain** with SSL certificate

### 📊 Monitoring & Alerting

Set up alerts for:
- High bandwidth usage
- Unusual request patterns
- Error rate spikes
- Blocked SSRF attempts

### 🚨 Legal Considerations

- Add Terms of Service
- Implement usage logging
- Consider content filtering
- Review Azure acceptable use policy
- Consider GDPR compliance if serving EU users

## Recommended Azure Configuration

```yaml
# azure-webapp-config.yml
runtime:
  python_version: "3.12"
  
app_settings:
  - name: "API_KEY"
    value: "@Microsoft.KeyVault(SecretUri=https://your-vault.vault.azure.net/secrets/api-key/)"
  - name: "ALLOWED_HOSTS"
    value: "your-trusted-domains.com"
  - name: "LOG_LEVEL"
    value: "INFO"
    
scaling:
  min_instances: 1
  max_instances: 3
  
monitoring:
  application_insights: true
  log_analytics: true
```

## Cost Optimization

- Set bandwidth limits
- Implement response caching
- Monitor Azure costs daily
- Consider Azure Functions for sporadic usage

## Emergency Response Plan

1. **Immediate shutdown**: Scale to 0 instances
2. **Block malicious IPs**: Update Azure NSG rules
3. **Review logs**: Check Application Insights
4. **Contact Azure support**: If under attack
