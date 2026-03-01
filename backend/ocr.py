import pytesseract
from PIL import Image
import io

# You may need to specify the path to tesseract executable if it's not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an uploaded image using Tesseract OCR.
    """
    try:
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Simple preprocessing check (just ensuring it can be read as Grayscale helps sometimes)
        image = image.convert('L')
        
        # Extract text
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        # Return a custom error message indicating OCR failed or isn't installed
        return f"ERROR_OCR_FAILED: {str(e)}\n\nPlease ensure Tesseract OCR is installed and added to your system PATH."

# Optional debug block
if __name__ == "__main__":
    print("OCR module loaded.")
