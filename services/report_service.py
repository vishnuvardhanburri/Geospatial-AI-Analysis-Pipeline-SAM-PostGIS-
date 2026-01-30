from repositories.geospatial_repository import GeospatialRepository
from core.pdf_generator import PDFGenerator

class ReportService:
    def __init__(self, repo: GeospatialRepository = Depends()):
        self.repo = repo
        self.pdf_engine = PDFGenerator()

    def generate_final_report(self, task_id: UUID, tenant_id: UUID):
        # 1. Fetch validated spatial data with area calculations
        features = self.repo.get_features_by_task(task_id, tenant_id)
        
        if not features:
            raise ValueError("No validated geospatial data found for this task.")

        # 2. Map data into a structured material estimate
        estimates = self._compute_material_estimates(features)

        # 3. Generate immutable PDF deliverable
        report_path = self.pdf_engine.create_document(
            task_id=task_id,
            features=features,
            estimates=estimates
        )
        
        return report_path

    def _compute_material_estimates(self, features):
        """
        Business logic for converting detected areas into cost estimates.
        """
        # Example: Applying cost-per-sq-ft logic based on feature type
        rates = {"mulch": 3.50, "lawn": 1.25, "patio": 15.00}
        return [
            {"type": f.feature_type, "cost": f.area_sq_ft * rates.get(f.feature_type, 0)}
            for f in features
        ]
