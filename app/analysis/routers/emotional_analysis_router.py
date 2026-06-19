from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.analysis.schemas.emotional_analysis_create import (
    EmotionalAnalysisCreate
)

from app.analysis.schemas.emotional_analysis_response import (
    EmotionalAnalysisResponse
)

from app.analysis.services.emotional_analysis_service import (
    create_analysis as create_analysis_service,
    get_analysis as get_analysis_service
)

from app.analysis.services.emotional_analysis_service import (
    create_analysis_from_entry
)

from app.analysis.schemas.weekly_summary_response import (
    WeeklySummaryResponse
)

from app.analysis.services.weekly_summary_service import (
    get_weekly_summary
)

router = APIRouter(
    prefix="/analysis",
    tags=["Emotional Analysis"]
)


@router.post(
    "/entries/{entry_id}",
    response_model=EmotionalAnalysisResponse
)
def create_analysis(
    entry_id: int,
    data: EmotionalAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_analysis_service(
        entry_id=entry_id,
        current_user_id=current_user.id,
        data=data,
        db=db
    )

@router.get(
    "/entries/{entry_id}",
    response_model=EmotionalAnalysisResponse
)
def get_analysis(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_analysis_service(
        entry_id=entry_id,
        current_user_id=current_user.id,
        db=db
    )
    
@router.post(
    "/entries/{entry_id}/auto",
    response_model=EmotionalAnalysisResponse
)
def auto_analyze(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_analysis_from_entry(
        entry_id=entry_id,
        current_user_id=current_user.id,
        db=db
    )
    
@router.get(
    "/weekly-summary",
    response_model=WeeklySummaryResponse
)
def weekly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_weekly_summary(
        current_user.id,
        db
    )