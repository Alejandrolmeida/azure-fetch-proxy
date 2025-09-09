#!/usr/bin/env python3
"""
AzureBrains Secure HTTP Proxy with Spanish Geolocation Simulation

This proxy server simulates Spanish geolocation by adding realistic headers
for Spanish ISPs and regions. It's designed to bypass bot detection while
maintaining ethical usage standards.

Features:
- Spanish ISP rotation (Telefónica, Orange, Vodafone, Euskaltel, Jazztel)
- Regional Spanish locations (Madrid, Barcelona, Valencia, Sevilla, Bilbao)
- API key authentication and rate limiting
- Health monitoring endpoint
- Production-ready logging and error handling

Usage:
    python secure_proxy.py
    
    Then make requests to:
    http://localhost:8000/fetch?url=https://example.com&api_key=YOUR_API_KEY

Environment Variables:
    API_KEY: Required API key for authentication
    SERVER_PORT: Server port (default: 8000)
    MAX_REQUESTS_PER_MINUTE: Rate limit per IP (default: 30)

Author: AzureBrains Team
Version: 2.0.0
"""

import socket
import threading
import urllib.parse
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import ssl
import json
import os
import hashlib
import time
import random
from datetime import datetime, timedelta
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security Configuration from .env
API_KEY = os.getenv('API_KEY', 'CHANGE-THIS-API-KEY-IN-PRODUCTION')
MAX_REQUESTS_PER_MINUTE = 30
RATE_LIMIT_STORAGE = {}

class SecurityManager:
    @staticmethod
    def validate_api_key(provided_key):
        """Validate API key"""
        return provided_key == API_KEY
    
    @staticmethod
    def is_domain_allowed(url):
        """Check if domain is allowed - All domains allowed for flexibility"""
        return True
    
    @staticmethod
    def check_rate_limit(client_ip):
        """Check rate limiting per IP"""
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old entries
        if client_ip in RATE_LIMIT_STORAGE:
            RATE_LIMIT_STORAGE[client_ip] = [
                req_time for req_time in RATE_LIMIT_STORAGE[client_ip] 
                if req_time > minute_ago
            ]
        else:
            RATE_LIMIT_STORAGE[client_ip] = []
        
        # Check if under limit
        if len(RATE_LIMIT_STORAGE[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
            return False
        
        # Add current request
        RATE_LIMIT_STORAGE[client_ip].append(current_time)
        return True
    
    @staticmethod
    def get_realistic_headers(target_url):
        """Generate realistic headers with Spanish geolocation simulation"""
        
        # Spanish ISP domains and regions for realistic geolocation
        spanish_regions = [
            {'region': 'Madrid', 'isp': 'telefonica.net', 'city': 'Madrid'},
            {'region': 'Cataluña', 'isp': 'orange.es', 'city': 'Barcelona'},
            {'region': 'Valencia', 'isp': 'vodafone.es', 'city': 'Valencia'},
            {'region': 'Andalucía', 'isp': 'jazztel.es', 'city': 'Sevilla'},
            {'region': 'País Vasco', 'isp': 'euskaltel.es', 'city': 'Bilbao'}
        ]
        
        # Select random Spanish region
        spanish_region = random.choice(spanish_regions)
        
        # Parse domain for customization
        parsed = urllib.parse.urlparse(target_url)
        domain = parsed.netloc.lower()
        
        # Base realistic headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8,en-US;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-CH-UA': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            # Spanish geolocation simulation
            'X-Forwarded-Region': spanish_region['region'],
            'X-Client-Location': f"{spanish_region['city']}, Spain",
            'X-ISP': spanish_region['isp'],
            'CF-IPCountry': 'ES',
            'X-Timezone': 'Europe/Madrid',
        }
        
        # Domain-specific customizations
        if 'amazon' in domain:
            headers.update({
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                'Referer': 'https://www.google.es/',
                'X-Amzn-Trace-Id': f'Root=1-{int(time.time()):x}-{random.randint(100000000000, 999999999999):x}',
                'X-Client-Region': spanish_region['region']
            })
        elif 'google' in domain:
            headers.update({
                'Accept-Encoding': '',  # No compression for Google
                'X-Forwarded-For': f'217.{random.randint(100,200)}.{random.randint(1,254)}.{random.randint(1,254)}',
            })
        
        return headers
    
    @staticmethod
    def simulate_human_delay():
        """Add realistic delay to simulate human browsing"""
        delay = random.uniform(0.5, 2.5)
        time.sleep(delay)

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle HTTP GET requests with security checks"""
        try:
            client_ip = self.client_address[0]
            
            # Rate limiting check
            if not SecurityManager.check_rate_limit(client_ip):
                self.send_error(429, 'Rate limit exceeded. Max 30 requests per minute.')
                return
            
            parsed_path = urllib.parse.urlparse(self.path)
            
            if parsed_path.path == '/fetch':
                self.handle_fetch_request(parsed_path, client_ip)
            elif parsed_path.path == '/':
                self.handle_home_page()
            elif parsed_path.path == '/health':
                self.handle_health_check()
            else:
                self.send_error(404, 'Endpoint not found. Use /fetch?url=<target_url>&api_key=<your_key>')
                
        except Exception as e:
            print(f"[ERROR] {e}")
            self.send_error(500, f'Server error: {e}')
    
    def handle_home_page(self):
        """Show usage instructions"""
        response_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Secure URL Resolver Proxy for ChatGPT</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .example {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔐 Secure URL Resolver Proxy for ChatGPT</h1>
                <p>This proxy allows ChatGPT to access websites with Spanish geolocation simulation and anti-bot detection.</p>
                
                <h2>🌐 Usage with ChatGPT:</h2>
                <div class="example">
                    <code>http://localhost:8000/fetch?url=https://example.com&api_key=your-api-key</code>
                </div>
                
                <h2>🛡️ Security Features:</h2>
                <ul>
                    <li>✅ API Key Authentication</li>
                    <li>✅ Rate Limiting (30 req/min per IP)</li>
                    <li>✅ Spanish Location Simulation</li>
                    <li>✅ Anti-Bot Headers</li>
                    <li>✅ Human Behavior Simulation</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(response_html.encode('utf-8'))
    
    def handle_fetch_request(self, parsed_path, client_ip):
        """Fetch content from target URL with security validation"""
        query_params = urllib.parse.parse_qs(parsed_path.query)
        target_url = query_params.get('url', [None])[0]
        provided_api_key = query_params.get('api_key', [None])[0]
        
        # Security validations
        if not provided_api_key:
            self.send_error(401, 'Missing API key.')
            return
            
        if not SecurityManager.validate_api_key(provided_api_key):
            print(f"[SECURITY] Invalid API key from {client_ip}")
            self.send_error(403, 'Invalid API key.')
            return
        
        if not target_url:
            self.send_error(400, 'Missing required parameter: url')
            return
        
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url
        
        if not SecurityManager.is_domain_allowed(target_url):
            self.send_error(403, 'Domain not allowed')
            return
        
        print(f"[FETCH] {client_ip} -> {target_url}")
        
        # Add human-like delay
        SecurityManager.simulate_human_delay()
        
        try:
            # Get realistic headers for Spanish geolocation
            headers = SecurityManager.get_realistic_headers(target_url)
            
            session = requests.Session()
            session.headers.update(headers)
            
            response = session.get(
                target_url,
                timeout=(10, 30),
                allow_redirects=True,
                verify=False,
                stream=False,
                cookies={
                    'session_id': f'sess_{random.randint(100000, 999999)}',
                    'preferred_language': 'es-ES',
                    'timezone': 'Europe/Madrid'
                }
            )
            
            print(f"[FETCH] {response.status_code} - {len(response.content)} bytes")
            
            # Send successful response
            self.send_response(response.status_code)
            
            content_type = response.headers.get('Content-Type', 'text/html; charset=utf-8')
            if 'text/html' in content_type and 'charset' not in content_type:
                content_type += '; charset=utf-8'
            
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('X-Proxy-Source', 'SecureProxy')
            self.send_header('X-Requested-URL', target_url)
            self.send_header('X-Spanish-Region', headers.get('X-Forwarded-Region', 'Unknown'))
            
            self.end_headers()
            
            # Send content with proper encoding
            try:
                if 'text/' in content_type or 'application/json' in content_type:
                    try:
                        decoded_content = response.content.decode(response.encoding or 'utf-8')
                        self.wfile.write(decoded_content.encode('utf-8'))
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        self.wfile.write(response.content)
                else:
                    self.wfile.write(response.content)
            except Exception as encoding_error:
                print(f"[ENCODING ERROR] {encoding_error}")
                self.wfile.write(response.content)
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error fetching {target_url}: {e}")
            self.send_error(500, f'Error fetching URL: {e}')
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            self.send_error(500, f'Unexpected error: {e}')
    
    def handle_health_check(self):
        """Health check endpoint"""
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0-secure',
            'features': {
                'api_key_auth': True,
                'rate_limiting': True,
                'spanish_geolocation': True,
                'anti_bot_headers': True,
                'human_delay_simulation': True
            }
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(health_data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass

class ThreadedHTTPServer(HTTPServer):
    """Handle requests in separate threads"""
    def process_request(self, request, client_address):
        thread = threading.Thread(target=self.process_request_thread,
                                 args=(request, client_address))
        thread.daemon = True
        thread.start()
    
    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

def main():
    # Configuration for both local and Azure deployment
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = int(os.getenv('PORT', 8000))  # Use Azure's assigned port or default
    
    print(f"""
🔐 Secure URL Resolver Proxy started on {HOST}:{PORT}

📖 INSTRUCTIONS FOR CHATGPT:
Use this URL to access websites:
http://{HOST}:{PORT}/fetch?url=<WEBSITE>&api_key=<YOUR_API_KEY>

🛡️ SECURITY FEATURES ACTIVE:
✅ API Key authentication (set in .env file)
✅ Rate limiting: {MAX_REQUESTS_PER_MINUTE} requests/minute per IP
✅ Spanish geolocation simulation
✅ Anti-bot headers and realistic browser simulation
✅ Human behavior delays (0.5-2.5s)

🔍 Web interface: http://{HOST}:{PORT}
🩺 Health check: http://{HOST}:{PORT}/health

⚠️  Remember to set API_KEY in .env file for production!
""")
    
    # Start the proxy server
    server = ThreadedHTTPServer((HOST, PORT), ProxyHTTPRequestHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Secure Proxy stopped")
        server.shutdown()

if __name__ == '__main__':
    main()
