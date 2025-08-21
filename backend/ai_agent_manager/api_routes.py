from flask import Flask, request, jsonify
from flask_cors import CORS # CORS handling ke liye
import logging

# Flask application instance banayein
app = Flask(__name__)
# CORS ko enable karein sabhi origins ke liye (development ke liye theek hai)
CORS(app)

logger = logging.getLogger(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    """
    Ek simple health check endpoint jo server ki up-status batata hai.
    """
    logger.info("Health check requested.")
    return jsonify({"status": "healthy", "message": "AI Agent Backend is running."}), 200

@app.route("/start_campaign", methods=["POST"])
def start_campaign():
    """
    Campaign workflow ko shuru karne ke liye endpoint.
    Frontend se campaign details JSON format mein receive karega.
    """
    data = request.get_json()
    if not data:
        logger.warning("No JSON data received for /start_campaign.")
        return jsonify({"status": "error", "message": "Request must contain JSON data."}), 400

    campaign_details = data.get("campaign_details")
    if not campaign_details:
        logger.warning("Missing 'campaign_details' in /start_campaign request.")
        return jsonify({"status": "error", "message": "Missing 'campaign_details' in request."}), 400

    # Manager instance ko Flask app ke config se access karein
    ai_manager = app.config.get('AI_MANAGER')
    if not ai_manager:
        logger.critical("AI Manager instance not found in app config.")
        return jsonify({"status": "error", "message": "Server error: AI Manager not initialized."}), 500

    logger.info(f"Received campaign request: {campaign_details.get('campaign_name', 'Unnamed')}")

    # Manager ke workflow ko trigger karein
    result = ai_manager.start_campaign_workflow(campaign_details)

    return jsonify(result), 200

# Future mein yahan aur routes add kiye jayenge