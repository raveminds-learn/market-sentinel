"""
Test script for risk scoring functionality.
"""

import sys
import os

# Add parent directory to path to allow importing from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scoring.risk_engine import score_event_risk

def test_score_event_risk():
    """
    Test the score_event_risk function with a sample event.
    """
    print("Testing score_event_risk function...")
    print("=" * 50)

    # Sample event data
    test_event = {
        'title': 'Apple announces major product recall',
        'ticker': 'AAPL',
        'date': '2024-01-17',
        'description': 'Apple recalls millions of devices due to safety concerns'
    }

    try:
        print(f"Analyzing risk for event: {test_event['title']}")
        print(f"Ticker: {test_event['ticker']}, Date: {test_event['date']}")
        print("-" * 50)

        result = score_event_risk(test_event)

        if result.get('status') == 'success':
            print("Risk Assessment Results:")
            print(f"Risk Score: {result.get('risk_score', 0)}/100")
            print(f"Risk Level: {result.get('risk_level', 'UNKNOWN')}")
            print(f"Reasoning: {result.get('reasoning', 'N/A')}")

            recommendations = result.get('recommendations', [])
            print(f"\nRecommendations ({len(recommendations)}):")
            for rec in recommendations:
                print(f"  • {rec}")

            raw_metrics = result.get('raw_metrics', {})
            similar_count = raw_metrics.get('similar_events_count', 0)
            print(f"\nRaw Metrics:")
            print(f"  Similar Events Found: {similar_count}")

            market_reaction = raw_metrics.get('market_reaction', {})
            if market_reaction and 'error' not in market_reaction:
                print(f"  Event Price: ${market_reaction.get('event_price', 0):.2f}")

                returns = market_reaction.get('returns', {})
                for period, data in returns.items():
                    if data.get('return') is not None:
                        ret_pct = data['return'] * 100
                        print(f"  {period.replace('_', '-')} return: {ret_pct:.2f}%")

            sentiment_analysis = raw_metrics.get('sentiment_impact_analysis', {})
            if sentiment_analysis:
                keywords = sentiment_analysis.get('sentiment_keywords_found', [])
                if keywords:
                    print(f"  Sentiment Keywords: {', '.join(keywords[:3])}")  # Show first 3

                # Check for AI analysis
                ai_analysis = raw_metrics.get('ai_event_analysis', {})
                if ai_analysis:
                    print(f"  AI Event Analysis: {ai_analysis.get('sentiment', 'No sentiment')} sentiment")
                    print(f"  AI Summary: {ai_analysis.get('summary', 'No summary')[:100]}...")
                else:
                    print("  AI Event Analysis: Not available (Ollama not running)")

            print("\nSUCCESS: Risk scoring completed successfully!")
            return True

        else:
            print(f"ERROR: Risk scoring failed: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"ERROR: Failed to test risk scoring: {e}")
        return False

def test_score_event_risk_missing_data():
    """
    Test risk scoring with incomplete event data.
    """
    print("\nTesting risk scoring with incomplete data...")
    print("=" * 55)

    # Event with missing ticker and date
    incomplete_event = {
        'title': 'Tesla faces SEC investigation',
        'description': 'Regulatory concerns'
    }

    try:
        result = score_event_risk(incomplete_event)

        if result.get('status') == 'success':
            print("Results for incomplete event:")
            print(f"Risk Score: {result.get('risk_score', 0)}/100")
            print(f"Risk Level: {result.get('risk_level', 'UNKNOWN')}")
            print(f"Reasoning: {result.get('reasoning', 'N/A')}")

            recommendations = result.get('recommendations', [])
            print(f"\nRecommendations ({len(recommendations)}):")
            for rec in recommendations[:3]:  # Show first 3
                print(f"  • {rec}")

            print("\nSUCCESS: Handled incomplete data correctly!")
            return True
        else:
            print(f"ERROR: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"ERROR: Failed to handle incomplete data: {e}")
        return False

def main():
    """Run all risk scoring tests"""
    print("Running Risk Scoring Module tests...\n")

    # Test with complete event data
    success1 = test_score_event_risk()

    # Test with incomplete event data
    success2 = test_score_event_risk_missing_data()

    print("\n" + "=" * 50)
    print("Risk Scoring Test Summary:")
    print(f"Complete event analysis: {'PASS' if success1 else 'FAIL'}")
    print(f"Incomplete data handling: {'PASS' if success2 else 'FAIL'}")

    if success1 and success2:
        print("SUCCESS: All risk scoring tests passed!")
    else:
        print("FAILURE: Some tests failed!")

if __name__ == "__main__":
    main()