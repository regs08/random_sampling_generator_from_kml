"""
Random point generator for creating sampling points inside polygon boundaries.
"""
from typing import List, Tuple, Optional
import numpy as np
from shapely.geometry import Point, Polygon
from .boundary import BoundaryHandler
import logging

logger = logging.getLogger(__name__)

class RandomPointGenerator:
    """Generate random sampling points inside polygon boundaries."""
    
    def __init__(self, boundary_handler: BoundaryHandler):
        """
        Initialize with a boundary handler.
        
        Args:
            boundary_handler: BoundaryHandler instance
        """
        self.boundary_handler = boundary_handler
        self.bounds = boundary_handler.get_bounds()
        
        if not self.bounds:
            raise ValueError("No valid boundary available for point generation")
    

    
    def generate_points_with_minimum_distance(self, n_points: int, min_distance: float, 
                                           seed: Optional[int] = None) -> List[Point]:
        """
        Generate random points with minimum distance between them.
        
        Args:
            n_points: Number of points to generate
            min_distance: Minimum distance between points in degrees
            seed: Random seed for reproducibility
            
        Returns:
            List[Point]: List of shapely Point objects
        """
        if seed is not None:
            np.random.seed(seed)
            
        if n_points <= 0:
            logger.warning("Number of points must be positive")
            return []
            
        if min_distance <= 0:
            logger.warning("Minimum distance must be positive")
            return self.generate_points(n_points, seed)
            
        points = []
        attempts = 0
        max_attempts = n_points * 1000  # Higher limit for distance constraint
        
        while len(points) < n_points and attempts < max_attempts:
            # Generate random point within bounding box
            x = np.random.uniform(self.bounds[0], self.bounds[2])
            y = np.random.uniform(self.bounds[1], self.bounds[3])
            
            point = Point(x, y)
            
            # Check if point is inside boundary
            if not self.boundary_handler.contains_point(point):
                attempts += 1
                continue
                
            # Check minimum distance from existing points
            too_close = False
            for existing_point in points:
                distance = point.distance(existing_point)
                if distance < min_distance:
                    too_close = True
                    break
                    
            if not too_close:
                points.append(point)
                
            attempts += 1
            
        if len(points) < n_points:
            logger.warning(f"Could only generate {len(points)} points with minimum distance {min_distance}")
            
        logger.info(f"Generated {len(points)} random points with minimum distance in {attempts} attempts")
        return points
    


    def generate_points_per_polygon(self, n_points_per_polygon: int, 
                                  seed: Optional[int] = None, **kwargs) -> List[Point]:
        """
        Generate points for each individual polygon in the boundary handler with minimum distance.
        
        Args:
            n_points_per_polygon: Number of points to generate per polygon
            seed: Random seed for reproducibility
            **kwargs: Additional arguments (min_distance required)
            
        Returns:
            List[Point]: List of shapely Point objects
        """
        all_points = []
        
        if not self.boundary_handler.polygons:
            logger.warning("No polygons available for per-polygon sampling")
            return []
        
        logger.info(f"Generating {n_points_per_polygon} points per polygon for {len(self.boundary_handler.polygons)} polygons")
        
        for i, polygon in enumerate(self.boundary_handler.polygons):
            try:
                # Create a boundary handler for this single polygon
                single_polygon_handler = BoundaryHandler([polygon])
                single_generator = RandomPointGenerator(single_polygon_handler)
                
                # Use a unique seed for each polygon if a base seed is provided
                polygon_seed = seed + i if seed is not None else None
                
                # Generate points for this polygon with minimum distance
                polygon_points = single_generator.generate_points_with_minimum_distance(
                    n_points_per_polygon, kwargs.get("min_distance", 0.001), polygon_seed
                )
                
                all_points.extend(polygon_points)
                logger.info(f"Generated {len(polygon_points)} points for polygon {i+1}")
                
            except Exception as e:
                logger.error(f"Error generating points for polygon {i}: {str(e)}")
        
        logger.info(f"Total points generated across all polygons: {len(all_points)}")
        return all_points

def generate_sampling_points(boundary_handler: BoundaryHandler, n_points: int,
                           method: str = "min_distance", per_polygon: bool = True, **kwargs) -> List[Point]:
    """
    Generate sampling points per polygon with minimum distance.
    
    Args:
        boundary_handler: BoundaryHandler instance
        n_points: Number of points to generate per polygon
        method: Generation method (always "min_distance")
        per_polygon: Always True for per-polygon sampling
        **kwargs: Additional arguments (min_distance required)
        
    Returns:
        List[Point]: List of shapely Point objects
    """
    generator = RandomPointGenerator(boundary_handler)
    
    # Remove 'seed' from kwargs to avoid duplicate argument
    seed = kwargs.pop("seed", None)
    return generator.generate_points_per_polygon(n_points, seed=seed, **kwargs)
