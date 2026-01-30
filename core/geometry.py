import numpy as np
from shapely.geometry import Polygon
import pyproj

class GeometryProcessor:
    def __init__(self):
        # Albers Equal Area for precise financial measurements
        self.geod = pyproj.Geod(ellps="WGS84")

    def simplify_polygon(self, polygon: Polygon, tolerance: float = 0.05) -> Polygon:
        """
        Applies Douglas-Peucker simplification to remove 'jagged' AI artifacts.
        Tolerance is in decimal degrees; 0.05 is generally safe for site plans.
        """
        # Preserve_topology=True prevents the polygon from 'collapsing' into a line
        simplified = polygon.simplify(tolerance, preserve_topology=True)
        return simplified

    def calculate_precision_area(self, poly: Polygon) -> float:
        """
        Calculates area in Square Feet with ellipsoidal correction.
        """
        # abs() handles ring orientation; 10.7639 converts sq m to sq ft
        area_sq_m, _ = self.geod.geometry_area_perimeter(poly)
        return abs(area_sq_m) * 10.7639
