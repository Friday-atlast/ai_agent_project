# Yeh file data ke structures ko define karti hai
# Taaki alag-alag modules aur agents ke beech data consistency bani rahe.

def get_campaign_details_schema():
    """
    Campaign details ke liye JSON schema return karta hai.
    """
    return {
        "type": "object",
        "properties": {
            "campaign_id": {"type": "string", "description": "Unique ID for the campaign"},
            "campaign_name": {"type": "string", "description": "Name of the campaign"},
            "input_type": {"type": "string", "enum": ["screenshot", "text_file", "discord_link"], "description": "Type of input provided"},
            "input_data": {"type": "string", "description": "Base64 encoded image data, file path, or URL"},
            "required_length_sec": {"type": "string", "description": "Desired video length range (e.g., '15-60s')"},
            "target_product": {"type": "string", "description": "Product name or topic of the campaign"},
            "target_audience": {"type": "string", "description": "Target audience (e.g., 'gamers', 'tech enthusiasts')"},
            "social_media_platforms": {
                "type": "array",
                "items": {"type": "string", "enum": ["youtube", "instagram"]},
                "description": "Platforms to publish to"
            },
            "brand_logo_path": {"type": "string", "nullable": True, "description": "Optional path to brand logo image"}
        },
        "required": ["campaign_name", "input_type", "input_data", "required_length_sec", "target_product", "social_media_platforms"]
    }

def get_agent_response_schema():
    """
    AI Agent responses ke liye JSON schema return karta hai.
    """
    return {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error", "pending"], "description": "Status of the agent's operation"},
            "message": {"type": "string", "description": "A human-readable message about the operation"},
            "data": {"type": "object", "nullable": True, "description": "Any data returned by the agent (e.g., video links, analytics)"}
        },
        "required": ["status", "message"]
    }

# Future mein yahan par har AI agent ke liye input/output schemas add kiye jayenge.