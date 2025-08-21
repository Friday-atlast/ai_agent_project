import os
import toml
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load configuration from config.toml
try:
    config = toml.load("config.toml")
    logger.info("Configuration loaded from config.toml")
except FileNotFoundError:
    logger.error("config.toml not found. Please create one.")
    exit(1)
except Exception as e:
    logger.error(f"Error loading config.toml: {e}")
    exit(1)

# Ensure data directories exist as per config
data_base_path = config.get("paths", {}).get("data_dir", "backend/data")
os.makedirs(os.path.join(data_base_path, "media"), exist_ok=True)
os.makedirs(os.path.join(data_base_path, "raw_videos"), exist_ok=True)
os.makedirs(os.path.join(data_base_path, "final_videos"), exist_ok=True)
logger.info(f"Data directories ensured at: {data_base_path}")

# Import Flask app and Manager after configuration and logging setup
# This ensures that manager and routes have access to configured settings
from backend.ai_agent_manager.api_routes import app
from backend.ai_agent_manager.manager import Manager

# Initialize the AI Agent Manager
try:
    ai_manager = Manager(config)
    logger.info("AI Agent Manager initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize AI Agent Manager: {e}")
    exit(1)

# Add manager instance to Flask app if needed for routes to access it
app.config['AI_MANAGER'] = ai_manager

if __name__ == "__main__":
    flask_host = config.get("server", {}).get("host", "0.0.0.0")
    flask_port = config.get("server", {}).get("port", 5000)
    flask_debug = config.get("server", {}).get("debug", False)

    logger.info(f"Starting Flask development server on {flask_host}:{flask_port} (Debug: {flask_debug})")
    try:
        app.run(host=flask_host, port=flask_port, debug=flask_debug)
    except Exception as e:
        logger.critical(f"Flask server failed to start: {e}")