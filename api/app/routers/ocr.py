from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except Exception:
    TESSERACT_AVAILABLE = False

router = APIRouter()

@router.post("/prescription")
async def ocr_prescription(file: UploadFile = File(...)):
    content = await file.read()
    try:
        image = Image.open(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")

    raw_text = ""
    if TESSERACT_AVAILABLE:
        try:
            raw_text = pytesseract.image_to_string(image)
        except Exception:
            raw_text = ""

    return {
        "raw_text": raw_text or "",
        "medications": []
    }


