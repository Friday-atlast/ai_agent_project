import logging
from backend.strategist_agent.strategist import Strategist # Strategist class ko import karein

class Manager:
    """
    Yeh AI Agent Manager class hai.
    Yeh poore content creation workflow ko orchestrate karegi.
    """
    def __init__(self, config):
        """
        Manager ko initialize karta hai.
        Args:
            config (dict): Application ki configuration settings.
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Manager initialized with provided configuration.")

        # Strategist Agent ko initialize karein
        self.strategist_agent = Strategist(config)
        self.logger.info("Strategist Agent initialized within Manager.")

        self.campaigns = {} # Active campaigns ka record.
        self.workflow_status = {} # Har campaign ke workflow ka status.

    def start_campaign_workflow(self, campaign_details):
        """
        Ek naye campaign workflow ko shuru karta hai.
        Yeh method Strategist agent ko campaign details pass karega
        aur fir poore pipeline ko manage karega.

        Args:
            campaign_details (dict): Campaign ki saari jaankari.
        Returns:
            dict: Campaign processing status aur results ka summary.
        """
        campaign_id = campaign_details.get("campaign_id", "default_id")
        campaign_name = campaign_details.get("campaign_name", "Unnamed Campaign")
        
        self.logger.info(f"[{campaign_id}] Starting workflow for campaign: {campaign_name}")
        
        try:
            # Step 1: Strategist Agent ko call karein
            self.logger.info(f"[{campaign_id}] Calling Strategist Agent with campaign details...")
            strategist_output = self.strategist_agent.run(campaign_details)
            
            if strategist_output["status"] == "error":
                raise Exception(f"Strategist Agent failed: {strategist_output.get('message', 'Unknown error')}")
            
            self.logger.info(f"[{campaign_id}] Strategist Agent finished. Action Plan created: {strategist_output.get('action_plan', 'No plan found')}")

            # Step 2: Researcher Agent ko call karein (Placeholder)
            self.logger.info(f"[{campaign_id}] Calling Researcher Agent with action plan...")
            # researcher_output = self.researcher_agent.run(strategist_output["action_plan"]) # Future mein aise call hoga
            researcher_output = {"status": "success", "videos": "placeholder"} # Abhi ke liye placeholder

            if researcher_output["status"] == "error":
                raise Exception(f"Researcher Agent failed: {researcher_output.get('message', 'Unknown error')}")

            self.logger.info(f"[{campaign_id}] Researcher Agent finished. Videos found.")

            # Is tarah se aage ke agents ko call kiya jayega.
            
            self.logger.info(f"[{campaign_id}] Campaign workflow completed successfully.")
            return {"status": "success", "message": "Campaign workflow initiated successfully.", "campaign_id": campaign_id}
            
        except Exception as e:
            self.logger.error(f"[{campaign_id}] Critical error in campaign workflow: {e}", exc_info=True)
            return {"status": "error", "message": f"Campaign workflow failed: {e}"}