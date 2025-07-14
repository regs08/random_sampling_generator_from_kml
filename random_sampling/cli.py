"""
Command-line interface for the random sampling point generator.

Author: Cole Regnier
Institution: Cornell University, Gold Lab
Email: nr466@cornell.edu

Designed for agricultural fieldwork and research sampling.
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .loader import load_kml_file, KMLLoader
from .boundary import create_boundary_handler
from .generator import generate_sampling_points
from .exporter import export_sampling_points, SamplingPointExporter
from .utils import meters_to_degrees, get_center_latitude

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate random sampling points inside KML polygon boundaries with minimum distance per polygon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (per-polygon with minimum distance)
  python -m random_sampling.cli --file data/field.kml --n_points 5 --min_distance_meters 50 --output data/samples.csv
  
  # With different distance
  python -m random_sampling.cli --file data/field.kml --n_points 10 --min_distance_meters 25 --output data/samples.csv
  
  # With custom metadata
  python -m random_sampling.cli --file data/field.kml --n_points 3 --min_distance_meters 100 --output data/samples.csv --metadata "project=Field Study 2024"

Author: Cole Regnier (Cornell University, Gold Lab) - nr466@cornell.edu
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to input KML file"
    )
    
    parser.add_argument(
        "--n_points", "-n",
        type=int,
        required=True,
        help="Number of sampling points to generate"
    )
    
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to output CSV file"
    )
    
    # Optional arguments
    parser.add_argument(
        "--min_distance_meters",
        type=float,
        default=5.0,
        help="Minimum distance between points in meters (default: 5.0)"
    )
    
    parser.add_argument(
        "--apply_to_group",
        help="Filter polygons by KML attribute (format: field=value, e.g., name=Chardonnay or styleUrl=poly-3949AB-2000-76)"
    )
    
    parser.add_argument(
        "--seed", "-s",
        type=int,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--sample_prefix",
        default="SAMPLE",
        help="Prefix for sample names (default: SAMPLE)"
    )
    
    parser.add_argument(
        "--metadata",
        action="append",
        help="Additional metadata in key=value format (can be used multiple times)"
    )
    
    parser.add_argument(
        "--format",
        choices=["csv", "geojson"],
        default="csv",
        help="Output format (default: csv)"
    )
    
    parser.add_argument(
        "--summary",
        help="Path to save summary report (optional)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress logging output"
    )
    
    return parser

def parse_metadata(metadata_args: Optional[list]) -> dict:
    """Parse metadata arguments into a dictionary."""
    metadata = {}
    if metadata_args:
        for arg in metadata_args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                metadata[key.strip()] = value.strip()
            else:
                logger.warning(f"Invalid metadata format: {arg}. Use key=value format.")
    return metadata

def validate_arguments(args: argparse.Namespace) -> bool:
    """Validate command-line arguments."""
    # Check input file exists
    if not Path(args.file).exists():
        logger.error(f"Input file not found: {args.file}")
        return False
    
    # Check number of points is positive
    if args.n_points <= 0:
        logger.error("Number of points must be positive")
        return False
    
    # Check minimum distance
    if args.min_distance_meters <= 0:
        logger.error("Minimum distance in meters must be positive")
        return False
    
    return True

def main():
    """Main CLI function."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('random_sampling').setLevel(logging.DEBUG)
        logging.getLogger('random_sampling.loader').setLevel(logging.DEBUG)
        logging.getLogger('random_sampling.boundary').setLevel(logging.DEBUG)
        logging.getLogger('random_sampling.generator').setLevel(logging.DEBUG)
        logging.getLogger('random_sampling.exporter').setLevel(logging.DEBUG)
    
    # Validate arguments
    if not validate_arguments(args):
        sys.exit(1)
    
    try:
        logger.info("Starting random sampling point generation")
        logger.info(f"Input file: {args.file}")
        logger.info(f"Number of points per polygon: {args.n_points}")
        logger.info(f"Minimum distance: {args.min_distance_meters} meters")
        logger.info(f"Output: {args.output}")
        
        # Step 1: Load KML file
        logger.info("Loading KML file...")
        loader = KMLLoader()
        if not loader.load_kml(args.file):
            logger.error("Failed to load KML file")
            sys.exit(1)
        
        polygons_with_attrs = loader.extract_polygons_with_attributes()
        if not polygons_with_attrs:
            logger.error("No valid polygons found in KML file")
            sys.exit(1)
        
        # Separate polygons and attributes
        polygons = [polygon for polygon, _ in polygons_with_attrs]
        polygon_attributes = [attrs for _, attrs in polygons_with_attrs]
        
        logger.info(f"Loaded {len(polygons)} polygon(s)")
        
        # Step 2: Create boundary handler
        logger.info("Processing boundaries...")
        boundary_handler = create_boundary_handler(polygons, polygon_attributes)
        
        # Apply filtering if specified
        if args.apply_to_group:
            try:
                field, value = args.apply_to_group.split('=', 1)
                field = field.strip()
                value = value.strip()
                logger.info(f"Filtering polygons by {field}={value}")
                boundary_handler = boundary_handler.filter_by_attribute(field, value)
                
                if not boundary_handler.polygons:
                    logger.error(f"No polygons match the filter {field}={value}")
                    sys.exit(1)
                    
                logger.info(f"Filtered to {len(boundary_handler.polygons)} polygon(s)")
                
            except ValueError:
                logger.error("Invalid filter format. Use 'field=value' (e.g., 'name=Chardonnay')")
                sys.exit(1)
        
        # Get boundary statistics
        bounds = boundary_handler.get_bounds()
        area = boundary_handler.get_area()
        
        if bounds:
            logger.info(f"Boundary bounds: {bounds}")
        if area > 0:
            logger.info(f"Boundary area: {area:.6f} square degrees")
        
        # Step 3: Generate sampling points
        logger.info("Generating sampling points per polygon with minimum distance...")
        
        # Get boundary bounds to calculate center latitude
        bounds = boundary_handler.get_bounds()
        if bounds:
            center_lat = get_center_latitude(bounds)
            min_distance_degrees = meters_to_degrees(args.min_distance_meters, center_lat)
            logger.info(f"Converting {args.min_distance_meters} meters to {min_distance_degrees:.6f} degrees at latitude {center_lat:.2f}")
        else:
            logger.warning("Could not determine boundary bounds, using default latitude (0.0)")
            min_distance_degrees = meters_to_degrees(args.min_distance_meters, 0.0)
        
        # Prepare generation arguments
        gen_kwargs = {
            "seed": args.seed,
            "min_distance": min_distance_degrees
        }
        
        points = generate_sampling_points(
            boundary_handler, 
            args.n_points, 
            "min_distance", 
            per_polygon=True,
            **gen_kwargs
        )
        
        if not points:
            logger.error("Failed to generate sampling points")
            sys.exit(1)
        
        logger.info(f"Generated {len(points)} sampling points")
        
        # Step 4: Export points
        logger.info("Exporting sampling points...")
        
        # Parse metadata
        metadata = parse_metadata(args.metadata)
        
        # Export main file
        export_kwargs = {
            "metadata": metadata,
            "sample_prefix": args.sample_prefix,
            "apply_to_group": args.apply_to_group,
            "n_points": args.n_points,
            "min_distance_meters": args.min_distance_meters
        }
        
        success = export_sampling_points(
            points, 
            args.output, 
            args.format, 
            **export_kwargs
        )
        
        if not success:
            logger.error("Failed to export sampling points")
            sys.exit(1)
        
        # Step 5: Export summary report if requested
        if args.summary:
            logger.info("Generating summary report...")
            exporter = SamplingPointExporter()
            exporter.export_summary_report(
                points,
                args.summary,
                boundary_area=area,
                generation_method=args.method
            )
        
        logger.info("Random sampling point generation completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
