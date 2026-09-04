from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.verification_service import verification_service

router = APIRouter(prefix="/credentials", tags=["Credentials"])

class IssueCredentialRequest(BaseModel):
    student_id: str
    degree_name: str
    issue_date: str  # Format: YYYY-MM-DD

class VerifyCredentialRequest(BaseModel):
    student_id: str
    degree_name: str
    issue_date: str

@router.post("/issue", status_code=status.HTTP_201_CREATED)
def issue_credential(payload: IssueCredentialRequest):
    try:
        result = verification_service.issue_credential(
            student_id=payload.student_id,
            degree_name=payload.degree_name,
            issue_date=payload.issue_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify")
def verify_credential(payload: VerifyCredentialRequest):
    try:
        result = verification_service.verify_credential(
            student_id=payload.student_id,
            degree_name=payload.degree_name,
            issue_date=payload.issue_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))