import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Hypothetical Hindsight API endpoint
HINDSIGHT_BASE_URL = "https://api.hindsight.com/v1"

def store_incident(log: str, analysis: str) -> bool:
    """Store the log and its analysis in Hindsight vector memory."""
    api_key = os.getenv("HINDSIGHT_API_KEY")
    if not api_key:
        return False
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": f"Log: {log}\nAnalysis: {analysis}",
        "metadata": {"type": "incident"}
    }
    
    try:
        response = requests.post(f"{HINDSIGHT_BASE_URL}/memory", headers=headers, json=data, timeout=5)
        response.raise_for_status()
        return True
    except Exception:
        # Fails gracefully without crashing the app
        return False

def retrieve_similar_incidents(log: str, top_k: int = 2) -> str:
    """Retrieve similar incidents from Hindsight memory to provide context."""
    api_key = os.getenv("HINDSIGHT_API_KEY")
    if not api_key:
        return ""
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": log,
        "top_k": top_k
    }
    
    try:
        response = requests.post(f"{HINDSIGHT_BASE_URL}/search", headers=headers, json=data, timeout=5)
        response.raise_for_status()
        results = response.json().get("results", [])
        
        if not results:
            return ""
            
        context = "\n".join([item.get("text", "") for item in results])
        return context
    except Exception:
        # Fails gracefully if Hindsight is unreachable
        return ""
