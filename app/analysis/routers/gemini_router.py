from fastapi import APIRouter

from app.analysis.schemas.gemini_analysis_request import (
    GeminiAnalysisRequest
)

from app.analysis.services.gemini_service import (
    call_gemini
)

router = APIRouter(
    prefix="/analysis",
    tags=["Gemini Analysis"]
)


@router.post("/test")
def test_gemini(
    data: GeminiAnalysisRequest
):

    result = call_gemini(data.texto)

    return result