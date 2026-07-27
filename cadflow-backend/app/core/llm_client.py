import os
import json
import httpx
from app.core.config import settings

def generate_cad_summary(old_meta: dict, new_meta: dict, filename: str) -> str:
    """
    Uses Groq to summarize the differences between two CAD file states.
    If no API key is provided, it falls back to a mock summary.
    """
    if not settings.groq_api_key or settings.groq_api_key.startswith("mock"):
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

    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }

    try:
        response = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return f"[ERROR] Failed to generate AI summary: {e}"
