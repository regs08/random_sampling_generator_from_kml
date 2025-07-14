from pathlib import Path
import math

def gather_files_by_extension(folder: str, extension: str) -> list:
    folder_path = Path(folder)
    return list(folder_path.glob(f'*.{extension.lstrip(".")}'))

def meters_to_degrees(meters: float, latitude: float = 0.0) -> float:
    """
    Convert meters to degrees at a given latitude.
    
    Args:
        meters: Distance in meters
        latitude: Latitude in degrees (default: 0.0 for equator)
        
    Returns:
        float: Distance in degrees
    """
    # Earth's radius in meters
    earth_radius = 6371000  # meters
    
    # Convert latitude to radians
    lat_rad = math.radians(latitude)
    
    # Calculate degrees per meter at this latitude
    degrees_per_meter = 1 / (earth_radius * math.cos(lat_rad))
    
    return meters * degrees_per_meter

def degrees_to_meters(degrees: float, latitude: float = 0.0) -> float:
    """
    Convert degrees to meters at a given latitude.
    
    Args:
        degrees: Distance in degrees
        latitude: Latitude in degrees (default: 0.0 for equator)
        
    Returns:
        float: Distance in meters
    """
    # Earth's radius in meters
    earth_radius = 6371000  # meters
    
    # Convert latitude to radians
    lat_rad = math.radians(latitude)
    
    # Calculate meters per degree at this latitude
    meters_per_degree = earth_radius * math.cos(lat_rad)
    
    return degrees * meters_per_degree

def get_center_latitude(bounds: tuple) -> float:
    """
    Get the center latitude from boundary bounds.
    
    Args:
        bounds: Tuple of (minx, miny, maxx, maxy) in degrees
        
    Returns:
        float: Center latitude in degrees
    """
    minx, miny, maxx, maxy = bounds
    return (miny + maxy) / 2
