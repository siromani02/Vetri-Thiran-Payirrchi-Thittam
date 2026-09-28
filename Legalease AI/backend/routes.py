from fastapi import APIRouter, HTTPException

from backend.schemas import DocumentRequest, DocumentResponse
from backend.services.ai_generator import GeminiDocumentGenerator


router = APIRouter(
    prefix="/api",
    tags=["documents"],
)

generator = GeminiDocumentGenerator()

LEGAL_WARNING = (
    "This document is an AI-generated draft for informational purposes only. "
    "Review it with a qualified legal professional before signing."
)


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate(
    request: DocumentRequest,
) -> DocumentResponse:

    try:
        content = generator.generate(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            additional_instructions=(
                request.additional_instructions or ""
            ),
        )

        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            demo_mode=generator.demo_mode,
            warning=LEGAL_WARNING,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}",
        ) from exc