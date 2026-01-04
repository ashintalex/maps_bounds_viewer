# CSV Bounds Viewer

A simple web-based tool to visualize geographic bounding boxes on an interactive map.

## Features

- Load CSV data with geographic bounds
- Interactive map visualization with OpenStreetMap
- Calculate area, width, height, and midpoint of bounds
- Responsive layout with control panel and map viewer

## Usage

1. Open `csv_bounds_viewer.html` in your browser
2. Paste CSV data in the left control panel
3. Click "Load Bounds" to visualize on the map
4. View bounds information including area and midpoint

## CSV Format

The CSV should include the following columns:
```
granule_id,north_lat,south_lat,west_lon,east_lon
```

Example:
```
milan_italy,45.43360417128909,45.296389684940266,8.993144532517837,9.141464063463546
```

See `example_bounds.csv` for sample data.

## Technologies

- Leaflet.js for map rendering
- PapaParse for CSV parsing
- OpenStreetMap tiles
