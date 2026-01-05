#!/usr/bin/env python3
"""
EnMAP Bounds Viewer - Complete Setup Guide

This file provides step-by-step instructions to run the integrated system.
"""

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║          EnMAP Bounds Viewer & Data Query - Setup Instructions           ║
╚══════════════════════════════════════════════════════════════════════════╝

📦 INSTALLATION
───────────────────────────────────────────────────────────────────────────

1. Install Python dependencies:
   
   $ pip install flask flask-cors pystac-client

   (Already installed if you see this message)


🚀 RUNNING THE SERVER
───────────────────────────────────────────────────────────────────────────

Start the Flask server:

   $ python3 server.py
   
   or

   $ chmod +x run_server.sh && ./run_server.sh

Expected output:
   ============================================================
   🌍 EnMAP Bounds Viewer Server
   ============================================================
   
   📍 Server: http://localhost:5000
   🔗 STAC API: https://geoservice.dlr.de/eoc/ogc/stac/v1/
   📦 Collection: ENMAP_HSI_L2A
   
   ✅ pystac-client is installed
   
    * Running on http://localhost:5000


🌐 USING THE WEB INTERFACE
───────────────────────────────────────────────────────────────────────────

1. Open browser: http://localhost:5000

2. **Drawing AOI (Area of Interest)**:
   - Click the square tool (⬜) in the left panel
   - First click: Place center marker (red dot)
   - Second click: Create rectangle
   - Bounds auto-populate in the CSV area

3. **Loading Existing Bounds**:
   - Paste CSV data in the textarea
   - Click "Load Bounds" button
   - Rectangles appear on the map

4. **Querying EnMAP Data**:
   - Set date range (Start Date, End Date)
   - Set Max Items (50-500)
   - Click "Query EnMAP" button
   - Results show in table below

5. **Exporting Data**:
   - Click "Export CSV" to download bounds
   - Click "Export Results" to download query results as JSON


📋 CSV FORMAT
───────────────────────────────────────────────────────────────────────────

Input/Output format:
   granule_id,north_lat,south_lat,west_lon,east_lon
   my_aoi,45.5,45.0,-122.5,-122.0

Example:
   granule_id,north_lat,south_lat,west_lon,east_lon
   milan_italy,45.43360417128909,45.296389684940266,8.993144532517837,9.141464063463546


🔧 TROUBLESHOOTING
───────────────────────────────────────────────────────────────────────────

Port 5000 already in use?
   $ lsof -i :5000
   $ kill -9 <PID>

Import errors (pystac-client, flask)?
   $ pip install flask flask-cors pystac-client

Map not loading?
   - Check internet connection
   - Clear browser cache (Ctrl+Shift+Del)
   - Check browser console (F12 → Console)

EnMAP queries return no results?
   - Try expanding date range
   - Check bounds are within EnMAP coverage (global, except poles)
   - Increase max_items parameter


📊 API ENDPOINT
───────────────────────────────────────────────────────────────────────────

POST http://localhost:5000/api/query-enmap

Request body:
{
  "bounds": [min_lon, min_lat, max_lon, max_lat],
  "datetime": "YYYY-MM-DD/YYYY-MM-DD",
  "max_items": 100
}

Example cURL:
   curl -X POST http://localhost:5000/api/query-enmap \\
     -H "Content-Type: application/json" \\
     -d '{
       "bounds": [8.9931, 45.2964, 9.1415, 45.4336],
       "datetime": "2024-01-01/2025-12-31",
       "max_items": 50
     }'


📁 FILE STRUCTURE
───────────────────────────────────────────────────────────────────────────

maps_bounds_viewer/
├── csv_bounds_viewer.html  ← Web UI (served by Flask)
├── server.py              ← Flask server with API
├── enmap_query.py         ← Legacy CLI script (optional)
├── run_server.sh          ← Startup script
├── example_bounds.csv     ← Sample data
└── README.md              ← Full documentation


🌟 FEATURES
───────────────────────────────────────────────────────────────────────────

✓ Interactive map with OpenStreetMap tiles
✓ Draw rectangle AOIs directly on map
✓ Load CSV bounds and visualize
✓ Query EnMAP satellite data availability
✓ View results in formatted table
✓ Export bounds and results (CSV/JSON)
✓ Calculate area, width, height, midpoint
✓ Real-time bounds information


💡 EXAMPLE WORKFLOW
───────────────────────────────────────────────────────────────────────────

1. Start server: python3 server.py
2. Open http://localhost:5000
3. Draw AOI on map (or paste CSV bounds)
4. Set date range: 2024-01-01 to 2025-12-31
5. Click "Query EnMAP"
6. Review satellite scene results
7. Export results for downstream analysis


❓ HELP & RESOURCES
───────────────────────────────────────────────────────────────────────────

- Full README: See README.md
- EnMAP Data: https://www.dlr.de/en/eoc/missions/enmap
- STAC API: https://geoservice.dlr.de/eoc/ogc/stac/v1/
- Leaflet.js: https://leafletjs.com/


═══════════════════════════════════════════════════════════════════════════
Ready to use! Open http://localhost:5000 in your browser.
═══════════════════════════════════════════════════════════════════════════
""")
