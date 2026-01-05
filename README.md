# CSV Bounds Viewer & EnMAP Data Integration

A unified geospatial platform for visualizing bounds, drawing AOIs, and querying EnMAP hyperspectral satellite data directly through an interactive web interface.

## Features

- **Interactive Map Viewer**: Visualize geographic bounds on OpenStreetMap
- **AOI Drawing Tool**: Draw custom rectangle Areas of Interest with real-time bounds calculation
- **Bounds Calculation**: Automatic area (km²), width, height, and midpoint computation
- **EnMAP Data Query**: Search for EnMAP HSI L2A satellite scenes by location and date
- **Scene Preview**: View thumbnail quicklooks of available satellite scenes
- **Smart Downloads**: Direct download links to scene data with intelligent URL construction
- **CSV Import/Export**: Load bounds from CSV and export query results as JSON
- **Responsive Design**: Three-panel layout (tools, controls, map) adapting to all screen sizes

## Quick Start

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/ashintalex/maps_bounds_viewer.git
cd maps_bounds_viewer
```

#### 2. Install Dependencies
```bash
pip install flask flask-cors pystac-client requests
```

#### 3. Run the Server
```bash
python3 server.py
```

You should see:
```
============================================================
🌍 EnMAP Bounds Viewer Server
============================================================

📍 Server: http://localhost:8080
🔗 STAC API: https://geoservice.dlr.de/eoc/ogc/stac/v1/
📦 Collection: ENMAP_HSI_L2A

✅ pystac-client is installed

Press Ctrl+C to stop the server
```

#### 4. Open in Browser
Navigate to **http://localhost:8080** in your web browser.

### Basic Usage

#### Drawing Areas of Interest (AOI)
1. Click the **square icon (⬜)** in the left tools panel to enable drawing mode
2. **First click** on the map: Places a red marker (center point)
3. **Second click** on the map: Creates a rectangle and populates the bounds in the CSV box
4. Bounds information displays automatically (area in km², width, height, center coordinates)

#### Loading Bounds from CSV
1. Paste CSV data in the "Load Bounds" text box with this format:
```csv
granule_id,north_lat,south_lat,west_lon,east_lon
my_aoi_1,45.5,45.0,-122.5,-122.0
my_aoi_2,46.0,45.5,-123.0,-122.5
```
2. Click **"Load Bounds"** button
3. Rectangles appear on the map showing each AOI

#### Querying EnMAP Data
1. Define your area (draw AOI or load bounds from CSV)
2. Set query parameters in the control panel:
   - **Start Date**: Beginning of search period
   - **End Date**: End of search period  
   - **Max Items**: Maximum results (1-500, default 100)
3. Click **"Query EnMAP"** button
4. Results appear in a table showing:
   - Scene ID
   - Acquisition date
   - Cloud cover percentage
   - Preview (🖼️) - Click to view quicklook thumbnail
   - Download (📥) - Click to access scene data

#### Downloading Scenes
1. In the query results table, check the boxes of scenes you want to download
2. Click **"Download Selected Scenes"** button
3. Each selected scene opens in a new browser tab for downloading
4. Files are available in multiple formats (ZIP, COG, etc.)

#### Exporting Data
- **Export Bounds as CSV**: Click "Export Bounds" to save your AOIs
- **Export Query Results**: Click "Export Results" to save EnMAP data as JSON

## File Structure

```
maps_bounds_viewer/
├── csv_bounds_viewer.html      # Complete web UI (HTML/CSS/JavaScript)
├── server.py                   # Flask backend with API endpoints
├── example_bounds.csv          # Sample bounds data
├── README.md                   # This file
└── requirements.txt            # Python dependencies (optional)
```

## System Requirements

- **Python**: 3.7 or higher
- **Browser**: Modern browser with JavaScript enabled (Chrome, Firefox, Safari, Edge)
- **Internet**: Connection required for map tiles and STAC API access
- **Port**: 8080 (must be available)

## Troubleshooting

### Server won't start
```bash
# Check if port 8080 is in use
lsof -i :8080

# Kill process using port 8080 (macOS/Linux)
lsof -ti :8080 | xargs kill -9

# Try starting server again
python3 server.py
```

### Missing Python packages
```bash
# Reinstall all dependencies
pip install --upgrade flask flask-cors pystac-client requests
```

### Map not displaying
- Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
- Check browser console for errors (F12)
- Verify internet connection (OpenStreetMap tiles require internet)
- Ensure JavaScript is enabled in browser

### EnMAP query returns no results
- Verify date range is valid and not too restrictive
- Check bounds are within EnMAP coverage (primarily Europe, Asia)
- Try increasing max_items parameter
- Ensure you clicked "Load Bounds" or drew an AOI before querying

### Preview images not loading
- Ensure internet connection is stable
- Try another scene's preview
- Check browser console (F12) for specific error messages

## API Documentation

### GET /api/preview
Proxy endpoint for preview images (handles CORS and MIME type fixes)

**Parameters:**
- `url`: Image URL to fetch (URL-encoded)

**Example:**
```
http://localhost:8080/api/preview?url=https://download.geoservice.dlr.de/...
```

### POST /api/query-enmap
Query EnMAP data for geographic bounds and date range

**Request:**
```json
{
  "bounds": [min_lon, min_lat, max_lon, max_lat],
  "datetime": "YYYY-MM-DD/YYYY-MM-DD",
  "max_items": 100
}
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "items": [
    {
      "id": "ENMAP01-____L2A-DT0000173759_20260103T180302Z_003_V010505_20260104T045017Z",
      "datetime": "2026-01-03T18:03:02Z",
      "cloud_cover": 8.5,
      "data_url": "https://download.geoservice.dlr.de/ENMAP/files/L2A/...",
      "preview_url": "https://download.geoservice.dlr.de/ENMAP/files/L2A/.../thumbnail.jpg",
      "available_assets": ["data", "metadata", "thumbnail"]
    }
  ]
}
```

## Architecture

### Frontend
- **HTML5** + **CSS3** + **Vanilla JavaScript** (no frameworks)
- **Leaflet.js 1.9.4** for interactive mapping
- **OpenStreetMap** tile layer
- **PapaParse 5.4.1** for CSV parsing

### Backend
- **Flask 1.x** web server with CORS support
- **pystac-client** for STAC API integration
- **requests** library for proxy image fetching

### Data Source
- **DLR EOC STAC API**: https://geoservice.dlr.de/eoc/ogc/stac/v1/
- **Collection**: ENMAP_HSI_L2A (EnMAP Hyperspectral Level 2A)
- **Download Server**: https://download.geoservice.dlr.de/ENMAP/

## Known Limitations

- Preview images may take a few seconds to load
- Large queries (>500 items) may be slow
- Browser storage may limit very large CSV files
- Some scene data may require authentication (redirects to DLR login)

## Contributing

Found a bug or have a feature request? Feel free to open an issue or submit a pull request!

## License

This project is provided as-is for geospatial data visualization and analysis.

## Support

For issues with:
- **Web App**: Check browser console (F12) for error messages
- **EnMAP Data**: Visit https://geoservice.dlr.de/eoc/ for platform documentation
- **STAC Specification**: See https://stacspec.org/
