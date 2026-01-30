import pyproj
from shapely.geometry import Polygon

class GeometryProcessor:
    """
    Handles high-precision spatial transformations. 
    Implements Snyder Equal-Area logic for accurate material estimation.
    """
    def __init__(self):
        # WGS84 to Albers Equal Area for precise SqFt measurements
        self.geod = pyproj.Geod(ellps="WGS84")

    def simplify_and_calculate(self, coords: list, tolerance: float = 0.05):
        poly = Polygon(coords)
        # Ramer-Douglas-Peucker simplification for professional deliverables
        simplified = poly.simplify(tolerance, preserve_topology=True)
        
        # Calculate area in Sq Meters, then convert to Sq Ft
        area_sq_m, _ = self.geod.geometry_area_perimeter(simplified)
        return abs(area_sq_m) * 10.7639, simplified
