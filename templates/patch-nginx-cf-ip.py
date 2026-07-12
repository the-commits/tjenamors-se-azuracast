#!/usr/bin/env python3
"""Patch nginx.conf to use CF-Connecting-IP in hls_json log format.

When Cloudflare is enabled, the X-Forwarded-For header contains
comma-separated IPs (real_ip, cf_edge_ip). The HLS listener parser
in AzuraCast prefers ip_xff over ip, causing two IPs to be stored.
Switching to CF-Connecting-IP gives a single clean real IP.
"""
import pathlib

NGINX_CONF = pathlib.Path("/etc/nginx/nginx.conf")

OLD = '"ip_xff": "$http_x_forwarded_for"'
NEW = '"ip_xff": "$http_cf_connecting_ip"'

text = NGINX_CONF.read_text()
if OLD in text:
    NGINX_CONF.write_text(text.replace(OLD, NEW))
    print("Patched hls_json log format: ip_xff now uses CF-Connecting-IP")
elif NEW in text:
    print("Already patched")
else:
    print("WARNING: Could not find ip_xff log format directive")
