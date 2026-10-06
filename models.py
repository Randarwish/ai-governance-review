from typing import Literal
from pydantic import BaseModel, Field


class RequirementResult(BaseModel):
    requirement_id: str
    title: str
    status: Literal[
        "Compliant",
        "Gap",
        "Review Required",
        "Not Applicable"
    ]
    evidence: str
    recommendation: str


class Assessment(BaseModel):
    use_case_type: str
    risk_level: Literal["Low", "Medium", "High", "Critical"]
    risk_score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)

    summary: str
    requirements: list[RequirementResult]
    risks: list[str]
    actions: list[str]
