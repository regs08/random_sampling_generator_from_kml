"""
Export sampling points to various formats (CSV, GeoJSON, etc.).
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from shapely.geometry import Point
import logging

logger = logging.getLogger(__name__)

class SamplingPointExporter:
    """Export sampling points to various file formats."""
    
    def __init__(self):
        self.default_metadata = {
            "project": "Random Sampling Generator",
            "version": "1.0.0"
        }
    
    def _generate_sample_prefix(self, sample_prefix: str = "SAMPLE", 
                              apply_to_group: Optional[str] = None,
                              n_points: int = 1,
                              min_distance_meters: float = 5.0) -> str:
        """
        Generate a descriptive sample prefix based on arguments.
        
        Args:
            sample_prefix: Base prefix for sample names
            apply_to_group: Filter applied (e.g., "description=triangle")
            n_points: Number of points per polygon
            min_distance_meters: Minimum distance in meters
            
        Returns:
            str: Descriptive prefix for sample names
        """
        prefix_parts = []
        
        # Add base prefix
        prefix_parts.append(sample_prefix)
        
        # Add filter information if present
        if apply_to_group:
            try:
                field, value = apply_to_group.split('=', 1)
                field = field.strip()
                value = value.strip()
                
                # Create descriptive filter name
                if field == "description":
                    prefix_parts.append(value.upper())
                elif field == "name":
                    # Use first word of name for brevity
                    name_parts = value.split()
                    prefix_parts.append(name_parts[0].upper())
                elif field == "styleUrl":
                    # Extract style identifier
                    if "#" in value:
                        style_id = value.split("#")[-1]
                        prefix_parts.append(style_id.upper())
                    else:
                        prefix_parts.append(value.upper())
                else:
                    prefix_parts.append(f"{field.upper()}_{value.upper()}")
                    
            except ValueError:
                # If parsing fails, use the raw filter value
                prefix_parts.append(apply_to_group.upper().replace("=", "_"))
        
        # Add point count if not default
        if n_points != 1:
            prefix_parts.append(f"P{n_points}")
        
        # Add distance if not default
        if min_distance_meters != 5.0:
            prefix_parts.append(f"D{int(min_distance_meters)}M")
        
        return "_".join(prefix_parts)
    
    def export_to_csv(self, points: List[Point], output_path: str, 
                     metadata: Optional[Dict[str, Any]] = None,
                     sample_prefix: str = "SAMPLE",
                     apply_to_group: Optional[str] = None,
                     n_points: int = 1,
                     min_distance_meters: float = 5.0) -> bool:
        """
        Export sampling points to CSV format.
        
        Args:
            points: List of shapely Point objects
            output_path: Path to output CSV file
            metadata: Additional metadata to include
            sample_prefix: Prefix for sample names
            apply_to_group: Filter applied (for naming)
            n_points: Number of points per polygon (for naming)
            min_distance_meters: Minimum distance in meters (for naming)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not points:
                logger.warning("No points to export")
                return False
                
            # Generate descriptive sample prefix
            descriptive_prefix = self._generate_sample_prefix(
                sample_prefix, apply_to_group, n_points, min_distance_meters
            )
            
            # Prepare data for DataFrame
            data = []
            for i, point in enumerate(points):
                sample_data = {
                    "sample_name": f"{descriptive_prefix}_{i+1:04d}",
                    "longitude": point.x,
                    "latitude": point.y,
                    "point_id": i + 1
                }
                
                # Add metadata if provided
                if metadata:
                    for key, value in metadata.items():
                        sample_data[f"metadata_{key}"] = value
                        
                data.append(sample_data)
                
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Export to CSV
            df.to_csv(output_path, index=False)
            
            logger.info(f"Exported {len(points)} points to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return False
    

    

    


def export_sampling_points(points: List[Point], output_path: str,
                          format: str = "csv", **kwargs) -> bool:
    """
    Export sampling points to CSV format.
    
    Args:
        points: List of shapely Point objects
        output_path: Path to output CSV file
        format: Output format (always "csv")
        **kwargs: Additional arguments for CSV export
        
    Returns:
        bool: True if successful, False otherwise
    """
    exporter = SamplingPointExporter()
    return exporter.export_to_csv(points, output_path, **kwargs)
