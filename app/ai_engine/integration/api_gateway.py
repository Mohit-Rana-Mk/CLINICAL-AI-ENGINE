from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from app.ai_engine.orchestrator import ClinicalAIEngine
from app.ai_engine.integration.auth_handler import AuthHandler
from app.ai_engine.integration.response_mapper import ResponseMapper

router = APIRouter(prefix="/ai", tags=["Multimodal Processing"])
ai_engine = ClinicalAIEngine()
auth = AuthHandler()

@router.post("/analyze")
def analyze_text(
    message: str = Form(...),
    patient_id: Optional[int] = Form(None),
    auth_user: dict = Depends(auth.verify_token)
):
    result = ai_engine.process(message=message, patient_id=patient_id)
    return ResponseMapper.map_to_healtrack(result)

@router.post("/voice")
async def analyze_voice(
    file: UploadFile = File(...),
    patient_id: Optional[int] = Form(None),
    auth_user: dict = Depends(auth.verify_token)
):
    result = ai_engine.process(file_name=file.filename, patient_id=patient_id, mime_type=file.content_type)
    return ResponseMapper.map_to_healtrack(result)

@router.post("/image")
async def analyze_image(
    file: UploadFile = File(...),
    patient_id: Optional[int] = Form(None),
    auth_user: dict = Depends(auth.verify_token)
):
    result = ai_engine.process(file_name=file.filename, patient_id=patient_id, mime_type=file.content_type)
    return ResponseMapper.map_to_healtrack(result)

@router.post("/ocr")
async def analyze_ocr(
    file: UploadFile = File(...),
    patient_id: Optional[int] = Form(None),
    auth_user: dict = Depends(auth.verify_token)
):
    result = ai_engine.process(file_name=file.filename, patient_id=patient_id, mime_type=file.content_type)
    return ResponseMapper.map_to_healtrack(result)

@router.get("/timeline/{patient_id}")
def get_timeline(patient_id: int, auth_user: dict = Depends(auth.verify_token)):
    result = ai_engine.process(message="fetch timeline status", patient_id=patient_id)
    return {"status": "success", "patient_id": patient_id, "timeline": result.get("timeline", [])}

@router.get("/history/{patient_id}")
def get_history(patient_id: int, auth_user: dict = Depends(auth.verify_token)):
    result = ai_engine.process(message="fetch history", patient_id=patient_id)
    return {"status": "success", "patient_id": patient_id, "conversation_history": result.get("conversation_history", [])}

@router.get("/summary/{patient_id}")
def get_summary(patient_id: int, auth_user: dict = Depends(auth.verify_token)):
    result = ai_engine.process(message="generate summary", patient_id=patient_id)
    return {"status": "success", "patient_id": patient_id, "clinical_summary": result.get("clinical_summary", {})}

@router.get("/recommendations/{patient_id}")
def get_recommendations(patient_id: int, auth_user: dict = Depends(auth.verify_token)):
    result = ai_engine.process(message="fetch recommendations", patient_id=patient_id)
    return {"status": "success", "patient_id": patient_id, "recommendation": result.get("recommendation", {})}