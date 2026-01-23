# Risk Scoring Engine for Market Sentinel

from typing import Dict, Any
import sys
import os

# Add parent directory to path to allow importing from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.context_retrieval import retrieve_similar_events
from analytics.historical_analytics import load_price_data, compute_event_reaction
from understanding.event_understanding import analyze_event

def score_event_risk(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main risk scoring function that combines RAG and analytics to assess event risk.

    Uses similar events and market reaction metrics to compute a comprehensive risk score.

    Args:
        event (Dict[str, Any]): Event data with keys like 'title', 'ticker', 'date', etc.

    Returns:
        Dict[str, Any]: Risk assessment with score, similar events, and market metrics
    """
    # Initialize result variables
    similar_result = {'status': 'error', 'similar_events': []}
    reaction_result = {'error': 'No market reaction analysis performed'}

    try:
        risk_assessment = {
            'event_title': event.get('title', ''),
            'event_ticker': event.get('ticker', ''),
            'event_date': event.get('date', ''),
            'risk_score': 0.0,
            'risk_factors': [],
            'similar_events': [],
            'market_reaction': {},
            'recommendations': []
        }

        # Step 0: Analyze event with Mistral AI
        ai_analysis = {'status': 'error', 'analysis': {}}
        if 'title' in event and event['title']:
            print(f"Analyzing event with Mistral AI: {event['title']}")
            try:
                ai_analysis = {
                    'status': 'success',
                    'analysis': analyze_event(event['title'])
                }
                print(f"Mistral analysis complete: {ai_analysis['analysis'].get('sentiment', 'Unknown')}")
            except Exception as e:
                ai_analysis = {
                    'status': 'error',
                    'error': str(e),
                    'analysis': {}
                }
                print(f"Warning: Mistral analysis failed: {e}")

        # Step 1: Retrieve similar events using RAG
        if 'title' in event and event['title']:
            print(f"Retrieving similar events for: {event['title']}")
            similar_result = retrieve_similar_events(
                headline=event['title'],
                collection_name="market_events",
                top_k=5
            )

            if similar_result.get('status') == 'success':
                risk_assessment['similar_events'] = similar_result.get('similar_events', [])

                # Analyze similar events for risk patterns
                negative_events = 0
                high_impact_events = 0

                for similar_event in risk_assessment['similar_events']:
                    sentiment = similar_event.get('sentiment_score', 0)
                    impact = similar_event.get('impact_score', 0)

                    if sentiment < -0.3:  # Negative sentiment
                        negative_events += 1
                    if impact > 0.7:  # High impact
                        high_impact_events += 1

                # Risk factor from similar events
                if negative_events > 0:
                    risk_assessment['risk_factors'].append(f"Found {negative_events} similar negative events")
                    risk_assessment['risk_score'] += negative_events * 0.2

                if high_impact_events > 0:
                    risk_assessment['risk_factors'].append(f"Found {high_impact_events} similar high-impact events")
                    risk_assessment['risk_score'] += high_impact_events * 0.15

                print(f"Found {len(risk_assessment['similar_events'])} similar events")
            else:
                risk_assessment['risk_factors'].append("Could not retrieve similar events")
                print(f"Warning: {similar_result.get('error', 'Unknown error retrieving similar events')}")
        else:
            risk_assessment['risk_factors'].append("No event title provided for similarity analysis")

        # Step 2: Compute market reaction metrics
        if 'ticker' in event and 'date' in event and event['ticker'] and event['date']:
            try:
                print(f"Computing market reaction for {event['ticker']} on {event['date']}")

                # Load price data
                price_df = load_price_data("data/price_data.csv")

                # Compute event reaction
                reaction_result = compute_event_reaction(
                    price_df=price_df,
                    ticker=event['ticker'],
                    event_date=event['date']
                )

                if 'error' not in reaction_result:
                    risk_assessment['market_reaction'] = reaction_result

                    # Analyze market reaction for risk
                    returns_to_analyze = []
                    for days in [1, 3, 5]:
                        return_key = f'{days}_day_return'
                        if return_key in reaction_result and reaction_result[return_key] is not None:
                            returns_to_analyze.append(reaction_result[return_key])

                    if returns_to_analyze:
                        avg_return = sum(returns_to_analyze) / len(returns_to_analyze)
                        max_negative_return = min(returns_to_analyze) if returns_to_analyze else 0

                        # Risk scoring based on returns
                        if avg_return < -0.05:  # Average return worse than -5%
                            risk_assessment['risk_factors'].append(f"Severe negative market reaction: {avg_return:.2f}")
                            risk_assessment['risk_score'] += 0.3
                        elif avg_return < -0.02:  # Average return worse than -2%
                            risk_assessment['risk_factors'].append(f"Moderate negative market reaction: {avg_return:.2f}")
                            risk_assessment['risk_score'] += 0.15

                        if max_negative_return < -0.10:  # Any single day drop > 10%
                            risk_assessment['risk_factors'].append(f"Extreme single-day drop: {max_negative_return:.2f}")
                            risk_assessment['risk_score'] += 0.25

                    # Check volatility
                    vol_data = reaction_result.get('volatility_20_day', {})
                    if 'annualized_volatility' in vol_data:
                        ann_vol = vol_data['annualized_volatility']
                        if ann_vol > 0.5:  # Very high volatility
                            risk_assessment['risk_factors'].append(f"Very high market volatility: {ann_vol:.2f}")
                            risk_assessment['risk_score'] += 0.2
                        elif ann_vol > 0.3:  # High volatility
                            risk_assessment['risk_factors'].append(f"High market volatility: {ann_vol:.2f}")
                            risk_assessment['risk_score'] += 0.1

                    print("Market reaction analysis completed")
                else:
                    risk_assessment['risk_factors'].append(f"Market reaction analysis failed: {reaction_result.get('error', 'Unknown error')}")
                    print(f"Warning: {reaction_result.get('error', 'Unknown error in market reaction analysis')}")

            except Exception as e:
                risk_assessment['risk_factors'].append(f"Error computing market reaction: {str(e)}")
                print(f"Error in market reaction analysis: {e}")
        else:
            risk_assessment['risk_factors'].append("Missing ticker or date for market reaction analysis")

        # Step 2.5: Integrate Mistral AI analysis into risk assessment
        if ai_analysis.get('status') == 'success' and ai_analysis.get('analysis'):
            mistral_data = ai_analysis['analysis']
            mistral_sentiment = mistral_data.get('sentiment', '').lower()

            # Enhance risk scoring with AI insights
            if mistral_sentiment == 'negative':
                risk_assessment['risk_score'] += 0.2
                risk_assessment['risk_factors'].append("AI-detected negative sentiment")
            elif mistral_sentiment == 'positive':
                risk_assessment['risk_score'] -= 0.1  # Reduce risk for positive sentiment
                risk_assessment['risk_factors'].append("AI-detected positive sentiment")

            # Extract ticker from AI analysis if not provided by user
            if not risk_assessment.get('event_ticker') and mistral_data.get('ticker'):
                risk_assessment['event_ticker'] = mistral_data['ticker']

            # Add AI insights to recommendations
            if 'recommendations' not in risk_assessment:
                risk_assessment['recommendations'] = []

            if mistral_data.get('summary'):
                risk_assessment['recommendations'].append(f"AI Analysis: {mistral_data['summary']}")

        # Step 3: Generate comprehensive risk score (0-100) and level
        final_risk_score, risk_level, reasoning = compute_comprehensive_risk_score(
            event, risk_assessment, similar_result, reaction_result
        )

        # Step 4: Generate recommendations based on risk level
        recommendations = generate_risk_recommendations(risk_level, final_risk_score)

        # Step 5: Compile final result
        result = {
            'risk_score': final_risk_score,  # 0-100 scale
            'risk_level': risk_level,  # Low, Medium, High
            'reasoning': reasoning,
            'raw_metrics': {
                'event_title': event.get('title', ''),
                'event_ticker': event.get('ticker', ''),
                'event_date': event.get('date', ''),
                'similar_events_count': len(risk_assessment.get('similar_events', [])),
                'market_reaction': risk_assessment.get('market_reaction', {}),
                'sentiment_impact_analysis': extract_sentiment_impact_analysis(event, similar_result),
                'ai_event_analysis': ai_analysis.get('analysis', {}),
                'price_reaction_metrics': extract_price_reaction_metrics(reaction_result)
            },
            'recommendations': recommendations,
            'assessment_timestamp': '2024-01-17T16:23:17Z',  # Would be datetime.now() in real implementation
            'status': 'success'
        }

        print(f"Final risk score: {final_risk_score}/100 ({risk_level})")
        return result

    except Exception as e:
        print(f"Critical error in risk scoring: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'event_title': event.get('title', ''),
            'risk_score': 0.0,
            'risk_level': 'UNKNOWN'
        }

def compute_comprehensive_risk_score(event: Dict[str, Any], risk_assessment: Dict[str, Any],
                                   similar_result: Dict[str, Any], reaction_result: Dict[str, Any]) -> tuple:
    """
    Compute comprehensive risk score (0-100) combining all factors.

    Returns:
        tuple: (risk_score, risk_level, reasoning)
    """
    base_score = 0
    reasoning_parts = []

    # Factor 1: Sentiment Analysis (0-30 points)
    sentiment_score = analyze_sentiment_risk(event, similar_result)
    base_score += sentiment_score
    if sentiment_score > 0:
        reasoning_parts.append(f"Sentiment analysis: {sentiment_score} points")

    # Factor 2: Impact Analysis (0-25 points)
    impact_score = analyze_impact_risk(event, similar_result)
    base_score += impact_score
    if impact_score > 0:
        reasoning_parts.append(f"Impact analysis: {impact_score} points")

    # Factor 3: Similar Events Analysis (0-20 points)
    similar_score = analyze_similar_events_risk(risk_assessment)
    base_score += similar_score
    if similar_score > 0:
        reasoning_parts.append(f"Similar events analysis: {similar_score} points")

    # Factor 4: Price Reaction Analysis (0-25 points)
    price_score = analyze_price_reaction_risk(reaction_result)
    base_score += price_score
    if price_score > 0:
        reasoning_parts.append(f"Price reaction analysis: {price_score} points")

    # Ensure score is within 0-100 range
    final_score = max(0, min(100, base_score))

    # Determine risk level
    if final_score >= 70:
        risk_level = "High"
    elif final_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Compile reasoning
    reasoning = f"Risk score of {final_score}/100 ({risk_level} risk) based on: {'; '.join(reasoning_parts)}"

    return final_score, risk_level, reasoning

def analyze_sentiment_risk(event: Dict[str, Any], similar_result: Dict[str, Any]) -> float:
    """Analyze sentiment-related risk (0-30 points)"""
    score = 0

    # Check event title for negative keywords
    title = event.get('title', '').lower()
    negative_keywords = ['faces', 'investigation', 'probe', 'recall', 'lawsuit', 'crisis', 'scandal',
                        'violation', 'penalty', 'ban', 'shutdown', 'failure', 'breach']
    positive_keywords = ['rally', 'surge', 'strong', 'positive', 'gains', 'success', 'breakthrough']

    negative_count = sum(1 for keyword in negative_keywords if keyword in title)
    positive_count = sum(1 for keyword in positive_keywords if keyword in title)

    if negative_count > 0:
        score += min(15, negative_count * 5)  # Up to 15 points for negative keywords
    if positive_count > 0:
        score -= min(5, positive_count * 2)  # Reduce score for positive keywords

    # Check similar events sentiment
    similar_events = similar_result.get('similar_events', [])
    if similar_events:
        negative_similar = sum(1 for e in similar_events if e.get('sentiment_score', 0) < -0.3)
        if negative_similar > 0:
            score += min(15, negative_similar * 3)  # Up to 15 points for negative similar events

    return max(0, score)

def analyze_impact_risk(event: Dict[str, Any], similar_result: Dict[str, Any]) -> float:
    """Analyze impact-related risk (0-25 points)"""
    score = 0

    # Check for high-impact keywords in title
    title = event.get('title', '').lower()
    high_impact_keywords = ['major', 'massive', 'significant', 'historic', 'unprecedented',
                           'revolutionary', 'breakthrough', 'crisis', 'emergency']

    impact_count = sum(1 for keyword in high_impact_keywords if keyword in title)
    if impact_count > 0:
        score += min(10, impact_count * 3)  # Up to 10 points for impact keywords

    # Check similar events impact
    similar_events = similar_result.get('similar_events', [])
    if similar_events:
        high_impact_similar = sum(1 for e in similar_events if e.get('impact_score', 0) > 0.7)
        if high_impact_similar > 0:
            score += min(15, high_impact_similar * 4)  # Up to 15 points for high-impact similar events

    return max(0, score)

def analyze_similar_events_risk(risk_assessment: Dict[str, Any]) -> float:
    """Analyze risk from similar events pattern (0-20 points)"""
    score = 0

    risk_factors = risk_assessment.get('risk_factors', [])
    similar_events = risk_assessment.get('similar_events', [])

    # Points for each risk factor identified
    score += len(risk_factors) * 2  # Up to 10 points for risk factors

    # Points for number of similar events found
    similar_count = len(similar_events)
    if similar_count > 3:
        score += 10  # 10 points if many similar events
    elif similar_count > 1:
        score += 5   # 5 points if some similar events

    return min(20, score)

def analyze_price_reaction_risk(reaction_result: Dict[str, Any]) -> float:
    """Analyze risk from price reaction metrics (0-25 points)"""
    score = 0

    if 'error' in reaction_result:
        return 0  # No price data available

    # Check return metrics
    returns_to_check = []
    for days in [1, 3, 5]:
        return_key = f'{days}_day_return'
        if return_key in reaction_result and reaction_result[return_key] is not None:
            returns_to_check.append(reaction_result[return_key])

    if returns_to_check:
        # Penalize for negative returns
        avg_return = sum(returns_to_check) / len(returns_to_check)
        if avg_return < -0.05:  # Worse than -5%
            score += 15
        elif avg_return < -0.02:  # Worse than -2%
            score += 8

        # Check for extreme single-day moves
        max_negative = min(returns_to_check) if returns_to_check else 0
        if max_negative < -0.10:  # Any single day drop > 10%
            score += 10

    # Check volatility
    vol_data = reaction_result.get('volatility_20_day', {})
    if 'annualized_volatility' in vol_data:
        ann_vol = vol_data['annualized_volatility']
        if ann_vol > 0.5:  # Very high volatility
            score += 10
        elif ann_vol > 0.3:  # High volatility
            score += 5

    return min(25, score)

def generate_risk_recommendations(risk_level: str, risk_score: float) -> list:
    """Generate risk-appropriate recommendations"""
    if risk_level == "High":
        return [
            "[HIGH RISK] IMMEDIATE ATTENTION REQUIRED",
            "Consider immediate position adjustments or hedging",
            "Monitor news feeds and social media closely",
            "Prepare contingency plans for further developments",
            "Consult with risk management team immediately"
        ]
    elif risk_level == "Medium":
        return [
            "[MEDIUM RISK] INCREASED MONITORING RECOMMENDED",
            "Review and potentially adjust position sizing",
            "Stay informed about related news developments",
            "Consider setting additional stop-loss levels",
            "Monitor competitor reactions and market sentiment"
        ]
    else:  # Low
        return [
            "[LOW RISK] NORMAL MONITORING PROCEDURES",
            "Continue standard market monitoring",
            "Note event for regular portfolio review",
            "No immediate action required",
            "Maintain existing risk management protocols"
        ]

def extract_sentiment_impact_analysis(event: Dict[str, Any], similar_result: Dict[str, Any]) -> dict:
    """Extract sentiment and impact analysis details"""
    return {
        'event_title': event.get('title', ''),
        'sentiment_keywords_found': extract_sentiment_keywords(event.get('title', '')),
        'similar_events_count': len(similar_result.get('similar_events', [])),
        'negative_similar_events': sum(1 for e in similar_result.get('similar_events', [])
                                     if e.get('sentiment_score', 0) < -0.3),
        'high_impact_similar_events': sum(1 for e in similar_result.get('similar_events', [])
                                        if e.get('impact_score', 0) > 0.7)
    }

def extract_price_reaction_metrics(reaction_result: Dict[str, Any]) -> dict:
    """Extract price reaction metrics"""
    if 'error' in reaction_result:
        return {'error': reaction_result['error']}

    metrics = {
        'event_price': reaction_result.get('event_price'),
        'returns': {},
        'volatility': reaction_result.get('volatility_20_day', {})
    }

    # Extract returns
    for days in [1, 3, 5]:
        return_key = f'{days}_day_return'
        price_key = f'{days}_day_price'
        date_key = f'{days}_day_date'

        if return_key in reaction_result:
            metrics['returns'][f'{days}_day'] = {
                'return': reaction_result[return_key],
                'price': reaction_result.get(price_key),
                'date': reaction_result.get(date_key)
            }

    return metrics

def extract_sentiment_keywords(title: str) -> list:
    """Extract sentiment-related keywords from title"""
    title_lower = title.lower()
    keywords = []

    negative_keywords = ['faces', 'investigation', 'probe', 'recall', 'lawsuit', 'crisis', 'scandal',
                        'violation', 'penalty', 'ban', 'shutdown', 'failure', 'breach']
    positive_keywords = ['rally', 'surge', 'strong', 'positive', 'gains', 'success', 'breakthrough']

    for keyword in negative_keywords:
        if keyword in title_lower:
            keywords.append(f"negative: {keyword}")

    for keyword in positive_keywords:
        if keyword in title_lower:
            keywords.append(f"positive: {keyword}")

    return keywords