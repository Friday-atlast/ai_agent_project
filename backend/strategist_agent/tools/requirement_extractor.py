import logging
import re

class RequirementExtractor:
    """
    Yeh class raw text se campaign requirements ko extract karne ke liye hai.
    """
    def __init__(self, config):
        """
        RequirementExtractor ko initialize karta hai.
        Args:
            config (dict): Application ki configuration settings.
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("RequirementExtractor initialized.")

    def extract(self, raw_text: str) -> dict:
        """
        Raw text se mukhya jaankari (product, audience, keywords) extract karta hai.

        Args:
            raw_text (str): OCR ya Document Parser se mila raw text.

        Returns:
            dict: Extracted requirements aur status.
            {"status": "success", "requirements": {...}, "message": "..."}
            {"status": "error", "message": "..."}
        """
        try:
            self.logger.info("Starting requirement extraction from raw text.")
            
            # Text ko lowercase mein badal dein aur extra spaces hata dein
            processed_text = raw_text.lower().strip()
            
            # Rule-based extraction ke liye keywords define karein
            # Yeh keywords "config.toml" se bhi a sakte hain
            product_keywords = ["product:", "product name:", "software:", "tool:", "ai solution:", "ai software:"]
            audience_keywords = ["audience:", "target audience:", "demographic:"]
            
            # Keywords extraction ke liye placeholders
            product = None
            audience = None
            research_keywords = []

            # 1. Product aur Audience extract karein
            for line in processed_text.split('\n'):
                line = line.strip()
                if not line:
                    continue

                for kw in product_keywords:
                    if line.startswith(kw):
                        product = line.replace(kw, '').strip().title()
                        self.logger.info(f"Product extracted: {product}")
                        break
                
                for kw in audience_keywords:
                    if line.startswith(kw):
                        audience = line.replace(kw, '').strip().title()
                        self.logger.info(f"Audience extracted: {audience}")
                        break

            # 2. Keywords extract karein (ek simple heuristic ka upyog karke)
            # Hum ek regex ka upyog karke kisi bhi line ke baad aane wale comma-separated words ko nikalenge
            
            # Ek simple regex pattern jo "keywords:" ya "tags:" ke baad words ko nikalta hai
            keywords_match = re.search(r'(keywords:|tags:)(.*)', processed_text)
            if keywords_match:
                keywords_str = keywords_match.group(2).strip()
                research_keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
                self.logger.info(f"Keywords extracted: {research_keywords}")

            # Agar koi keywords nahi mile, to product aur audience ko keywords ke roop mein add karein
            if not research_keywords and product:
                research_keywords.append(product)
            if not research_keywords and audience:
                research_keywords.append(audience)

            # Ek final check karein ki zaroori jaankari mili hai ya nahi
            if not product and not audience:
                self.logger.warning("Could not extract main product or audience from the text.")
            
            extracted_requirements = {
                "product": product,
                "audience": audience,
                "research_keywords": research_keywords
            }
            
            self.logger.info(f"Requirement extraction finished. Final requirements: {extracted_requirements}")

            return {"status": "success", "requirements": extracted_requirements, "message": "Requirements extracted successfully."}

        except Exception as e:
            self.logger.error(f"An unexpected error occurred during requirement extraction: {e}", exc_info=True)
            return {"status": "error", "message": f"Failed to extract requirements: {e}"}