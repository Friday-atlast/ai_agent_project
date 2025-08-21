import io
import pytesseract
from PIL import Image
import os
import logging
import base64

logger = logging.getLogger(__name__)

class OCRModel:
    """
    Yeh class images (screenshots) se text extract karne ke liye zimmedar hai.
    Google ke Tesseract OCR engine ka upyog karta hai.
    """
    def __init__(self, config):
        """
        OCRModel ko initialize karta hai.
        Args:
            config (dict): Application ki configuration settings.
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("OCRModel initialized.")

        # Tesseract executable ka path configure karein agar system PATH mein nahi hai
        # Example (Windows): pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # Agar Tesseract PATH mein hai, to is line ki zaroorat nahi hai.
        tesseract_path = self.config.get("paths", {}).get("tesseract_cmd", None)
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            self.logger.info(f"Tesseract CMD path set to: {tesseract_path}")
        else:
            self.logger.warning("Tesseract CMD path not explicitly set or not found. Assuming Tesseract is in system PATH.")


    def extract_text_from_image(self, image_input: str, input_type: str) -> dict:
        """
        Image se text extract karta hai.
        Image input base64 string ya local file path ho sakta hai.

        Args:
            image_input (str): Base64 encoded image string ya local image file ka path.
            input_type (str): 'base64' ya 'filepath'.

        Returns:
            dict: Extracted text aur status.
            {"status": "success", "extracted_text": "...", "message": "Text extracted successfully."}
            {"status": "error", "message": "Error message"}
        """
        try:
            image = None
            if input_type == "base64":
                # Base64 string ko decode karke image load karein
                image_bytes = base64.b64decode(image_input)
                image = Image.open(io.BytesIO(image_bytes))
                self.logger.info("Image loaded from base64 string.")
            elif input_type == "filepath":
                # File path se image load karein
                if not os.path.exists(image_input):
                    raise FileNotFoundError(f"Image file not found at: {image_input}")
                image = Image.open(image_input)
                self.logger.info(f"Image loaded from filepath: {image_input}")
            else:
                raise ValueError("Invalid input_type. Must be 'base64' or 'filepath'.")

            if image is None:
                raise ValueError("Failed to load image.")

            # OCR process
            extracted_text = pytesseract.image_to_string(image)
            self.logger.info("Text extraction successful.")

            return {"status": "success", "extracted_text": extracted_text.strip(), "message": "Text extracted successfully."}

        except FileNotFoundError as e:
            self.logger.error(f"OCR Error: File not found - {e}", exc_info=True)
            return {"status": "error", "message": f"Image file not found: {e}"}
        except pytesseract.TesseractNotFoundError:
            self.logger.critical("Tesseract is not installed or not in your PATH. Please install Tesseract OCR engine.")
            return {"status": "error", "message": "Tesseract OCR engine not found. Please install it."}
        except Exception as e:
            self.logger.error(f"OCR Error: An unexpected error occurred - {e}", exc_info=True)
            return {"status": "error", "message": f"Failed to extract text: {e}"}