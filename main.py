#!/usr/bin/env python3
"""
Azure App Service entry point for the secure proxy
This file is required by Azure App Service
"""

# Import our secure proxy
from secure_proxy import main

if __name__ == '__main__':
    # Start the secure proxy server
    main()