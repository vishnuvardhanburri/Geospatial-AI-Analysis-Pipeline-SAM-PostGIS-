from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from services.report_service import ReportService
from schemas.report import ReportResponse

router = APIRouter(prefix="/v1/reports", tags=["reporting"])

@router.post("/{task_id}/generate", response_model=ReportResponse, status_code=status.HTTP_202_ACCEPTED)
def trigger_report_generation(
    task_id: UUID,
    tenant_id: UUID, # Extracted from JWT context in production
    service: ReportService = Depends()
):
    """
    Triggers the asynchronous generation of a production-grade PDF report.
    Ensures that reporting logic is decoupled from primary API execution.
    """
    try:
        report_meta = service.queue_report(task_id, tenant_id)
        return report_meta
    except Exception as exc:
        # Error handling must be explicit and structured
        logger.exception(f"Failed to queue report for task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not initialize report generation."
        )
