import json
import os

from anthropic import Anthropic

# For testing, we mock the anthropic client if the key is dummy or not set
MOCK_MODE = os.getenv("ANTHROPIC_API_KEY", "").startswith("mock") or not os.getenv("ANTHROPIC_API_KEY")

if not MOCK_MODE:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_cad_summary(old_meta: dict, new_meta: dict, filename: str) -> str:
    """
    Uses Anthropic Claude to summarize the differences between two CAD file states.
    """
    if MOCK_MODE:
        return f"[MOCK] AI Summary: The file {filename} changed. Entity counts went from {old_meta.get('entity_counts', {})} to {new_meta.get('entity_counts', {})}. Bounding box changed slightly."

    prompt = f"""
    You are an expert CAD engineer. 
    Analyze the following metadata changes for the CAD file {filename}.
    
    Old Metadata:
    {json.dumps(old_meta, indent=2)}
    
    New Metadata:
    {json.dumps(new_meta, indent=2)}
    
    Please provide a concise, professional summary of what changed (e.g., 'Added 5 lines, changed bounding box width by 10%').
    Also state if the changes seem typical or potentially problematic (e.g. layers were deleted).
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text
