from flask import Flask, request, jsonify
from flask_cors import CORS
from jsonschema import validate, ValidationError
import logging
from backend.ai_agent_manager.data_schema import get_campaign_details_schema, get_agent_response_schema

# Flask application instance banayein
app = Flask(__name__)
# CORS ko enable karein sabhi origins ke liye (development ke liye theek hai)
CORS(app)
logger = logging.getLogger(__name__)

# --- API Specification ---
# Base URL: http://localhost:5000/api
# Version: v1

@app.route("/api/v1/health", methods=["GET"])
def health_check():
    """
    Ek simple health check endpoint jo server ki up-status batata hai.
    """
    logger.info("Health check requested.")
    return jsonify({"status": "healthy", "message": "AI Agent Backend is running."}), 200

@app.route("/api/v1/campaigns", methods=["POST"])
def create_campaign():
    """
    Naya campaign shuru karne ke liye endpoint.
    Frontend se campaign details JSON format mein receive karega.
    """
    # 1. JSON Request Body ko check karein
    data = request.get_json()
    if not data:
        logger.warning("No JSON data received for /api/v1/campaigns.")
        return jsonify({"status": "error", "message": "Request must contain JSON data."}), 400

    # 2. Schema Validation karein
    campaign_details = data.get("campaign_details")
    if not campaign_details:
        logger.warning("Missing 'campaign_details' in /api/v1/campaigns request.")
        return jsonify({"status": "error", "message": "Missing 'campaign_details' in request."}), 400

    schema = get_campaign_details_schema()
    try:
        validate(instance=campaign_details, schema=schema)
    except ValidationError as e:
        logger.error(f"Validation error: {e.message}", exc_info=True)
        return jsonify({"status": "error", "message": f"Invalid campaign data: {e.message}"}), 400

    # 3. Manager instance ko access karein
    ai_manager = app.config.get('AI_MANAGER')
    if not ai_manager:
        logger.critical("AI Manager instance not found in app config.")
        return jsonify({"status": "error", "message": "Server error: AI Manager not initialized."}), 500

    # 4. Manager ke workflow ko trigger karein
    try:
        logger.info(f"Received campaign request: {campaign_details.get('campaign_name', 'Unnamed')}")
        result = ai_manager.start_campaign_workflow(campaign_details)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"An unexpected error occurred in the campaign workflow: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "An internal server error occurred."}), 500