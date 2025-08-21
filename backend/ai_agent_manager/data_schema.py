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

# --- Strategist Agent (Team Member 1) Schemas ---
def get_strategist_input_schema():
    """
    Strategist Agent ke liye input schema.
    Input: Manager se mila campaign details.
    """
    return get_campaign_details_schema()

def get_strategist_output_schema():
    """
    Strategist Agent ke output ka schema.
    Output: ek structured JSON object jismein campaign ki saari details hain.
    """
    return {
        "type": "object",
        "properties": {
            "campaign_id": {"type": "string"},
            "campaign_name": {"type": "string"},
            "video_length": {"type": "string"},
            "target_product": {"type": "string"},
            "target_audience": {"type": "string", "nullable": True},
            "social_media_platforms": {
                "type": "array",
                "items": {"type": "string"}
            },
            "action_plan": {
                "type": "object",
                "properties": {
                    "research_keywords": {"type": "array", "items": {"type": "string"}},
                    "download_count": {"type": "integer"},
                    "clip_length": {"type": "string"}
                },
                "required": ["research_keywords", "download_count", "clip_length"]
            }
        },
        "required": ["campaign_id", "campaign_name", "video_length", "target_product", "social_media_platforms", "action_plan"]
    }

# --- Researcher Agent (Team Member 2) Schemas ---
def get_researcher_input_schema():
    """
    Researcher Agent ke liye input schema.
    Input: Strategist se mila action plan.
    """
    return {
        "type": "object",
        "properties": {
            "research_keywords": {"type": "array", "items": {"type": "string"}},
            "download_count": {"type": "integer"}
        },
        "required": ["research_keywords", "download_count"]
    }

def get_researcher_output_schema():
    """
    Researcher Agent ke output ka schema.
    Output: Downloaded videos ke paths aur metadata ki list.
    """
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "video_path": {"type": "string", "description": "Path to the downloaded video file"},
                "metadata": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "tags": {"type": "array", "items": {"type": "string"}},
                        "source_url": {"type": "string"},
                        "virality_score": {"type": "number"}
                    },
                    "required": ["title", "description", "source_url"]
                }
            },
            "required": ["video_path", "metadata"]
        }
    }

# --- Storyteller Agent (Team Member 3) Schemas ---
def get_storyteller_input_schema():
    """
    Storyteller Agent ke liye input schema.
    Input: Researcher se mile video files ke paths.
    """
    return get_researcher_output_schema()

def get_storyteller_output_schema():
    """
    Storyteller Agent ke output ka schema.
    Output: Trimmed clips, summary aur music recommendations.
    """
    return {
        "type": "object",
        "properties": {
            "clipped_videos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "clip_path": {"type": "string"},
                        "clip_summary": {"type": "string"},
                        "recommended_music": {"type": "string"}
                    },
                    "required": ["clip_path", "clip_summary", "recommended_music"]
                }
            }
        },
        "required": ["clipped_videos"]
    }

# --- Editor Agent (Team Member 4) Schemas ---
def get_editor_input_schema():
    """
    Editor Agent ke liye input schema.
    Input: Storyteller se mile clipped videos aur summary.
    """
    return get_storyteller_output_schema()

def get_editor_output_schema():
    """
    Editor Agent ke output ka schema.
    Output: Final edited video clips ke paths.
    """
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "final_video_path": {"type": "string"},
                "original_video_summary": {"type": "string"}
            },
            "required": ["final_video_path", "original_video_summary"]
        }
    }

# --- Marketer Agent (Team Member 5) Schemas ---
def get_marketer_input_schema():
    """
    Marketer Agent ke liye input schema.
    Input: Editor se mile final video clips ke paths aur summary.
    """
    return get_editor_output_schema()

def get_marketer_output_schema():
    """
    Marketer Agent ke output ka schema.
    Output: Published video links aur analytics.
    """
    return {
        "type": "object",
        "properties": {
            "published_videos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string", "enum": ["youtube", "instagram"]},
                        "link": {"type": "string"},
                        "status": {"type": "string", "enum": ["published", "failed"]},
                        "initial_performance": {"type": "object"}
                    },
                    "required": ["platform", "link", "status"]
                }
            }
        },
        "required": ["published_videos"]
    }