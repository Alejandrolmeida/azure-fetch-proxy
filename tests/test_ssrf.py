import pytest
from main import _is_private_ip


class TestSSRFProtection:
    """Test SSRF protection functionality"""
    
    def test_private_ipv4_addresses(self):
        """Test that private IPv4 addresses are blocked"""
        private_ips = [
            "192.168.1.1",
            "10.0.0.1", 
            "172.16.0.1",
            "127.0.0.1",
            "169.254.169.254",  # AWS metadata
        ]
        
        for ip in private_ips:
            assert _is_private_ip(ip), f"IP {ip} should be blocked"
    
    def test_public_ipv4_addresses(self):
        """Test that public IPv4 addresses are allowed"""
        public_ips = [
            "8.8.8.8",
            "1.1.1.1",
            "208.67.222.222",
            "151.101.193.140",  # Reddit
        ]
        
        for ip in public_ips:
            assert not _is_private_ip(ip), f"IP {ip} should be allowed"
    
    def test_private_ipv6_addresses(self):
        """Test that private IPv6 addresses are blocked"""
        private_ipv6 = [
            "::1",  # loopback
            "fe80::1",  # link-local
            "fc00::1",  # unique local
            "fd00::1",  # unique local
            "ff02::1",  # multicast
        ]
        
        for ip in private_ipv6:
            assert _is_private_ip(ip), f"IPv6 {ip} should be blocked"
    
    def test_ipv6_mapped_ipv4(self):
        """Test IPv6-mapped IPv4 addresses"""
        # IPv6-mapped private IPv4
        assert _is_private_ip("::ffff:192.168.1.1"), "IPv6-mapped private IP should be blocked"
        assert _is_private_ip("::ffff:127.0.0.1"), "IPv6-mapped loopback should be blocked"
        
        # IPv6-mapped public IPv4 (these should be allowed)
        assert not _is_private_ip("::ffff:8.8.8.8"), "IPv6-mapped public IP should be allowed"
    
    def test_public_ipv6_addresses(self):
        """Test that public IPv6 addresses are allowed"""
        public_ipv6 = [
            "2001:4860:4860::8888",  # Google DNS
            "2606:4700:4700::1111",  # Cloudflare DNS
        ]
        
        for ip in public_ipv6:
            assert not _is_private_ip(ip), f"IPv6 {ip} should be allowed"
    
    def test_invalid_ip_addresses(self):
        """Test that invalid IP addresses are blocked"""
        invalid_ips = [
            "not.an.ip",
            "300.300.300.300",
            "192.168.1",
            "",
            "::gggg",
        ]
        
        for ip in invalid_ips:
            assert _is_private_ip(ip), f"Invalid IP {ip} should be blocked"
