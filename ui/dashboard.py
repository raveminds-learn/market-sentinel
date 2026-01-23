"""
Market Sentinel Risk Assessment Dashboard
A Streamlit application for analyzing market event risks using AI and analytics.
"""

import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Add parent directory to path to allow importing from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scoring.risk_engine import score_event_risk
from analytics.historical_analytics import load_price_data
from rag.context_retrieval import retrieve_similar_events

# Page configuration
st.set_page_config(
    page_title="Market Sentinel - Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def create_risk_gauge(risk_score):
    """Create a gauge chart for risk score visualization"""
    if risk_score >= 70:
        color = "red"
        label = "HIGH RISK"
    elif risk_score >= 40:
        color = "orange"
        label = "MEDIUM RISK"
    else:
        color = "green"
        label = "LOW RISK"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': f"Risk Score ({label})", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': 'lightgreen'},
                {'range': [40, 70], 'color': 'lightyellow'},
                {'range': [70, 100], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))

    fig.update_layout(height=300)
    return fig

def create_returns_chart(market_reaction):
    """Create a chart showing price returns over time"""
    if not market_reaction or 'error' in market_reaction:
        return None

    returns_data = market_reaction.get('returns', {})

    if not returns_data:
        return None

    # Prepare data for plotting
    periods = []
    returns = []

    for period, data in returns_data.items():
        if data.get('return') is not None:
            periods.append(period.replace('_', '-').title())
            returns.append(data['return'] * 100)  # Convert to percentage

    if not periods:
        return None

    fig = go.Figure()

    # Add bars for returns
    colors = ['green' if r >= 0 else 'red' for r in returns]
    fig.add_trace(go.Bar(
        x=periods,
        y=returns,
        marker_color=colors,
        name='Returns (%)'
    ))

    fig.update_layout(
        title="Price Returns by Time Period",
        xaxis_title="Time Period",
        yaxis_title="Return (%)",
        height=300
    )

    return fig

def display_similar_events(similar_events):
    """Display similar events in a formatted table"""
    if not similar_events:
        st.info("No similar events found")
        return

    # Create a dataframe for display
    events_data = []
    for event in similar_events[:5]:  # Show top 5
        events_data.append({
            "Rank": event.get('rank', 'N/A'),
            "Title": event.get('title', 'N/A')[:50] + "..." if len(event.get('title', '')) > 50 else event.get('title', 'N/A'),
            "Similarity": f"{event.get('similarity_score', 0):.3f}",
            "Sentiment": event.get('sentiment_score', 'N/A'),
            "Impact": event.get('impact_score', 'N/A'),
            "Source": event.get('source', 'N/A')
        })

    df = pd.DataFrame(events_data)
    st.dataframe(df, use_container_width=True)

def main():
    """Main Streamlit application"""

    # Header
    st.markdown('<h1 class="main-header">📊 Market Sentinel Risk Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("Analyze market event risks using AI-powered sentiment analysis, similar event detection, and price reaction metrics.")

    # Sidebar for inputs
    st.sidebar.header("🎯 Event Analysis Input")

    # Event input form
    with st.sidebar.form("event_form"):
        st.subheader("Event Details")

        title = st.text_input(
            "Event Title",
            placeholder="e.g., Apple announces major product recall",
            help="Enter the news headline or event description"
        )

        ticker = st.text_input(
            "Stock Ticker",
            placeholder="e.g., AAPL",
            help="Enter the stock symbol (e.g., AAPL, TSLA, MSFT)"
        ).upper()

        event_date = st.date_input(
            "Event Date",
            value=datetime.now().date(),
            help="Date when the event occurred"
        )

        submitted = st.form_submit_button("🔍 Analyze Risk", type="primary", use_container_width=True)

    # Main content area
    if submitted and title and ticker:
        with st.spinner("🔄 Analyzing event risk... This may take a few seconds."):

            # Prepare event data
            event_data = {
                'title': title,
                'ticker': ticker,
                'date': event_date.strftime('%Y-%m-%d'),
                'description': f"Analysis of {title} for {ticker}"
            }

            # Call risk scoring function
            result = score_event_risk(event_data)

            if result.get('status') == 'success':

                # Risk Score Display
                st.header("🎯 Risk Assessment Results")

                # AI Event Analysis Section
                if 'ai_event_analysis' in result.get('raw_metrics', {}) and result['raw_metrics']['ai_event_analysis']:
                    st.subheader("🤖 AI Event Analysis (Mistral)")

                    ai_data = result['raw_metrics']['ai_event_analysis']

                    # AI Analysis Cards
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        event_type = ai_data.get('event_type', 'Unknown')
                        st.metric("Event Type", event_type if event_type else "Unknown")

                    with col2:
                        sentiment = ai_data.get('sentiment', 'Neutral')
                        sentiment_icon = "🔴" if sentiment.lower() == 'negative' else "🟢" if sentiment.lower() == 'positive' else "🟡"
                        st.metric("Sentiment", f"{sentiment_icon} {sentiment}")

                    with col3:
                        ticker = ai_data.get('ticker', 'None')
                        st.metric("Detected Ticker", ticker if ticker else "None")

                    with col4:
                        sector = ai_data.get('sector', 'Unknown')
                        st.metric("Sector", sector if sector else "Unknown")

                    # AI Summary
                    if ai_data.get('summary'):
                        st.info(f"📝 **AI Summary:** {ai_data['summary']}")

                    st.markdown("---")

                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    risk_score = result.get('risk_score', 0)
                    st.plotly_chart(create_risk_gauge(risk_score), use_container_width=True)

                with col2:
                    st.metric(
                        label="Risk Level",
                        value=result.get('risk_level', 'UNKNOWN'),
                        delta=f"{risk_score}/100"
                    )

                with col3:
                    reasoning = result.get('reasoning', 'N/A')
                    st.metric(
                        label="Assessment",
                        value="Complete",
                        delta="AI Analysis"
                    )

                # Reasoning section
                with st.expander("📋 Detailed Reasoning", expanded=True):
                    st.write(reasoning)

                # Recommendations
                st.header("💡 Recommendations")
                recommendations = result.get('recommendations', [])

                if recommendations:
                    for rec in recommendations:
                        st.success(f"✅ {rec}")
                else:
                    st.info("No specific recommendations available")

                # Charts and Analytics Section
                st.header("📈 Market Analytics")

                col1, col2 = st.columns(2)

                with col1:
                    # Price Returns Chart
                    market_reaction = result.get('raw_metrics', {}).get('market_reaction', {})
                    returns_chart = create_returns_chart(market_reaction)

                    if returns_chart:
                        st.subheader("📊 Price Returns Analysis")
                        st.plotly_chart(returns_chart, use_container_width=True)
                    else:
                        st.info("Price data not available for chart")

                with col2:
                    # Risk Factors
                    raw_metrics = result.get('raw_metrics', {})
                    similar_count = raw_metrics.get('similar_events_count', 0)
                    sentiment_keywords = raw_metrics.get('sentiment_impact_analysis', {}).get('sentiment_keywords_found', [])

                    st.subheader("📋 Key Metrics")

                    metric_col1, metric_col2 = st.columns(2)

                    with metric_col1:
                        st.metric("Similar Events", similar_count)
                        event_price = market_reaction.get('event_price')
                        if event_price:
                            st.metric("Event Price", f"${event_price:.2f}")

                    with metric_col2:
                        vol_data = market_reaction.get('volatility_20_day', {})
                        if 'annualized_volatility' in vol_data:
                            ann_vol = vol_data['annualized_volatility'] * 100
                            st.metric("20-Day Volatility", f"{ann_vol:.1f}%")

                    if sentiment_keywords:
                        st.subheader("🔍 Sentiment Keywords")
                        keywords_text = ", ".join(sentiment_keywords[:5])  # Show first 5
                        st.info(keywords_text)

                # Similar Events Section
                st.header("🔍 Similar Historical Events")
                # Get similar events count from raw metrics
                raw_metrics = result.get('raw_metrics', {})
                similar_count = raw_metrics.get('similar_events_count', 0)

                if similar_count > 0:
                    st.info(f"Found {similar_count} similar historical events in the knowledge base")

                    # Try to get more details from the risk assessment
                    sentiment_analysis = raw_metrics.get('sentiment_impact_analysis', {})

                    # Display summary stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        negative_events = sentiment_analysis.get('negative_similar_events', 0)
                        st.metric("Negative Events", negative_events)

                    with col2:
                        high_impact = sentiment_analysis.get('high_impact_similar_events', 0)
                        st.metric("High Impact Events", high_impact)

                    with col3:
                        neutral_positive = similar_count - negative_events
                        st.metric("Other Events", neutral_positive)

                else:
                    st.info("No similar historical events found in the knowledge base")

                # Raw Data Section (Collapsible)
                with st.expander("🔧 Raw Analysis Data", expanded=False):
                    st.json(result)

            else:
                st.error(f"❌ Risk analysis failed: {result.get('error', 'Unknown error')}")
                st.json(result)

    elif submitted:
        st.warning("⚠️ Please fill in all required fields (Title and Ticker)")

    # Footer
    st.markdown("---")
    st.markdown("*Market Sentinel - AI-Powered Market Risk Assessment*")
    st.markdown("*Built with Streamlit, Mistral LLM, Sentence Transformers, LanceDB, and DuckDB*")

if __name__ == "__main__":
    main()