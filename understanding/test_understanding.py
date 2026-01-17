"""
Test script for event understanding functionality using actual Ollama.
"""

import sys
import os

# Add parent directory to path to allow importing from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from understanding.event_understanding import analyze_event

def test_analyze_event():
    """
    Test the analyze_event function with a sample headline using actual Ollama.
    """
    # Sample headline for testing
    headline = "Tesla faces SEC investigation over accounting practices"

    print("Testing analyze_event function with Ollama...")
    print("=" * 50)
    print(f"Headline: {headline}")
    print("-" * 50)

    # First, test basic Ollama connectivity and check for models
    print("\nTesting Ollama connectivity...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Ollama API is accessible")
            models_data = response.json()
            available_models = models_data.get('models', [])
            if available_models:
                print(f"Available models: {[model['name'] for model in available_models]}")
                if not any('mistral' in model['name'].lower() for model in available_models):
                    print("WARNING: Mistral model not found!")
                    print("Please pull the Mistral model with: ollama pull mistral")
                    return
            else:
                print("WARNING: No models available!")
                print("Please pull the Mistral model with: ollama pull mistral")
                return
        else:
            print(f"WARNING: Ollama API returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Cannot connect to Ollama: {e}")
        print("Make sure Ollama is running with: ollama serve")
        return

    try:
        # Call the actual analyze_event function
        print("\nCalling analyze_event function...")
        result = analyze_event(headline)

        print("Analysis Result:")
        print(f"Event Type: {result.get('event_type', 'N/A')}")
        print(f"Sentiment: {result.get('sentiment', 'N/A')}")
        print(f"Ticker: {result.get('ticker', 'N/A')}")
        print(f"Sector: {result.get('sector', 'N/A')}")
        print(f"Summary: {result.get('summary', 'N/A')}")

        # Check if we got meaningful results
        if result.get('event_type') or result.get('sentiment'):
            print("\nSUCCESS: Analysis completed successfully!")
        else:
            print("\nWARNING: Analysis returned empty results - check Mistral model")

    except Exception as e:
        print(f"Error during analysis: {e}")
        print("\nTroubleshooting tips:")
        print("- Make sure Mistral model is pulled: ollama pull mistral")
        print("- Try restarting Ollama: ollama serve")
        print("- Check Ollama logs for errors")

if __name__ == "__main__":
    test_analyze_event()