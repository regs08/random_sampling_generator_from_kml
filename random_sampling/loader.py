"""
KML file loader for parsing polygon boundaries using lxml.
"""
from pathlib import Path
from typing import List, Tuple, Optional
from lxml import etree
from shapely.geometry import Polygon
import logging

logger = logging.getLogger(__name__)

class KMLLoader:
    """Load and parse KML files to extract polygon boundaries using lxml."""
    
    def __init__(self):
        self.kml_doc = None
        
    def load_kml(self, file_path: str) -> bool:
        """
        Load a KML file from the given path.
        
        Args:
            file_path: Path to the KML file
            
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        try:
            kml_path = Path(file_path)
            if not kml_path.exists():
                logger.error(f"KML file not found: {file_path}")
                return False
                
            # Parse KML with lxml
            parser = etree.XMLParser(remove_blank_text=True)
            self.kml_doc = etree.parse(str(kml_path), parser)
            
            logger.info(f"Successfully loaded KML file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading KML file {file_path}: {str(e)}")
            return False
    
    def extract_polygons_with_attributes(self) -> List[Tuple[Polygon, dict]]:
        """Extract all polygons with their KML attributes from the loaded KML document."""
        polygons_with_attrs = []
        if not self.kml_doc:
            logger.error("No KML document loaded")
            return []
        
        # Define KML namespace
        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
        
        try:
            # Find all Placemark elements that contain polygons
            placemark_elements = self.kml_doc.xpath('//kml:Placemark', namespaces=ns)
            logger.info(f"Found {len(placemark_elements)} placemark elements")
            
            for i, placemark_elem in enumerate(placemark_elements):
                try:
                    # Extract polygon from this placemark
                    polygon_elem = placemark_elem.xpath('.//kml:Polygon', namespaces=ns)
                    if not polygon_elem:
                        continue
                    
                    # Extract coordinates from the polygon
                    coords = self._extract_polygon_coordinates(polygon_elem[0], ns)
                    if coords and len(coords) >= 3:
                        polygon = Polygon(coords)
                        if polygon.is_valid:
                            # Extract attributes from the placemark
                            attributes = self._extract_placemark_attributes(placemark_elem, ns)
                            polygons_with_attrs.append((polygon, attributes))
                            logger.debug(f"Added valid polygon {i+1} with {len(coords)} coordinates and attributes: {attributes}")
                        else:
                            logger.warning(f"Invalid polygon geometry found at index {i}")
                    else:
                        logger.warning(f"Insufficient coordinates for polygon at index {i}")
                        
                except Exception as e:
                    logger.error(f"Error processing placemark {i}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error extracting polygons: {str(e)}")
            
        logger.info(f"Successfully extracted {len(polygons_with_attrs)} valid polygons with attributes")
        return polygons_with_attrs
    
    def extract_polygons(self) -> List[Polygon]:
        """Extract all polygons from the loaded KML document (backward compatibility)."""
        polygons_with_attrs = self.extract_polygons_with_attributes()
        return [polygon for polygon, _ in polygons_with_attrs]
    
    def _extract_placemark_attributes(self, placemark_elem, ns) -> dict:
        """Extract attributes from a KML Placemark element."""
        attributes = {}
        
        try:
            # Extract name
            name_elem = placemark_elem.xpath('.//kml:name', namespaces=ns)
            if name_elem and name_elem[0].text:
                attributes['name'] = name_elem[0].text.strip()
            
            # Extract styleUrl
            style_elem = placemark_elem.xpath('.//kml:styleUrl', namespaces=ns)
            if style_elem and style_elem[0].text:
                style_url = style_elem[0].text.strip()
                # Remove the # prefix if present
                if style_url.startswith('#'):
                    style_url = style_url[1:]
                attributes['styleUrl'] = style_url
            
            # Extract description
            desc_elem = placemark_elem.xpath('.//kml:description', namespaces=ns)
            if desc_elem and desc_elem[0].text:
                attributes['description'] = desc_elem[0].text.strip()
            
            # Extract ExtendedData
            extended_data = placemark_elem.xpath('.//kml:ExtendedData//kml:Data', namespaces=ns)
            for data_elem in extended_data:
                name_attr = data_elem.get('name')
                if name_attr:
                    value_elem = data_elem.xpath('.//kml:value', namespaces=ns)
                    if value_elem and value_elem[0].text:
                        attributes[f'data_{name_attr}'] = value_elem[0].text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting placemark attributes: {str(e)}")
            
        return attributes
    
    def _extract_polygon_coordinates(self, polygon_elem, ns) -> Optional[List[Tuple[float, float]]]:
        """Extract coordinate pairs from a KML Polygon element."""
        try:
            # Look for coordinates in outerBoundaryIs first, then innerBoundaryIs
            outer_boundary = polygon_elem.xpath('.//kml:outerBoundaryIs//kml:coordinates', namespaces=ns)
            
            if not outer_boundary:
                # Try direct coordinates element (some KML files have this structure)
                outer_boundary = polygon_elem.xpath('.//kml:coordinates', namespaces=ns)
            
            if outer_boundary:
                coords_text = outer_boundary[0].text.strip()
                return self._parse_coordinates_text(coords_text)
            else:
                logger.warning("No coordinates found in polygon element")
                return None
                
        except Exception as e:
            logger.error(f"Error extracting coordinates: {str(e)}")
            return None
    
    def _parse_coordinates_text(self, coords_text: str) -> List[Tuple[float, float]]:
        """Parse KML coordinates text into list of (lon, lat) tuples."""
        coordinates = []
        
        try:
            # Split by whitespace and newlines
            coord_pairs = coords_text.split()
            
            for coord_pair in coord_pairs:
                # KML format is "longitude,latitude,altitude" (altitude is optional)
                parts = coord_pair.split(',')
                if len(parts) >= 2:
                    lon = float(parts[0])
                    lat = float(parts[1])
                    coordinates.append((lon, lat))
                    
        except Exception as e:
            logger.error(f"Error parsing coordinates text: {str(e)}")
            
        return coordinates

def load_kml_file(file_path: str) -> List[Polygon]:
    """
    Convenience function to load KML file and extract polygons.
    
    Args:
        file_path: Path to the KML file
        
    Returns:
        List[Polygon]: List of shapely Polygon objects
    """
    loader = KMLLoader()
    if loader.load_kml(file_path):
        return loader.extract_polygons()
    return []
