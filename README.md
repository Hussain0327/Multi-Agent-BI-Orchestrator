# Business Intelligence Orchestrator

A self-hosted multi-agent business intelligence system with automated document generation, research augmentation, and intelligent query routing. Generates professional PowerPoint presentations and Excel workbooks from natural language business questions.

## Overview

This system coordinates multiple specialized AI agents to provide comprehensive business analysis backed by academic research. It automatically generates three deliverables from a single query:

1. **Structured JSON** - Machine-readable data for API integrations
2. **PowerPoint Presentation** - Professional executive summary decks
3. **Excel Workbook** - Analysis spreadsheets with formulas and scenarios

**Key Features:**
- Research-Augmented Generation (RAG) with academic paper citations
- Parallel agent execution for 2-3x performance improvement
- Hybrid LLM strategy (DeepSeek + GPT-5) for 90% cost savings
- Redis caching layer for 60-138x speedup on repeated queries
- Docker Compose deployment for easy self-hosting

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd multi_agent_workflow

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up

# Access API at http://localhost:8000/docs
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Interactive CLI
python cli.py

# Or start API server
uvicorn src.main:app --reload
```

### Prerequisites

- Python 3.12+ or Docker
- OpenAI API key (GPT-5 access)
- DeepSeek API key (optional, for cost savings)
- LangSmith API key (optional, for tracing)

---

## System Architecture

### Agent Workflow

```
User Query
    ↓
Query Classifier (simple/business/complex)
    ↓
├─ SIMPLE → Direct Answer (5s)
├─ BUSINESS → Agent Router → 4 Parallel Agents → Synthesis
└─ COMPLEX → Research Retrieval → Agent Router → 4 Parallel Agents → Synthesis
```

### Specialized Agents

1. **Market Analysis** - Trends, competition, customer segmentation
2. **Operations Audit** - Process optimization, efficiency analysis
3. **Financial Modeling** - ROI calculations, revenue projections
4. **Lead Generation** - Customer acquisition, growth strategies

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Orchestration | LangGraph state machine |
| LLM | DeepSeek v3.2-Exp + GPT-5-nano |
| Routing | SetFit ML classifier + GPT-5 fallback |
| Execution | Python asyncio (parallel) |
| Caching | Redis + file fallback |
| Vector Store | ChromaDB |
| Research | Semantic Scholar + arXiv APIs |
| Documents | python-pptx + openpyxl |
| API | FastAPI |

---

## Document Automation

### Automatic Generation

From a single business query, the system generates:

**PowerPoint Presentation** (10-12 slides)
- Title slide with branding
- Executive summary
- Context and methodology
- Key findings
- Metrics visualization
- Risk analysis
- Detailed recommendations
- Next steps
- References

**Excel Workbook** (5 sheets)
- Executive Summary: KPI dashboard
- Raw Data: Complete analysis output
- Calculations: Formulas with Base/Upside/Downside scenarios
- Charts & Visuals: Data visualizations
- Assumptions & Sources: Methodology and citations

### Usage Example

```python
from src.agents.financial_modeling import FinancialModelingAgent
from src.generators import PowerPointGenerator, ExcelGenerator

# Generate analysis
agent = FinancialModelingAgent()
output = agent.model_financials_structured(
    "What are the unit economics for my SaaS business?"
)

# Generate PowerPoint
ppt_gen = PowerPointGenerator()
ppt_gen.generate(output, "analysis.pptx")

# Generate Excel
excel_gen = ExcelGenerator()
excel_gen.generate(output, "analysis.xlsx")
```

### Complete Automation Test

```bash
# Generates JSON + PowerPoint + Excel from one query
python test_document_automation.py
```

---

## Features by Phase

### Phase 1: Core System (Complete)

- GPT-5 API integration
- LangGraph orchestration
- 4 specialized agents
- Conversation memory
- FastAPI REST API
- Interactive CLI

### Phase 2: Research & Intelligence (Complete)

**Week 1: RAG Integration**
- ChromaDB vector store
- Semantic Scholar integration
- arXiv integration
- Research synthesis agent
- APA citation formatting

**Week 2: ML Routing**
- SetFit ML classifier (77% accuracy)
- Evaluation framework
- DeepSeek integration (90% cost savings)
- Hybrid routing strategy
- 10-query benchmark analysis

**Week 3: Performance & Production**
- Parallel agent execution (2.1x speedup)
- Query complexity classification
- Redis caching (60-138x speedup)
- Docker Compose deployment
- Fast answer path for simple queries

### Phase 3: Document Automation (Complete)

- Structured JSON schema with Pydantic
- PowerPoint generation (branded decks)
- Excel generation (workbooks with scenarios)
- Chart generation with matplotlib
- Complete automation pipeline

---

## Performance Metrics

### Current Performance

| Metric | Value |
|--------|-------|
| Simple query latency | ~5s |
| Business query latency | 69s (2.1x faster than sequential) |
| Complex query latency | 153s (1.5x faster) |
| Cost per query | $0.0026 (90% savings vs GPT-5) |
| Cache hit speedup | 60-138x |
| Agent execution | Parallel (4 concurrent) |

### Benchmark Results

- Visual analysis: `eval/benchmark_analysis.pdf`
- Raw data: `eval/benchmark_results_10queries.csv`
- 10-query benchmark showing routing accuracy and latency

---

## Directory Structure

```
multi_agent_workflow/
├── src/
│   ├── agents/              # Specialized AI agents
│   ├── tools/               # Agent tools (research, calculator)
│   ├── generators/          # Document generators (PowerPoint, Excel)
│   ├── schemas/             # Pydantic data schemas
│   ├── langgraph_orchestrator.py
│   ├── cache.py             # Redis caching
│   └── main.py              # FastAPI server
│
├── eval/                    # Evaluation framework
│   ├── benchmark.py
│   └── test_queries.json
│
├── models/                  # ML models
│   └── routing_classifier.pkl
│
├── docs/                    # Documentation
│   ├── DOCUMENT_AUTOMATION.md
│   ├── PARALLEL_EXECUTION_COMPLETE.md
│   └── [other docs]
│
├── test_document_automation.py   # Complete automation demo
├── test_structured_output.py     # Phase 1 test
├── test_powerpoint_generation.py # Phase 2 test
├── cli.py                         # Interactive CLI
└── docker-compose.yml             # Docker deployment
```

---

## API Usage

### REST API

```bash
# Start server
uvicorn src.main:app --reload
```

```python
import requests

# Run query
response = requests.post(
    "http://localhost:8000/query",
    json={"query": "How can I reduce churn?"}
)

# Get cache statistics
stats = requests.get("http://localhost:8000/cache/stats")
```

### Python SDK

```python
from src.langgraph_orchestrator import LangGraphOrchestrator

# Initialize with RAG
orch = LangGraphOrchestrator(enable_rag=True)

# Execute query
result = orch.orchestrate(
    query="What are SaaS pricing best practices?",
    use_memory=False
)

print(result['recommendation'])
print(result['agents_consulted'])
```

---

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-5-nano

# Optional (for cost savings)
DEEPSEEK_API_KEY=sk-...
MODEL_STRATEGY=hybrid  # or "gpt5" or "deepseek"

# Optional (for tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...

# Cache configuration
CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

### Model Strategy

- **gpt5**: Use GPT-5 for everything (highest quality)
- **deepseek**: Use DeepSeek for everything (lowest cost)
- **hybrid**: Smart routing (DeepSeek for most, GPT-5 fallback)

---

## Testing

### Run Tests

```bash
# System tests
python test_system.py

# RAG integration (5 tests)
python test_rag_system.py

# Document automation
python test_document_automation.py

# Structured output
python test_structured_output.py
```

### Run Benchmarks

```bash
# Quick test (3 queries)
python eval/benchmark.py --mode both --num-queries 3 --no-judge

# Full evaluation (25 queries)
python eval/benchmark.py --mode both --num-queries 25
```

---

## Deployment

### Docker Compose

```yaml
# docker-compose.yml includes:
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  orchestrator:
    build: .
    ports: ["8000:8000"]
    depends_on: [redis]
    environment:
      - REDIS_URL=redis://redis:6379/0
```

### Production Considerations

- Set up monitoring (Prometheus/Grafana)
- Configure authentication and rate limiting
- Use managed Redis (AWS ElastiCache, etc.)
- Enable HTTPS with reverse proxy
- Set appropriate resource limits

---

## Cost Analysis

### Comparison (100 queries/day)

| Model Strategy | Cost/Query | Monthly Cost | Annual Cost |
|---------------|-----------|--------------|-------------|
| GPT-5 only | $0.30 | $900 | $10,800 |
| Hybrid (recommended) | $0.04 | $120 | $1,440 |
| DeepSeek only | $0.003 | $9 | $108 |

**Savings with Hybrid:** $780/month ($9,360/year)

### Cache Benefits

- First query: ~$0.003-0.004
- Cached query: ~$0.000 (instant response)
- Cache hit rate: 60-70% in production
- Effective cost reduction: 90%+ vs GPT-5

---

## Troubleshooting

### Common Issues

**Empty Agent Outputs**
- Cause: GPT-5 reasoning_effort too high
- Fix: Set to "low" in agent configurations
- Reference: `docs/BUG_FIX_REPORT.md`

**Semantic Scholar Rate Limiting**
- System automatically falls back to arXiv
- 7-day caching reduces API calls
- Wait 1 minute between rapid tests

**Cache Not Working**
- Verify Redis is running: `docker ps | grep redis`
- Check health endpoint: `curl http://localhost:8000/health`
- View cache stats: `curl http://localhost:8000/cache/stats`

**Docker Build Slow**
- First build takes 10-15 minutes (ML dependencies)
- Subsequent builds use cache
- Pre-built image available (coming soon)

---

## Documentation

### Key Documents

- `docs/DOCUMENT_AUTOMATION.md` - Complete automation guide
- `docs/PARALLEL_EXECUTION_COMPLETE.md` - Performance optimization
- `docs/PICKUP_HERE.md` - Session resume guide
- `docs/WEEK2_PLAN.md` - ML routing implementation
- `docs/BUG_FIX_REPORT.md` - Known issues and fixes

### API References

- `docs/gpt5nano.md` - GPT-5 API documentation
- `docs/phase2.md` - Technical specifications
- `docs/readtom.md` - Architecture overview

---

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_system.py
python test_rag_system.py
```

### Code Quality

```bash
# Format
black src/ eval/ *.py

# Lint
flake8 src/ eval/ --max-line-length=120

# Type check
mypy src/ --ignore-missing-imports
```

### Contributing

1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Run test suite
5. Submit pull request

**Code Standards:**
- Black formatter (120 char lines)
- Type hints for all functions
- Docstrings for public methods
- Conventional Commits format

---

## Use Cases

### Business Consulting

- Comprehensive business analysis
- Strategic planning recommendations
- Market research with citations
- Competitive analysis

### Financial Analysis

- Unit economics modeling
- Pricing strategy optimization
- ROI calculations
- Revenue projections

### Operations Consulting

- Process optimization
- Efficiency analysis
- Resource allocation
- Workflow improvements

### Growth Strategy

- Customer acquisition planning
- Retention optimization
- Market expansion analysis
- Lead generation strategies

---

## Roadmap

### Completed

- Core multi-agent system
- Research augmentation (RAG)
- ML routing classifier
- Parallel execution
- Redis caching
- Document automation (PowerPoint + Excel)
- Docker deployment

### In Progress

- ML classifier retraining (77% → 95% accuracy)
- Production monitoring
- Performance optimization

### Planned

- Additional research sources (Google Scholar, PubMed)
- Web UI frontend
- Additional agent types
- Advanced caching strategies
- Multi-language support

---

## License

[Add your license here]

## Project Information

- **Built for:** Self-hosted business intelligence
- **Technology:** GPT-5, DeepSeek, LangGraph, FastAPI, Docker
- **Status:** Production-ready (Phase 3 complete)
- **Last Updated:** November 15, 2025

---

## Support

For issues, questions, or contributions:
- Check documentation in `docs/`
- Review troubleshooting section
- Run test suite for diagnostics
- Create GitHub issue with details

---

Built with LangGraph, FastAPI, and modern LLM technology for self-hosted business intelligence.
