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
    
    def export_to_csv(self, points: List[Point], output_path: str, 
                     metadata: Optional[Dict[str, Any]] = None,
                     sample_prefix: str = "SAMPLE") -> bool:
        """
        Export sampling points to CSV format.
        
        Args:
            points: List of shapely Point objects
            output_path: Path to output CSV file
            metadata: Additional metadata to include
            sample_prefix: Prefix for sample names
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not points:
                logger.warning("No points to export")
                return False
                
            # Prepare data for DataFrame
            data = []
            for i, point in enumerate(points):
                sample_data = {
                    "sample_name": f"{sample_prefix}_{i+1:04d}",
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
