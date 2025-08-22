import logging
from backend.strategist_agent.tools.ocr_model import OCRModel
from backend.strategist_agent.tools.document_parser import DocumentParser

class Strategist:
    """
    Yeh Strategist Agent class hai.
    Yeh campaign details ko analyze karegi aur ek action plan banayegi.
    """
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Strategist Agent initialized with provided configuration.")

        # OCRModel tool ko initialize karein
        self.ocr_model = OCRModel(config)
        self.logger.info("OCRModel initialized within Strategist.")

        # DocumentParser tool ko initialize karein
        self.document_parser = DocumentParser(config)
        self.logger.info("DocumentParser initialized within Strategist.")


    def run(self, campaign_details: dict) -> dict:
        """
        Strategist agent ka mukhya execution method.
        Campaign details ko analyze karta hai aur ek action plan banata hai.
        """
        campaign_id = campaign_details.get("campaign_id", "unknown_campaign")
        self.logger.info(f"[{campaign_id}] Strategist Agent: Starting analysis for campaign.")
        
        input_type = campaign_details.get("input_type")
        input_data = campaign_details.get("input_data")

        # Input type ke aadhar par sahi tool ka upyog karein
        if input_type == "screenshot":
            self.logger.info(f"[{campaign_id}] Strategist Agent: Processing screenshot input for OCR.")
            result = self.ocr_model.extract_text_from_image(input_data, "base64")
            
        elif input_type in ["text_file", "pdf_file", "docx_file", "url", "discord_link"]:
            self.logger.info(f"[{campaign_id}] Strategist Agent: Processing document/URL input.")
            result = self.document_parser.extract_text(input_data, input_type)

        else:
            self.logger.warning(f"[{campaign_id}] Strategist Agent: Input type '{input_type}' not supported. Returning placeholder.")
            return {"status": "error", "message": f"Unsupported input type: {input_type}"}

        # Extracted text ko action plan mein shaamil karein
        if result["status"] == "success":
            extracted_text = result["extracted_text"]
            self.logger.info(f"[{campaign_id}] Strategist Agent: Content extraction successful. Extracted text length: {len(extracted_text)} characters.")
            action_plan = {
                "extracted_text": extracted_text,
                "research_keywords": [] # Isko aage ke dinon mein implement karenge
            }
            return {"status": "success", "action_plan": action_plan, "message": "Strategist processed input successfully."}
        else:
            self.logger.error(f"[{campaign_id}] Strategist Agent: Content extraction failed: {result['message']}")
            return {"status": "error", "message": f"Strategist failed to process input: {result['message']}"}