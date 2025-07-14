"""
Boundary handling for polygon operations and coordinate transformations.
"""
from typing import List, Tuple, Optional
from shapely.geometry import Polygon, Point
from shapely.ops import transform
import pyproj
import logging

logger = logging.getLogger(__name__)

class BoundaryHandler:
    """Handle polygon boundaries and coordinate transformations."""
    
    def __init__(self, polygons: List[Polygon], polygon_attributes: Optional[List[dict]] = None):
        """
        Initialize with a list of polygons and optional attributes.
        
        Args:
            polygons: List of shapely Polygon objects
            polygon_attributes: List of attribute dictionaries (optional)
        """
        self.polygons = polygons
        self.polygon_attributes = polygon_attributes or [{}] * len(polygons)
        self._validate_polygons()
        
    def _validate_polygons(self):
        """Validate that all polygons are valid."""
        valid_polygons = []
        valid_attributes = []
        for i, polygon in enumerate(self.polygons):
            if polygon.is_valid:
                valid_polygons.append(polygon)
                valid_attributes.append(self.polygon_attributes[i] if i < len(self.polygon_attributes) else {})
            else:
                logger.warning(f"Invalid polygon at index {i}, skipping")
                
        self.polygons = valid_polygons
        self.polygon_attributes = valid_attributes
        
    def get_combined_boundary(self) -> Optional[Polygon]:
        """
        Get a single polygon representing the union of all boundaries.
        
        Returns:
            Polygon: Combined boundary polygon, or None if no valid polygons
        """
        if not self.polygons:
            logger.error("No valid polygons available")
            return None
            
        if len(self.polygons) == 1:
            return self.polygons[0]
            
        try:
            # Union all polygons
            combined = self.polygons[0]
            for polygon in self.polygons[1:]:
                combined = combined.union(polygon)
                
            return combined
            
        except Exception as e:
            logger.error(f"Error combining polygons: {str(e)}")
            return None
    
    def contains_point(self, point: Point) -> bool:
        """
        Check if a point is inside any of the boundary polygons.
        
        Args:
            point: shapely Point object
            
        Returns:
            bool: True if point is inside any boundary
        """
        if not self.polygons:
            return False
            
        try:
            for polygon in self.polygons:
                if polygon.contains(point):
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Error checking point containment: {str(e)}")
            return False
    
    def get_bounds(self) -> Optional[Tuple[float, float, float, float]]:
        """
        Get the bounding box of all polygons (minx, miny, maxx, maxy).
        
        Returns:
            Tuple: (minx, miny, maxx, maxy) or None if no polygons
        """
        if not self.polygons:
            return None
            
        try:
            combined = self.get_combined_boundary()
            if combined:
                return combined.bounds
            return None
            
        except Exception as e:
            logger.error(f"Error getting bounds: {str(e)}")
            return None
    
    def get_area(self) -> float:
        """
        Get the total area of all polygons in square degrees.
        
        Returns:
            float: Total area
        """
        if not self.polygons:
            return 0.0
            
        try:
            total_area = sum(polygon.area for polygon in self.polygons)
            return total_area
            
        except Exception as e:
            logger.error(f"Error calculating area: {str(e)}")
            return 0.0
    
    def filter_by_attribute(self, field: str, value: str) -> 'BoundaryHandler':
        """
        Filter polygons by a specific attribute field and value.
        
        Args:
            field: Attribute field name (e.g., 'name', 'styleUrl', 'data_Name')
            value: Value to match (case-insensitive)
            
        Returns:
            BoundaryHandler: New handler with filtered polygons
        """
        if not self.polygon_attributes:
            logger.warning("No polygon attributes available for filtering")
            return self
            
        filtered_polygons = []
        filtered_attributes = []
        
        for i, (polygon, attributes) in enumerate(zip(self.polygons, self.polygon_attributes)):
            # Check if the attribute matches
            attr_value = attributes.get(field, '')
            if isinstance(attr_value, str) and value.lower() in attr_value.lower():
                filtered_polygons.append(polygon)
                filtered_attributes.append(attributes)
                logger.debug(f"Matched polygon {i+1}: {field}={attr_value}")
        
        logger.info(f"Filtered to {len(filtered_polygons)} polygons matching {field}={value}")
        return BoundaryHandler(filtered_polygons, filtered_attributes)

class CoordinateTransformer:
    """Handle coordinate system transformations."""
    
    def __init__(self, from_crs: str = "EPSG:4326", to_crs: str = "EPSG:4326"):
        """
        Initialize coordinate transformer.
        
        Args:
            from_crs: Source coordinate reference system
            to_crs: Target coordinate reference system
        """
        self.from_crs = from_crs
        self.to_crs = to_crs
        self.transformer = None
        
        if from_crs != to_crs:
            try:
                self.transformer = pyproj.Transformer.from_crs(
                    from_crs, to_crs, always_xy=True
                )
            except Exception as e:
                logger.error(f"Error creating coordinate transformer: {str(e)}")
    
    def transform_point(self, x: float, y: float) -> Tuple[float, float]:
        """
        Transform a point from source CRS to target CRS.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple: (transformed_x, transformed_y)
        """
        if self.transformer is None:
            return (x, y)
            
        try:
            transformed_x, transformed_y = self.transformer.transform(x, y)
            return (transformed_x, transformed_y)
        except Exception as e:
            logger.error(f"Error transforming coordinates: {str(e)}")
            return (x, y)
    
    def transform_polygon(self, polygon: Polygon) -> Polygon:
        """
        Transform a polygon from source CRS to target CRS.
        
        Args:
            polygon: shapely Polygon object
            
        Returns:
            Polygon: Transformed polygon
        """
        if self.transformer is None:
            return polygon
            
        try:
            return transform(self.transformer.transform, polygon)
        except Exception as e:
            logger.error(f"Error transforming polygon: {str(e)}")
            return polygon

def create_boundary_handler(polygons: List[Polygon], polygon_attributes: Optional[List[dict]] = None) -> BoundaryHandler:
    """
    Convenience function to create a boundary handler.
    
    Args:
        polygons: List of shapely Polygon objects
        polygon_attributes: List of attribute dictionaries (optional)
        
    Returns:
        BoundaryHandler: Configured boundary handler
    """
    return BoundaryHandler(polygons, polygon_attributes)
