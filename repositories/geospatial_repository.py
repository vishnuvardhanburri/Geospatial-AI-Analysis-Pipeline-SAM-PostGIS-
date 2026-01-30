import json
from sqlalchemy.orm import Session
from models.geospatial import LandscapeFeature
from geoalchemy2.functions import ST_GeomFromGeoJSON

class GeospatialRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_validated_features(self, task_id: str, tenant_id: str, features: list):
        """
        Atomic insertion of AI-detected features with PostGIS spatial indexing.
        Ensures measurement data is persistent and queryable.
        """
        for feat in features:
            # Convert Python dict geometry to PostGIS format using ST_GeomFromGeoJSON
            new_feature = LandscapeFeature(
                tenant_id=tenant_id,
                task_id=task_id,
                feature_type=feat["type"],
                confidence_score=feat["confidence"],
                geometry=ST_GeomFromGeoJSON(json.dumps(feat["geometry"])),
                area_sq_ft=feat["area"],
                metadata_json=feat.get("raw_meta")
            )
            self.session.add(new_feature)
        
        # Commit ensures transaction integrity
        self.session.commit()
