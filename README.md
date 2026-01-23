# 🚀 Market Sentinel

**AI-powered market risk assessment** - integrates Mistral LLM for real-time event analysis with historical pattern matching to generate quantitative risk scores (0-100) with explainable AI reasoning.

**Repository**: [raveminds-learn/market-sentinel](https://github.com/raveminds-learn/market-sentinel)

## 🎯 Features

- **🤖 Integrated AI Analysis** - Mistral LLM provides real-time event understanding (sentiment, type, summary) + historical pattern matching
- **🔍 Semantic Search** - Sentence Transformers + LanceDB for finding similar historical market events
- **📊 Multi-factor Risk Scoring** - 0-100 scale combining AI insights, market data, and historical patterns
- **📈 Real-time Analytics** - DuckDB-powered price reaction metrics and volatility analysis
- **🎛️ Interactive Dashboard** - Streamlit interface with AI analysis visualization and risk gauges


## 🏗️ Architecture

**Modular AI Pipeline:**
```
Input → Mistral AI Analysis → Vector Search → Risk Scoring → Dashboard
```

**Core Modules:**
- `ingestion/` - Data loading & preprocessing
- `understanding/` - Real-time AI event analysis (Mistral LLM)
- `rag/` - Vector embeddings & similarity search
- `analytics/` - Price metrics & market reactions
- `scoring/` - Multi-factor risk assessment with AI integration
- `ui/` - Interactive web dashboard

## 🛠️ Tech Stack

**AI/ML:** Mistral LLM (via Ollama), Sentence Transformers, PyTorch, Scikit-learn
**Data:** LanceDB (vector database), DuckDB (analytical queries), Pandas, NumPy
**Web:** Streamlit, Plotly, FastAPI
**DevOps:** Docker, pytest, Black

## 🚀 Quick Start

### 🐳 Docker (Recommended - One Command)
```bash
git clone https://github.com/raveminds-learn/market-sentinel.git
cd market-sentinel
docker-compose up
```
Navigate to `http://localhost:8501`

#### 🚀 Single-Command Launchers
```bash
# Using batch script (Windows)
run_market_sentinel.bat

# Using PowerShell script (Windows)
.\run_market_sentinel.ps1
```

### 🐍 Manual Installation

**Prerequisites:** Python 3.8+, Ollama (for full AI features), Git

1. **Clone & Setup:**
```bash
git clone https://github.com/raveminds-learn/market-sentinel.git
cd market-sentinel
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Setup Ollama (Recommended for AI features):**
```bash
ollama pull mistral  # Pull Mistral AI model
ollama serve         # Start Ollama server (keep running)
```
*Note: System works without Ollama but with reduced AI analysis capabilities*

3. **Launch Dashboard:**
```bash
python -m streamlit run ui/dashboard.py
# Or use the quick launcher:
python ui/run_dashboard.py
```

#### 🧪 Testing
```bash
python -m pytest                    # Run all tests
python analytics/test_analytics.py  # Test analytics
python scoring/test_risk_engine.py   # Test risk engine
```

#### 📊 API Usage
```python
from scoring.risk_engine import score_event_risk

result = score_event_risk({
    'title': 'Apple announces major product recall',
    'ticker': 'AAPL',
    'date': '2024-01-17'
})

print(f"Risk Score: {result['risk_score']}/100 ({result['risk_level']})")
print(f"AI Analysis: {result['raw_metrics']['ai_event_analysis'].get('sentiment', 'N/A')} sentiment")
print(f"Recommendations: {len(result['recommendations'])} insights provided")
```

## 📁 Structure

```
market-sentinel/
├── analytics/         # Price analysis & market reaction metrics
├── rag/              # Vector search & embeddings (LanceDB)
├── scoring/          # Multi-factor risk assessment engine
├── ui/               # Streamlit web dashboard
├── understanding/    # Mistral LLM event analysis & understanding
├── data/             # Sample news & price datasets
├── outputs/          # Generated diagrams & screenshots
└── utils/            # Helper utilities
```

## 🤝 Contributing

**Areas:** AI models, data sources, analytics, UI/UX, API development

**Setup:** `pip install -r requirements.txt && python -m pytest`

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

For educational/research use only. Not financial advice. Consult professionals before investment decisions.

---

## 🔬 AI Integration Benefits

**Dual Analysis Approach:**
- **Real-time AI Analysis**: Mistral LLM provides immediate event understanding and sentiment analysis
- **Historical Pattern Matching**: Vector search finds similar past events for context
- **Hybrid Intelligence**: Combines AI reasoning with quantitative market data for robust risk assessment

**Key Advantages:**
- Handles novel events not seen in training data
- Provides explainable AI reasoning alongside numerical scores
- Graceful degradation when AI services are unavailable
- Real-time insights complement historical analysis

**Built for the financial technology community** 🚀
