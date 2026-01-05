#!/bin/bash
# Run the EnMAP Bounds Viewer Flask Server

cd "$(dirname "$0")"
echo "Starting EnMAP Bounds Viewer Server..."
echo "=================================="
echo "📍 Web UI: http://localhost:5000"
echo "=================================="
echo ""
python3 server.py
