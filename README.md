# 🚀 Market Sentinel

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

**AI-powered market risk assessment** - analyzes news events and generates real-time risk scores with explainable reasoning.

**Repository**: [raveminds-learn/market-sentinel](https://github.com/raveminds-learn/market-sentinel)

## 🎯 Features

- **🤖 AI Event Analysis** - Mistral LLM for sentiment & context understanding
- **🔍 Vector Search** - LanceDB similarity matching with historical events
- **📊 Risk Scoring** - 0-100 scale with multi-factor analysis
- **📈 Price Analytics** - DuckDB-powered market reaction metrics
- **🎛️ Web Dashboard** - Streamlit interface with interactive charts


## 🏗️ Architecture

**Modular AI Pipeline:**
```
Input → AI Analysis → Vector Search → Risk Scoring → Dashboard
```

**Core Modules:**
- `ingestion/` - Data loading & preprocessing
- `understanding/` - AI event analysis (Mistral)
- `rag/` - Vector embeddings & similarity search
- `analytics/` - Price metrics & market reactions
- `scoring/` - Multi-factor risk assessment
- `ui/` - Interactive web dashboard

## 🛠️ Tech Stack

**AI/ML:** Mistral LLM, Sentence Transformers, Scikit-learn
**Data:** LanceDB (vectors), DuckDB (analytics), Pandas, NumPy
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

### 🐍 Manual Installation

**Prerequisites:** Python 3.8+, Ollama, Git

1. **Clone & Setup:**
```bash
git clone https://github.com/raveminds-learn/market-sentinel.git
cd market-sentinel
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Setup Ollama:**
```bash
ollama pull mistral  # Pull AI model
ollama serve         # Start server
```

3. **Launch Dashboard:**
```bash
python -m streamlit run ui/dashboard.py
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

print(f"Risk: {result['risk_score']}/100 ({result['risk_level']})")
```

## 📁 Structure

```
market-sentinel/
├── analytics/     # Price analysis & event reactions
├── rag/          # Vector search & embeddings
├── scoring/      # Risk assessment engine
├── ui/           # Streamlit dashboard
├── understanding/# AI event analysis
├── data/         # Sample datasets
└── tests/        # Comprehensive testing
```

## 🤝 Contributing

**Areas:** AI models, data sources, analytics, UI/UX, API development

**Setup:** `pip install -r requirements.txt && python -m pytest`

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

For educational/research use only. Not financial advice. Consult professionals before investment decisions.

---

**Built for the financial technology community** 🚀
