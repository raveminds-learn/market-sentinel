# 🚀 Market Sentinel

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web--App-red.svg)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-raveminds--learn/market--sentinel-blue)](https://github.com/raveminds-learn/market-sentinel)

**Market Sentinel** is an open-source, AI-powered engine that analyzes market-moving news events and generates real-time risk scores with clear, explainable reasoning. Built for investors, analysts, and financial institutions who need to understand market sentiment and risk exposure from news events.

**Repository**: [raveminds-learn/market-sentinel](https://github.com/raveminds-learn/market-sentinel)

## 🎯 What It Does

Market Sentinel transforms raw news headlines into actionable investment intelligence by:

- **🧠 AI Analysis**: Uses advanced language models (Mistral) to understand event context and sentiment
- **🔍 Similarity Search**: Finds historical events similar to current news using vector embeddings
- **📊 Price Impact Analysis**: Measures market reaction through price movements and volatility
- **⚡ Real-time Risk Scoring**: Generates 0-100 risk scores with detailed reasoning
- **📈 Interactive Dashboard**: Web-based interface for instant risk assessment

## ✨ Key Features

### 🤖 AI-Powered Event Analysis
- Sentiment analysis using state-of-the-art language models
- Event type classification (Regulatory, Earnings, M&A, etc.)
- Impact assessment and entity extraction

### 🔍 Vector Similarity Search (RAG)
- Semantic search through historical news events
- Context-aware event matching
- Efficient vector database operations

### 📊 Financial Analytics
- Price reaction analysis (1, 3, 5-day returns)
- Volatility calculations (20-day annualized)
- Market impact assessment

### 🎛️ Interactive Dashboard
- Web-based interface built with Streamlit
- Real-time risk visualization with charts
- Historical event comparison
- Actionable recommendations

### 🏗️ Modular Architecture
- Clean separation of concerns
- Extensible component design
- RESTful API endpoints
- Comprehensive testing suite

## 🏛️ Architecture

```
market-sentinel/
├── 📁 ingestion/          # Data ingestion & preprocessing
├── 📁 understanding/      # AI-powered event analysis
├── 📁 rag/               # Vector search & context retrieval
├── 📁 analytics/         # Financial metrics & analytics
├── 📁 scoring/           # Risk assessment engine
├── 📁 api/               # REST API endpoints
├── 📁 ui/                # Streamlit dashboard
├── 📁 data/              # Sample datasets
└── 📁 utils/             # Shared utilities
```

### Data Flow
1. **Input**: News headlines and market data
2. **Processing**: AI analysis + vector embedding + price metrics
3. **Analysis**: Multi-factor risk scoring with historical context
4. **Output**: Risk scores, recommendations, and visualizations

## 🛠️ Tools & Technologies

### 🤖 AI & Machine Learning
- **Mistral 7B**: Advanced language model for event analysis via Ollama
- **Sentence Transformers**: Text embedding generation (`all-MiniLM-L6-v2`)
- **Scikit-learn**: Machine learning utilities

### 🗄️ Data & Storage
- **LanceDB**: High-performance vector database for similarity search
- **DuckDB**: In-memory analytical database for fast CSV processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### 🌐 Web & API
- **Streamlit**: Interactive web dashboard
- **FastAPI**: REST API framework (future expansion)
- **Plotly**: Interactive data visualizations
- **Requests**: HTTP client for API integrations

### 🧪 Testing & Development
- **pytest**: Comprehensive testing framework
- **Jupyter**: Interactive development notebooks
- **Black**: Code formatting
- **mypy**: Type checking

### 📊 Data Visualization
- **Matplotlib**: Static plotting
- **Seaborn**: Statistical visualization
- **Plotly**: Interactive charts and dashboards

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama (for Mistral model)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/raveminds-learn/market-sentinel.git
cd market-sentinel
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
# OR install individually:
pip install streamlit plotly matplotlib sentence-transformers lancedb pandas duckdb
```

4. **Install Ollama and pull Mistral model:**
```bash
# Install Ollama from https://ollama.ai/
ollama pull mistral
ollama serve  # Start Ollama server
```

### Usage

#### 🖥️ Launch Dashboard
```bash
# From project root
python -m streamlit run ui/dashboard.py

# OR use the launcher
python ui/run_dashboard.py
```

Navigate to `http://localhost:8501` in your browser.

#### 🧪 Run Tests
```bash
# Run all tests
python -m pytest

# Run specific module tests
python analytics/test_analytics.py
python scoring/test_risk_engine.py
```

#### 🏗️ Build Event Index
```python
from rag.context_retrieval import build_event_index

# Build vector index from news data
result = build_event_index("data/news_sample.csv", "market_events")
print(f"Indexed {result['document_count']} events")
```

## 📖 Usage Examples

### Basic Risk Assessment
```python
from scoring.risk_engine import score_event_risk

event = {
    'title': 'Apple announces major product recall',
    'ticker': 'AAPL',
    'date': '2024-01-17'
}

result = score_event_risk(event)
print(f"Risk Score: {result['risk_score']}/100 ({result['risk_level']})")
print(f"Reasoning: {result['reasoning']}")
```

### Price Analytics
```python
from analytics.historical_analytics import load_price_data, compute_event_reaction

# Load price data
df = load_price_data("data/price_data.csv")

# Analyze event reaction
reaction = compute_event_reaction(df, "AAPL", "2024-01-17")
print(f"1-day return: {reaction['1_day_return']:.2%}")
```

### Vector Search
```python
from rag.context_retrieval import retrieve_similar_events

# Find similar events
results = retrieve_similar_events("Tesla faces SEC investigation")
for event in results['similar_events']:
    print(f"{event['title']} (sentiment: {event['sentiment_score']})")
```

## 📁 Project Structure

```
market-sentinel/
├── 📂 analytics/           # Financial analytics & price metrics
│   ├── historical_analytics.py
│   └── test_analytics.py
├── 📂 api/                  # REST API endpoints
├── 📂 data/                 # Sample datasets
│   ├── news_sample.csv
│   └── price_data.csv
├── 📂 ingestion/            # Data ingestion utilities
│   ├── event_ingestion.py
│   └── test_ingestion.py
├── 📂 rag/                  # Retrieval-Augmented Generation
│   ├── context_retrieval.py
│   └── test_rag.py
├── 📂 scoring/              # Risk assessment engine
│   ├── risk_engine.py
│   └── test_risk_engine.py
├── 📂 ui/                   # Streamlit dashboard
│   ├── dashboard.py
│   ├── run_dashboard.py
│   └── README.md
├── 📂 understanding/        # AI event analysis
│   ├── event_understanding.py
│   └── test_understanding.py
├── 📂 utils/                # Shared utilities
├── 📄 .gitignore            # Git ignore rules
├── 📄 README.md             # This file
└── 📄 requirements.txt      # Python dependencies
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup
git clone https://github.com/raveminds-learn/market-sentinel.git
cd market-sentinel
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Format code
black .
mypy .
```

### Areas for Contribution
- **Model Improvements**: Better embedding models, fine-tuned LLMs
- **Data Sources**: Additional news feeds, alternative data
- **Analytics**: More sophisticated financial metrics
- **UI/UX**: Enhanced dashboard features
- **API**: RESTful endpoints for integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Market Sentinel is for educational and research purposes. Not intended as financial advice. Always consult with qualified financial advisors before making investment decisions. Past performance does not guarantee future results.

## 🙏 Acknowledgments

- **Mistral AI** for the language model
- **LanceDB** for vector database technology
- **Ollama** for local LLM deployment
- **Streamlit** for the web framework
- **Sentence Transformers** for embedding generation

---

**Built with ❤️ for the financial technology community**
