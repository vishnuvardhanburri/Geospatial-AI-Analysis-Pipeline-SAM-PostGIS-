import pytest
from shapely.geometry import Polygon
from core.geometry import GeometryProcessor

def test_area_consistency_after_simplification():
    """
    Requirement: Area deviation must be < 1% post-simplification.
    Ensures that "cleaning" the polygon doesn't skew financial estimates.
    """
    processor = GeometryProcessor()
    
    # Define a complex, "jagged" 100x100ft square with noise
    jagged_coords = [
        (0, 0), (5, 0.1), (10, 0), (10, 5), (10.1, 10), 
        (5, 9.9), (0, 10), (0.1, 5), (0, 0)
    ]
    raw_poly = Polygon(jagged_coords)
    
    # 1. Calculate original area
    original_area = processor.calculate_precision_area(raw_poly)
    
    # 2. Apply simplification logic
    simplified_poly = processor.simplify_polygon(raw_poly, tolerance=0.05)
    new_area = processor.calculate_precision_area(simplified_poly)
    
    # 3. Validation Logic
    deviation = abs(original_area - new_area) / original_area
    
    print(f"Original Area: {original_area:.2f} sq ft")
    print(f"Simplified Area: {new_area:.2f} sq ft")
    print(f"Deviation: {deviation:.4%}")

    assert deviation < 0.01, f"Area deviation {deviation:.2%} exceeds 1% threshold"
