# EnMAP Bounds Viewer - Web UI Integration Complete ✅

## What's New

Your request: "I wan to see and be able to run it through the UI"

### ✅ COMPLETED
- **Flask Web Server** (`server.py`) - Serves the HTML UI and provides `/api/query-enmap` endpoint
- **Integrated EnMAP Query UI** - Query panel added to the web app with:
  - Date range selectors (Start Date, End Date)
  - Max items input (1-500)
  - Query button that calls the Flask API
  - Results displayed in formatted table
  - Export results as JSON
- **Real-time STAC Integration** - Directly queries DLR EOC STAC API from the browser
- **Unified Interface** - No need to use command line anymore:
  1. Draw bounds or load CSV
  2. Set date range
  3. Click "Query EnMAP"
  4. View results immediately
  5. Export if needed

## How to Run

```bash
# 1. Start the server (it's already running on port 5000)
python3 server.py

# 2. Open in browser
http://localhost:5000

# 3. Use the interface:
#    - Use drawing tool to create AOI (click square icon)
#    - Or paste CSV bounds
#    - Set date range in EnMAP Query section
#    - Click "Query EnMAP"
#    - Results appear in table below
```

## New Files Created

| File | Purpose |
|------|---------|
| `server.py` | Flask web server with EnMAP API endpoint |
| `run_server.sh` | Convenient startup script |
| `SETUP_GUIDE.py` | Complete setup and usage documentation |

## Modified Files

| File | Changes |
|------|---------|
| `csv_bounds_viewer.html` | Added EnMAP query UI section with styled forms, results table, and export button |
| `README.md` | Updated with new server instructions and unified workflow |

## Features Now Available Through Web UI

✅ Draw rectangular AOIs on map
✅ Load bounds from CSV
✅ Calculate bounds information (area, width, height, midpoint)
✅ **Query EnMAP data directly from UI** ← NEW
✅ View satellite scene results (ID, date, cloud cover) ← NEW
✅ Export bounds as CSV
✅ Export query results as JSON ← NEW
✅ No command-line required ← NEW

## API Endpoint

The Flask server provides:

**POST** `/api/query-enmap`

```json
{
  "bounds": [min_lon, min_lat, max_lon, max_lat],
  "datetime": "YYYY-MM-DD/YYYY-MM-DD",
  "max_items": 100
}
```

Returns EnMAP scene information with cloud cover and data URLs.

## Current Status

✅ Server running on http://localhost:5000
✅ All dependencies installed (flask, flask-cors, pystac-client)
✅ Web UI fully functional with integrated EnMAP queries
✅ Ready to use!

## Next Steps (Optional)

If you want to:
- **Deploy to production**: Use Gunicorn or uWSGI instead of Flask dev server
- **Add more features**: Cloud cover filtering, scene preview images, direct download
- **Customize results display**: Add sorting, pagination, scene geometry visualization
- **Connect to database**: Store query history and saved bounds
