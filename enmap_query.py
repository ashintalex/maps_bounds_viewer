#!/usr/bin/env python3
"""
EnMAP Data Availability Checker
Queries the DLR EOC STAC API for EnMAP HSI L2A products within specified bounds.
"""

import argparse
import json
import csv
from datetime import datetime
from pathlib import Path
from pystac_client import Client


class EnMAPQuery:
    def __init__(self, stac_url="https://geoservice.dlr.de/eoc/ogc/stac/v1/"):
        self.stac_url = stac_url
        self.catalog = Client.open(stac_url)
        self.collection = "ENMAP_HSI_L2A"
    
    def query_bounds(self, bbox, datetime_range="2024-01-01/2026-01-05", max_items=100):
        """
        Query EnMAP data within specified bounds.
        
        Args:
            bbox: [min_lon, min_lat, max_lon, max_lat]
            datetime_range: "start_date/end_date"
            max_items: Maximum number of items to return
        
        Returns:
            List of matching items
        """
        print(f"🔍 Querying EnMAP data...")
        print(f"   Bounding Box: {bbox}")
        print(f"   Time Range: {datetime_range}")
        print(f"   Collection: {self.collection}")
        print()
        
        try:
            search = self.catalog.search(
                collections=[self.collection],
                bbox=bbox,
                datetime=datetime_range,
                max_items=max_items
            )
            
            items = search.item_collection()
            return list(items)
        
        except Exception as e:
            print(f"❌ Error querying STAC API: {e}")
            return []
    
    def print_results(self, items):
        """Print results in a formatted table."""
        if not items:
            print("❌ No EnMAP scenes found for the specified criteria.")
            return
        
        print(f"✅ Found {len(items)} matching EnMAP scenes!\n")
        print("=" * 100)
        print(f"{'ID':<40} {'Date':<20} {'Cloud Cover':<15} {'Data Available':<15}")
        print("=" * 100)
        
        for item in items:
            item_id = item.id[:38] + ".." if len(item.id) > 40 else item.id
            date = str(item.datetime)[:10] if item.datetime else "N/A"
            cloud_cover = f"{item.properties.get('eo:cloud_cover', 'N/A')}%"
            has_data = "✓ Yes" if "data" in item.assets else "✗ No"
            
            print(f"{item_id:<40} {date:<20} {cloud_cover:<15} {has_data:<15}")
        
        print("=" * 100)
        print()
    
    def export_results(self, items, output_file="enmap_results.json"):
        """Export results to JSON file."""
        results = []
        for item in items:
            result = {
                "id": item.id,
                "datetime": str(item.datetime),
                "cloud_cover": item.properties.get("eo:cloud_cover", None),
                "data_url": item.assets.get("data", {}).get("href") if "data" in item.assets else None,
                "preview_url": item.assets.get("thumbnail", {}).get("href") if "thumbnail" in item.assets else None,
            }
            results.append(result)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Results exported to: {output_file}")
    
    def load_bounds_from_csv(self, csv_file):
        """Load bounds from the CSV Bounds Viewer export."""
        bounds_list = []
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bbox = [
                        float(row['west_lon']),
                        float(row['south_lat']),
                        float(row['east_lon']),
                        float(row['north_lat'])
                    ]
                    bounds_list.append({
                        'granule_id': row['granule_id'],
                        'bbox': bbox
                    })
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")
        
        return bounds_list


def main():
    parser = argparse.ArgumentParser(
        description="Query EnMAP data availability for specified geographic bounds",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query using command-line bounds
  python enmap_query.py --bbox 11.23 48.05 11.33 48.11
  
  # Query using CSV file from bounds viewer
  python enmap_query.py --csv-file bounds.csv
  
  # Query with custom time range
  python enmap_query.py --bbox 11.23 48.05 11.33 48.11 --datetime 2025-01-01/2025-12-31
  
  # Export results to JSON
  python enmap_query.py --bbox 11.23 48.05 11.33 48.11 --export enmap_results.json
        """
    )
    
    parser.add_argument(
        '--bbox',
        nargs=4,
        type=float,
        metavar=('MIN_LON', 'MIN_LAT', 'MAX_LON', 'MAX_LAT'),
        help='Bounding box as: min_lon min_lat max_lon max_lat'
    )
    
    parser.add_argument(
        '--csv-file',
        type=str,
        help='Path to CSV file exported from CSV Bounds Viewer'
    )
    
    parser.add_argument(
        '--datetime',
        type=str,
        default='2024-01-01/2026-01-05',
        help='Time range as: start_date/end_date (default: 2024-01-01/2026-01-05)'
    )
    
    parser.add_argument(
        '--max-items',
        type=int,
        default=100,
        help='Maximum number of results to return (default: 100)'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        help='Export results to JSON file'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.bbox and not args.csv_file:
        parser.print_help()
        print("\n❌ Error: Please provide either --bbox or --csv-file")
        return
    
    # Initialize query object
    query = EnMAPQuery()
    
    # Process bounds
    bounds_to_query = []
    
    if args.bbox:
        bounds_to_query.append({
            'name': 'Custom Bounds',
            'bbox': args.bbox
        })
    
    if args.csv_file:
        csv_bounds = query.load_bounds_from_csv(args.csv_file)
        bounds_to_query.extend([{'name': b['granule_id'], 'bbox': b['bbox']} for b in csv_bounds])
    
    # Execute queries
    all_items = []
    for bounds in bounds_to_query:
        print(f"\n📍 Querying: {bounds['name']}")
        items = query.query_bounds(bounds['bbox'], args.datetime, args.max_items)
        query.print_results(items)
        all_items.extend(items)
    
    # Export if requested
    if args.export and all_items:
        query.export_results(all_items, args.export)


if __name__ == "__main__":
    main()
