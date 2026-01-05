#!/usr/bin/env python3
"""
EnMAP Bounds Viewer Server
Serves the web UI and provides API endpoints for EnMAP queries.
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path
import requests

try:
    from pystac_client import Client
except ImportError:
    print("Warning: pystac-client not installed. Install with: pip install pystac-client")
    Client = None


app = Flask(__name__)
CORS(app)

# Configuration
STAC_URL = "https://geoservice.dlr.de/eoc/ogc/stac/v1/"
COLLECTION = "ENMAP_HSI_L2A"


class EnMAPQuery:
    """Query EnMAP data from DLR EOC STAC API"""
    
    def __init__(self):
        if Client is None:
            raise ImportError("pystac-client is not installed")
        self.catalog = Client.open(STAC_URL)
    
    def query_bounds(self, bbox, datetime_range="2024-01-01/2026-01-05", max_items=100):
        """Query EnMAP data for given bounds"""
        try:
            search = self.catalog.search(
                collections=[COLLECTION],
                bbox=bbox,
                datetime=datetime_range,
                max_items=max_items
            )
            
            items = search.item_collection()
            return list(items), None
        except Exception as e:
            return None, str(e)


@app.route('/')
def index():
    """Serve the main HTML file"""
    try:
        html_file = Path(__file__).parent / 'csv_bounds_viewer.html'
        if not html_file.exists():
            return jsonify({'error': 'HTML file not found'}), 404
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/query-enmap', methods=['POST'])
def query_enmap():
    """
    API endpoint for EnMAP queries
    Expected JSON: {
        "bounds": [min_lon, min_lat, max_lon, max_lat],
        "datetime": "start_date/end_date",
        "max_items": 100
    }
    """
    try:
        data = request.get_json()
        bounds = data.get('bounds')
        datetime_range = data.get('datetime', '2024-01-01/2026-01-05')
        max_items = data.get('max_items', 100)
        
        if not bounds or len(bounds) != 4:
            return jsonify({'error': 'Invalid bounds format'}), 400
        
        if Client is None:
            return jsonify({'error': 'pystac-client not installed'}), 500
        
        # Query EnMAP
        query = EnMAPQuery()
        items, error = query.query_bounds(bounds, datetime_range, max_items)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Format results
        results = []
        for item in items:
            # Extract asset URLs safely
            data_url = None
            preview_url = None
            
            # Parse scene ID to construct direct download URLs
            # Format: ENMAP01-____L2A-DT{DT_NUM}_{DATE}T{TIME}Z_{VERSION}_V{PROD_VERSION}_{TIMESTAMP}Z
            scene_id = item.id
            try:
                # Extract date from scene ID (format: YYYYMMDD)
                date_str = scene_id.split('_')[1]  # e.g., "20260103"
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                
                # Extract DT number
                dt_part = scene_id.split('-')[2]  # e.g., "DT0000173759"
                
                # Extract version number from scene ID
                version_num = scene_id.split('_')[3]  # e.g., "003"
                
                # Extract product version
                prod_version = scene_id.split('_')[4]  # e.g., "V010505"
                
                # Construct download URL (for VNIR data)
                data_url = f"https://download.geoservice.dlr.de/ENMAP/files/L2A/{year}/{month}/{day}/{dt_part}/{version_num}/{scene_id}-QL_VNIR_COG.zip"
                
                # Construct preview URL (quicklook thumbnail)
                preview_url = f"https://download.geoservice.dlr.de/ENMAP/files/L2A/{year}/{month}/{day}/{dt_part}/{version_num}/{scene_id}-QL_VNIR_COG_thumbnail.jpg"
            except (IndexError, ValueError):
                # Fallback if parsing fails
                data_url = f"https://geoservice.dlr.de/eoc/oseo/download?parentIdentifier=ENMAP_HSI_L2A&uid={scene_id}"
                preview_url = f"https://geoservice.dlr.de/eoc/oseo/quicklook?parentIdentifier=ENMAP_HSI_L2A&uid={scene_id}"
            
            # Also try to get assets from STAC metadata if available
            data_candidates = ['data', 'VNIR', 'SWIR', 'product', 'ql_VNIR_COG', 'ql_SWIR_COG']
            for asset_name in data_candidates:
                if asset_name in item.assets:
                    try:
                        asset_url = item.assets[asset_name].href
                        if asset_url:
                            data_url = asset_url
                            break
                    except (AttributeError, KeyError):
                        continue
            
            preview_candidates = ['thumbnail', 'visual', 'preview', 'quicklook']
            for asset_name in preview_candidates:
                if asset_name in item.assets:
                    try:
                        asset_url = item.assets[asset_name].href
                        if asset_url:
                            preview_url = asset_url
                            break
                    except (AttributeError, KeyError):
                        continue
            
            # Compile all available assets for debugging
            available_assets = list(item.assets.keys())
            
            result = {
                'id': item.id,
                'datetime': str(item.datetime),
                'cloud_cover': item.properties.get('eo:cloud_cover', None),
                'data_url': data_url,
                'preview_url': preview_url,
                'available_assets': available_assets,  # Debug info
            }
            results.append(result)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'items': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/preview', methods=['GET'])
def preview_proxy():
    """
    Proxy endpoint for preview images
    Fetches images from external URLs and serves them with CORS headers
    Query params: url (the image URL to fetch)
    """
    try:
        preview_url = request.args.get('url')
        if not preview_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Fetch the image from the external URL
        response = requests.get(preview_url, timeout=10, verify=False)
        
        if response.status_code != 200:
            return jsonify({'error': f'Failed to fetch preview: {response.status_code}'}), response.status_code
        
        # Determine correct Content-Type
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        
        # Fix incorrect MIME types from DLR server (e.g., application/octet-stream, .dat files)
        if 'octet-stream' in content_type or 'dat' in content_type.lower():
            content_type = 'image/jpeg'  # DLR quicklooks are JPEG format
        
        # Return the image with proper CORS headers using Response
        return Response(
            response.content,
            status=200,
            headers={
                'Content-Type': content_type,
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'max-age=86400',
                'Content-Length': len(response.content),
                'Content-Disposition': 'inline'  # Force inline display, not download
            }
        )
    
    except requests.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except Exception as e:
        return jsonify({'error': f'Proxy error: {str(e)}'}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Check server and API status"""
    return jsonify({
        'status': 'ok',
        'stac_api': STAC_URL,
        'collection': COLLECTION,
        'pystac_client_available': Client is not None
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🌍 EnMAP Bounds Viewer Server")
    print("=" * 60)
    print()
    print("📍 Server: http://localhost:8080")
    print("🔗 STAC API: " + STAC_URL)
    print("📦 Collection: " + COLLECTION)
    print()
    
    if Client is None:
        print("⚠️  Warning: pystac-client not installed")
        print("   Install with: pip install pystac-client")
        print("   EnMAP queries will not be available")
    else:
        print("✅ pystac-client is installed")
    
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='localhost', port=8080)
