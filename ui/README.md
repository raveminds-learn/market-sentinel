# Market Sentinel Dashboard

A Streamlit-based web interface for analyzing market event risks using AI and analytics.

## Features

- 🎯 **Event Risk Analysis**: Input event details and get comprehensive risk assessment
- 📊 **Risk Score Visualization**: Interactive gauge chart showing risk level (0-100 scale)
- 🔍 **Similar Events Detection**: Find historical events similar to current news
- 📈 **Price Reaction Charts**: Visualize market impact with interactive charts
- 💡 **AI-Powered Recommendations**: Get actionable insights based on risk analysis
- 🔧 **Raw Data Access**: View detailed analytics and metrics

## How to Run

### Prerequisites
Make sure you have all required dependencies installed:
```bash
pip install streamlit plotly matplotlib sentence-transformers lancedb pandas duckdb
```

### Start the Dashboard
```bash
cd market-sentinel
python -m streamlit run ui/dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Output Examples

See the `outputs/` folder for interface screenshots:
- `starting-the-app.png` - Application startup screen
- `ui-landing-page.png` - Main dashboard interface
- `ui-results-page.png` - Risk analysis results view

## Usage

1. **Enter Event Details**:
   - **Event Title**: News headline or event description
   - **Stock Ticker**: Company symbol (e.g., AAPL, TSLA)
   - **Event Date**: When the event occurred

2. **Click "Analyze Risk"** to get comprehensive analysis including:
   - Overall risk score (0-100) with risk level (Low/Medium/High)
   - Detailed reasoning explaining the score
   - Similar historical events found
   - Price reaction metrics and charts
   - Actionable recommendations

## Dashboard Sections

### 🎯 Risk Assessment
- Interactive risk gauge showing score and level
- Key metrics and reasoning

### 📈 Market Analytics
- Price returns visualization
- Volatility metrics
- Key performance indicators

### 🔍 Similar Events
- Historical events similar to current news
- Sentiment and impact analysis
- Source attribution

### 💡 Recommendations
- Risk-appropriate action items
- Monitoring guidance
- Strategic insights

## Technical Details

- **Frontend**: Streamlit for interactive web interface
- **Charts**: Plotly for interactive visualizations
- **AI/ML**: Sentence Transformers for embeddings, Mistral for analysis
- **Vector DB**: LanceDB for efficient similarity search
- **Analytics**: DuckDB for fast CSV processing
- **Risk Engine**: Multi-factor scoring algorithm (0-100 scale)

## Troubleshooting

### Common Issues:

1. **Streamlit not found**: Install with `pip install streamlit`
2. **Missing dependencies**: Install all requirements listed above
3. **LanceDB errors**: Make sure event index is built (see main README)
4. **Port conflicts**: Streamlit defaults to port 8501

### Performance Tips:
- Keep event titles concise but descriptive
- Use recent dates for better analysis
- Ensure ticker symbols are valid

## Integration

The dashboard integrates with all Market Sentinel modules:
- **Ingestion**: CSV data loading
- **Understanding**: AI-powered event analysis
- **RAG**: Vector similarity search
- **Analytics**: Price reaction metrics
- **Scoring**: Risk assessment engine