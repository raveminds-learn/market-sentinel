# Event Understanding Module for Market Sentinel

import requests

def analyze_event(headline):
    """
    Analyzes a market news headline using Ollama (Mistral model) to extract event details.

    Args:
        headline (str): The market news headline to analyze.

    Returns:
        dict: Dictionary with keys: event_type, sentiment, ticker, sector, summary.
    """
    prompt = f"""
Given the following market news headline, extract:
- event_type (e.g., 'Rate Decision', 'Earnings Report', 'M&A', etc.)
- sentiment (Positive, Negative, Neutral)
- ticker (if mentioned, else null or empty string)
- sector (if mentioned, else null or empty string)
- summary (a 1-2 sentence summary of the event in plain English)

Respond in valid JSON using keys: event_type, sentiment, ticker, sector, summary.

Headline:
\"\"\"{headline}\"\"\"
"""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        model_response = response.json()

        # Ollama returns {'response': <string>} for non-streaming mode
        import json
        content = model_response.get("response", "")
        # Try to find JSON object in response
        try:
            # Sometimes the model's response might have text before JSON
            start = content.find('{')
            end = content.rfind('}') + 1
            json_content = content[start:end]
            result = json.loads(json_content)
        except Exception:
            # fallback: return as much as we can
            result = {
                "event_type": None,
                "sentiment": None,
                "ticker": None,
                "sector": None,
                "summary": content.strip()
            }
        return result
    except Exception as e:
        return {
            "event_type": None,
            "sentiment": None,
            "ticker": None,
            "sector": None,
            "summary": f"Error analyzing event: {e}"
        }