from typing import Optional

from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    effective_date: str
    jurisdiction: str = "Not specified"
    additional_instructions: Optional[str] = ""


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    demo_mode: bool
    warning: str