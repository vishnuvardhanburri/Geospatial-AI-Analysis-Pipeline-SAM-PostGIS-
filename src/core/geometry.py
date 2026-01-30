import pyproj
from shapely.geometry import Polygon

class GeometryProcessor:
    def __init__(self):
        # Using Albers Equal Area for financial-grade SqFt accuracy
        self.geod = pyproj.Geod(ellps="WGS84")

    def refine_and_measure(self, raw_coords, tolerance=0.05):
        # 1. Transform jagged AI mask to professional clean-line polygon
        poly = Polygon(raw_coords)
        simplified = poly.simplify(tolerance, preserve_topology=True)
        
        # 2. Precise Area Calculation (Sq Meters to Sq Feet)
        area_sq_m, _ = self.geod.geometry_area_perimeter(simplified)
        return {
            "area_sq_ft": abs(area_sq_m) * 10.7639,
            "geojson": simplified.__geo_interface__
        }
