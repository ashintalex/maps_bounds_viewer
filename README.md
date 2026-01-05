# CSV Bounds Viewer

A simple web-based tool to visualize geographic bounding boxes on an interactive map.

## Features

- Load CSV data with geographic bounds
- Interactive map visualization with OpenStreetMap
- Calculate area, width, height, and midpoint of bounds
- **Tools Panel**: Draw custom rectangle Areas of Interest (AOI) directly on the map
- **View Bounds**: Toggle display of bounds information
- Responsive layout with tools panel, control panel, and map viewer

## Usage

1. Open `csv_bounds_viewer.html` in your browser
2. Use the **Tools Panel** on the left:
   - Click the square icon (⬜) to enter drawing mode
   - **First click**: Places a red numbered marker (1) on the map
   - **Second click**: Places a green numbered marker (2) and creates the rectangle AOI between the two points
   - The drawn bounds will automatically appear in the CSV input area
   - Click the ruler icon (📐) to show/hide bounds information
3. Alternatively, paste CSV data in the control panel and click "Load Bounds"
4. View bounds information including area, width, height, and midpoint

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
