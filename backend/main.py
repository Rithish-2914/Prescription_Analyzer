from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from parser import parse_prescription, generate_simple_explanation
from ocr import extract_text_from_image

app = FastAPI(title="Prescription Explainer API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExplainRequest(BaseModel):
    prescription_text: str

@app.post("/explain")
async def explain_prescription(
    prescription_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Endpoint to explain a prescription.
    Accepts either raw text via form data OR an image file for OCR.
    """
    text_to_process = ""

    # Priority 1: Use provided text
    if prescription_text:
        text_to_process = prescription_text
    # Priority 2: Use Image OCR
    elif file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File provided is not an image.")
        
        image_bytes = await file.read()
        extracted_text = extract_text_from_image(image_bytes)
        
        # Check if OCR failed
        if extracted_text.startswith("ERROR_OCR_FAILED"):
             raise HTTPException(status_code=500, detail=extracted_text)
             
        text_to_process = extracted_text
    else:
        raise HTTPException(status_code=400, detail="Must provide either text or an image file.")

    if not text_to_process.strip():
        raise HTTPException(status_code=400, detail="No text found to process.")

    # 1. Parse the text into structured data
    structured_data = parse_prescription(text_to_process)
    
    # 2. Generate the simple explanation
    simple_explanation = generate_simple_explanation(structured_data)
    
    # Add the extracted text back to the response context if it came from OCR
    if file:
        structured_data["extracted_text_from_ocr"] = text_to_process

    return {
        "simple_explanation": simple_explanation,
        "structured_data": structured_data
    }

@app.get("/")
def read_root():
    return {"message": "Prescription Explainer API is running."}
