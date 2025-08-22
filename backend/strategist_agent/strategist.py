import logging
from backend.strategist_agent.tools.ocr_model import OCRModel
from backend.strategist_agent.tools.document_parser import DocumentParser
from backend.strategist_agent.tools.requirement_extractor import RequirementExtractor # Nayi import

class Strategist:
    """
    Yeh Strategist Agent class hai.
    Yeh campaign details ko analyze karegi aur ek action plan banayegi.
    """
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Strategist Agent initialized with provided configuration.")

        # Tools ko initialize karein
        self.ocr_model = OCRModel(config)
        self.document_parser = DocumentParser(config)
        self.requirement_extractor = RequirementExtractor(config) # Naya tool initialize hua

    def run(self, campaign_details: dict) -> dict:
        """
        Strategist agent ka mukhya execution method.
        """
        campaign_id = campaign_details.get("campaign_id", "unknown_campaign")
        self.logger.info(f"[{campaign_id}] Strategist Agent: Starting analysis for campaign.")
        
        input_type = campaign_details.get("input_type")
        input_data = campaign_details.get("input_data")
        extracted_text = ""

        # Step 1: Input type ke aadhar par sahi tool ka upyog karke content extract karein
        if input_type == "screenshot":
            self.logger.info(f"[{campaign_id}] Strategist Agent: Processing screenshot input for OCR.")
            result = self.ocr_model.extract_text_from_image(input_data, "base64")
        elif input_type in ["text_file", "pdf_file", "docx_file", "url", "discord_link"]:
            self.logger.info(f"[{campaign_id}] Strategist Agent: Processing document/URL input.")
            result = self.document_parser.extract_text(input_data, input_type)
        else:
            self.logger.warning(f"[{campaign_id}] Strategist Agent: Input type '{input_type}' not supported. Returning placeholder.")
            return {"status": "error", "message": f"Unsupported input type: {input_type}"}

        if result["status"] == "error":
            self.logger.error(f"[{campaign_id}] Strategist Agent: Content extraction failed: {result['message']}")
            return {"status": "error", "message": f"Strategist failed to process input: {result['message']}"}

        extracted_text = result["extracted_text"]
        self.logger.info(f"[{campaign_id}] Strategist Agent: Content extraction successful. Extracted text length: {len(extracted_text)} characters.")
        
        # Step 2: Extracted text se requirements nikalne ke liye naye tool ko call karein
        self.logger.info(f"[{campaign_id}] Strategist Agent: Calling Requirement Extractor.")
        extraction_result = self.requirement_extractor.extract(extracted_text)
        
        if extraction_result["status"] == "error":
            self.logger.error(f"[{campaign_id}] Strategist Agent: Requirement extraction failed: {extraction_result['message']}")
            return {"status": "error", "message": f"Strategist failed to extract requirements: {extraction_result['message']}"}
        
        extracted_requirements = extraction_result["requirements"]
        self.logger.info(f"[{campaign_id}] Strategist Agent: Requirements extracted successfully: {extracted_requirements}")

        # Final action plan banayein aur return karein
        action_plan = {
            "extracted_text": extracted_text,
            "product": extracted_requirements.get("product"),
            "audience": extracted_requirements.get("audience"),
            "research_keywords": extracted_requirements.get("research_keywords", [])
        }
        
        return {"status": "success", "action_plan": action_plan, "message": "Strategist successfully analyzed the campaign."}