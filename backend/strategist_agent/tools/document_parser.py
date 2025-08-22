import logging
import requests
import fitz # PyMuPDF library
import docx
import os
import io

logger = logging.getLogger(__name__)

class DocumentParser:
    """
    Yeh class text files, PDF, DOCX, aur URLs se content extract karne ke liye hai.
    """
    def __init__(self, config):
        """
        DocumentParser ko initialize karta hai.
        Args:
            config (dict): Application ki configuration settings.
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("DocumentParser initialized.")

    def extract_text(self, input_data: str, input_type: str) -> dict:
        """
        File path ya URL se text extract karta hai.

        Args:
            input_data (str): Local file path ya URL.
            input_type (str): 'text_file', 'pdf_file', 'docx_file', 'url'

        Returns:
            dict: Extracted text aur status.
            {"status": "success", "extracted_text": "...", "message": "Text extracted successfully."}
            {"status": "error", "message": "Error message"}
        """
        try:
            extracted_text = ""
            
            if input_type == "text_file":
                if not os.path.exists(input_data):
                    raise FileNotFoundError(f"File not found at: {input_data}")
                with open(input_data, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
                self.logger.info("Text extracted from TXT file successfully.")

            elif input_type == "pdf_file":
                if not os.path.exists(input_data):
                    raise FileNotFoundError(f"File not found at: {input_data}")
                with fitz.open(input_data) as doc:
                    for page in doc:
                        extracted_text += page.get_text()
                self.logger.info("Text extracted from PDF file successfully.")

            elif input_type == "docx_file":
                if not os.path.exists(input_data):
                    raise FileNotFoundError(f"File not found at: {input_data}")
                doc = docx.Document(input_data)
                for para in doc.paragraphs:
                    extracted_text += para.text + '\n'
                self.logger.info("Text extracted from DOCX file successfully.")

            elif input_type == "url" or input_type == "discord_link":
                self.logger.info(f"Fetching content from URL: {input_data}")
                response = requests.get(input_data, timeout=10)
                response.raise_for_status() # HTTP errors ke liye exception raise karein
                extracted_text = response.text
                self.logger.info("Content from URL fetched successfully.")

            else:
                raise ValueError(f"Unsupported input type: {input_type}")

            return {"status": "success", "extracted_text": extracted_text.strip(), "message": "Text extracted successfully."}

        except FileNotFoundError as e:
            self.logger.error(f"File not found error: {e}", exc_info=True)
            return {"status": "error", "message": f"File not found: {e}"}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network request error: {e}", exc_info=True)
            return {"status": "error", "message": f"Could not fetch content from URL: {e}"}
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return {"status": "error", "message": f"Failed to extract text: {e}"}