# 🌍 EnMAP Bounds Viewer - Quick Start Guide

## ✅ Now Running at http://localhost:5000

Your complete geospatial tool is ready to use! No more command-line needed.

---

## 🚀 Getting Started

### What You Can Do Now:

1. **Draw AOIs on the Map**
   - Click the square icon (⬜) in the left tools panel
   - Click once on the map (red marker = center)
   - Click again to complete rectangle (green marker = corner)
   - Bounds auto-populate in the CSV area

2. **Load Existing Bounds**
   - Paste CSV data into the textarea
   - Click "Load Bounds" to visualize on map
   - Click rectangles to see details

3. **Query EnMAP Data** ← NEW FEATURE
   - Load or draw bounds (step 1 or 2)
   - Scroll down to "EnMAP Query" section
   - Set date range (Start Date → End Date)
   - Set Max Items (up to 500)
   - Click "Query EnMAP"
   - Results appear in formatted table below
   - See: Scene ID, Acquisition Date, Cloud Cover %

4. **Export Results**
   - Click "Export Bounds" to download CSV
   - Click "Export Results" to download query results as JSON

---

## 📊 CSV Format

**Input (Load Bounds):**
```csv
granule_id,north_lat,south_lat,west_lon,east_lon
aoi_1,45.5,45.0,-122.5,-122.0
aoi_2,46.0,45.5,-123.0,-122.5
```

**Output (Export):**
Same format, auto-timestamped filename

---

## 🔍 EnMAP Query Tips

- **Date Range**: Use format YYYY-MM-DD
- **Default**: 2024-01-01 to 2026-01-05
- **Max Items**: Start with 50, increase if needed
- **No Results?**: Bounds might not have EnMAP coverage, or date range too narrow
- **Cloud Cover**: Shown in results for each scene

---

## 📁 What's Running

```
Backend:        Flask server (Python)
Frontend:       HTML5 + Leaflet.js maps
API Endpoint:   /api/query-enmap
Port:           5000
Database:       DLR EOC STAC API
```

---

## ⚙️ System Status

✅ Flask server running
✅ STAC API connection ready
✅ pystac-client installed
✅ Map tiles loading from OpenStreetMap
✅ CSV parsing enabled
✅ JSON export ready

---

## 🔧 Troubleshooting

**Map not showing?**
- Refresh the page (Cmd+R)
- Check browser console (F12)
- Ensure internet connection

**EnMAP query won't run?**
- Check date format (YYYY-MM-DD)
- Verify bounds are loaded
- Try increasing Max Items
- Check internet connection

**Server error?**
- Server is running on http://localhost:5000
- Check terminal for error messages
- Port 5000 should be free

---

## 💡 Example Workflow

1. Open http://localhost:5000 in browser
2. Click "Load Bounds" (default bounds are pre-filled)
3. Scroll down to "EnMAP Query" section
4. Set dates: 2024-01-01 to 2025-12-31
5. Click "Query EnMAP"
6. See results table populate with scenes
7. Click "Export Results" to download JSON

That's it! No CLI needed. Everything is in the UI.

---

## 📚 Server Files

- **server.py**: Flask app (runs on 5000)
- **csv_bounds_viewer.html**: Web UI (served by Flask)
- **enmap_query.py**: Legacy CLI tool (optional)
- **run_server.sh**: Startup script

---

**Ready to explore? Go to http://localhost:5000 now! 🚀**
