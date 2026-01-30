from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from geoalchemy2 import Geometry
from db.base import Base
import uuid

class LandscapeFeature(Base):
    __tablename__ = "landscape_features"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)  # Enforces Multi-tenancy
    task_id = Column(UUID(as_uuid=True), index=True)
    
    feature_type = Column(String(50), nullable=False) # mulch, lawn, patio
    confidence_score = Column(Float, nullable=False)
    
    # PostGIS Geometry column (EPSG:4326 for WGS84)
    geometry = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    
    area_sq_ft = Column(Float, nullable=False)
    metadata_json = Column(JSONB)  # Stores raw AI model metadata for auditability
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
