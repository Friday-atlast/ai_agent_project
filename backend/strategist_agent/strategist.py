import logging
from backend.strategist_agent.tools.ocr_model import OCRModel # OCRModel ko import karein

class Strategist:
    """
    Yeh Strategist Agent class hai.
    Yeh campaign details ko analyze karegi aur ek action plan banayegi.
    """
    def __init__(self, config):
        """
        Strategist ko initialize karta hai.
        Args:
            config (dict): Application ki configuration settings.
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Strategist Agent initialized with provided configuration.")

        # OCRModel tool ko initialize karein
        self.ocr_model = OCRModel(config) # OCRModel ko yahan initialize kar rahe hain.


    def run(self, campaign_details: dict) -> dict:
        """
        Strategist agent ka mukhya execution method.
        Campaign details ko analyze karta hai aur ek action plan banata hai.

        Args:
            campaign_details (dict): Manager se mila campaign details.

        Returns:
            dict: Strategist ka output (action plan).
            {"status": "success", "action_plan": {...}, "message": "..."}
            {"status": "error", "message": "..."}
        """
        campaign_id = campaign_details.get("campaign_id", "unknown_campaign")
        self.logger.info(f"[{campaign_id}] Strategist Agent: Starting analysis for campaign.")
        
        # Abhi ke liye, hum yahan sirf OCRModel ko test karenge.
        # Future mein yahan par saare Strategist tools ka workflow hoga.
        
        input_type = campaign_details.get("input_type")
        input_data = campaign_details.get("input_data")

        if input_type == "screenshot":
            self.logger.info(f"[{campaign_id}] Strategist Agent: Processing screenshot input for OCR.")
            ocr_result = self.ocr_model.extract_text_from_image(input_data, "base64") # Assuming base64 for now
            
            if ocr_result["status"] == "success":
                self.logger.info(f"[{campaign_id}] Strategist Agent: OCR successful. Extracted text length: {len(ocr_result['extracted_text'])} characters.")
                # Yahan extracted text ko aage ke tools (e.g., Requirement Extraction) ko pass kiya jayega
                return {"status": "success", "action_plan": {"extracted_text": ocr_result["extracted_text"]}, "message": "Strategist processed screenshot successfully."}
            else:
                self.logger.error(f"[{campaign_id}] Strategist Agent: OCR failed: {ocr_result['message']}")
                return {"status": "error", "message": f"Strategist failed to process screenshot: {ocr_result['message']}"}
        else:
            self.logger.warning(f"[{campaign_id}] Strategist Agent: Input type '{input_type}' not yet fully supported. Returning placeholder.")
            # Future mein yahan text_file, discord_link handle honge
            return {"status": "success", "action_plan": {"research_keywords": ["placeholder"]}, "message": "Strategist completed (placeholder for other input types)."}