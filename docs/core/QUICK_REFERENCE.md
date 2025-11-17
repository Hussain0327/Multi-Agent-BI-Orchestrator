# Quick Reference Guide

**Business Intelligence Orchestrator v2.0** - Last Updated: Nov 17, 2025

---

## Quick Start Commands

```bash
# Docker deployment (recommended)
docker-compose up

# Interactive CLI
python cli.py

# Test complete automation pipeline
python test_document_automation.py

# Run evaluation benchmark
python eval/benchmark.py --mode both --num-queries 5

# Start API server (local)
uvicorn src.main:app --reload
```

---

## Cost Comparison

| Configuration | Cost/Query | Monthly (100/day) | Annual |
|---------------|-----------|-------------------|--------|
| GPT-5 Only | $0.30 | $900 | $10,800 |
| Hybrid (Current) | $0.043 | $129 | $1,548 |
| DeepSeek Only | $0.003 | $9 | $108 |
| **Savings (Hybrid)** | **$0.257** | **$771** | **$9,252** |

---

## Model Strategy (.env)

```bash
# Smart routing (recommended - current config)
MODEL_STRATEGY=hybrid

# Use DeepSeek for everything (cheapest)
MODEL_STRATEGY=deepseek

# Use GPT-5 for everything (highest quality)
MODEL_STRATEGY=gpt5
```

---

## Hybrid Routing Configuration

| Agent | Model | Temperature | Max Tokens | Purpose |
|-------|-------|-------------|------------|---------|
| Research Synthesis | DeepSeek-reasoner | 1.0 | 32,000 | Deep thinking, citations |
| Financial | DeepSeek-chat | 0.0 | 8,000 | Math, precision |
| Market | DeepSeek-chat | 1.3 | 4,000 | Creative analysis |
| Operations | DeepSeek-chat | 1.0 | 4,000 | Balanced analysis |
| LeadGen | DeepSeek-chat | 1.3 | 4,000 | Creative strategies |
| Router | DeepSeek-chat | 0.0 | 4,000 | Classification |
| Synthesis | DeepSeek-chat | 1.0 | 4,000 | Aggregation |

**All include automatic fallback to GPT-5 on errors**

---

## Performance Metrics

### Speed

| Query Type | Time | vs Sequential | Cache Hit |
|-----------|------|---------------|-----------|
| Simple | 5s | New capability | 0.1s |
| Business | 69s | **2.1x faster** | 0.5s |
| Complex | 153s | **1.5x faster** | 1s |

### Cost

| Metric | GPT-5 | Hybrid | Savings |
|--------|-------|--------|---------|
| Routing | $0.01 | $0.00 | 100% |
| Per Agent | $0.06 | $0.007 | 90% |
| Full Query | $0.30 | $0.043 | 86% |

### Cache

- Hit rate: 60-70% in production
- Speedup: 60-138x on cache hits
- Backend: Redis (prod) or File (dev)
- TTLs: 7 days (research), 1 day (agents)

---

## Current System Status

### Completed (Production Ready)

- LangGraph orchestration with conditional routing
- 5 specialized agents (all use UnifiedLLM)
- Parallel agent execution (2.1x speedup)
- ML routing classifier (77% accuracy)
- RAG system (ChromaDB + Semantic Scholar + arXiv)
- Redis caching layer (138x speedup)
- Document automation (PowerPoint + Excel)
- Docker Compose deployment
- DeepSeek hybrid routing (90% cost savings)
- LangSmith tracing

### Needs Improvement

- ML routing accuracy: 77% (target: 90%+)
- No authentication on API
- No monitoring/alerting

### ⏳ Planned

- Authentication & rate limiting
- Prometheus + Grafana monitoring
- Load testing
- Cloud deployment

---

## Quick Tests

### Test Complete System

```bash
# End-to-end automation test
python test_document_automation.py

# Expected output:
#  Analysis complete (structured JSON)
#  PowerPoint created: *.pptx
#  Excel workbook created: *.xlsx
```

### Test Individual Components

```bash
# Test RAG system
python test_rag_system.py

# Test DeepSeek integration
python test_deepseek.py

# Test structured output
python test_structured_output.py
```

### Verify Configuration

```bash
# Check model strategy
python -c "from src.config import Config; print(f'Strategy: {Config.MODEL_STRATEGY}')"

# Verify APIs
python -c "from src.config import Config; Config.validate()"
```

---

## Environment Variables

### Required

```bash
OPENAI_API_KEY=sk-proj-...        # GPT-5 access
OPENAI_MODEL=gpt-5-nano
```

### Optional (Recommended)

```bash
# DeepSeek (for 90% cost savings)
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_CHAT_MODEL=deepseek-chat
DEEPSEEK_REASONER_MODEL=deepseek-reasoner
MODEL_STRATEGY=hybrid

# LangSmith (for tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=business-intelligence-orchestrator

# Caching
CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

---

## Key Files & Directories

### Configuration

```
.env                    # Environment variables
src/config.py          # Configuration management
docker-compose.yml     # Docker deployment
```

### Core System

```
src/langgraph_orchestrator.py  # Main orchestration (688 lines)
src/unified_llm.py              # Hybrid LLM routing
src/cache.py                    # Multi-layer caching
```

### Agents (All Updated)

```
src/agents/market_analysis.py       #  Uses UnifiedLLM
src/agents/operations_audit.py      #  Uses UnifiedLLM
src/agents/financial_modeling.py    #  Uses UnifiedLLM
src/agents/lead_generation.py       #  Uses UnifiedLLM
src/agents/research_synthesis.py    #  Uses UnifiedLLM
```

### Document Generation

```
src/generators/powerpoint_generator.py  # PPT generation
src/generators/excel_generator.py      # Excel generation
src/generators/chart_generator.py      # Chart creation
src/schemas/agent_output.py           # Pydantic schemas
```

### ML & Evaluation

```
src/ml/routing_classifier.py     # SetFit classifier
models/routing_classifier.pkl    # Trained model (349MB)
eval/benchmark.py                # Evaluation framework
eval/test_queries.json           # Test dataset
```

---

## Common Issues & Solutions

### "DeepSeek API Error: 401"
**Solution**: Check `DEEPSEEK_API_KEY` in .env file

### "Redis connection failed"
**Solutions**:
- Check Redis is running: `docker ps | grep redis`
- System falls back to file cache automatically
- Start Redis: `docker-compose up redis`

### "Semantic Scholar rate limit"
**Solution**:
- System automatically caches for 7 days
- Falls back to arXiv if needed
- Wait 1 minute between rapid tests

### "Empty agent outputs"
**Solution**: Already fixed! (reasoning_effort set to "low")

### "Module not found"
**Solution**: `pip install -r requirements.txt`

---

## API Endpoints

```bash
# Query endpoint
POST /query
Body: {"query": "Your business question"}

# Health check
GET /health

# Cache statistics
GET /cache/stats

# Clear cache
POST /cache/clear

# API documentation
GET /docs  # Swagger UI
```

---

## Workflow Overview

```
User Query
    ↓
[Complexity Classifier] → simple | business | complex
    ↓
 SIMPLE
   → Fast Answer (5s, cached)

 BUSINESS
   → ML Router (select agents, 20ms)
   → 4 Parallel Agents (40s)
   → Synthesis (10s)
   Total: ~69s

 COMPLEX
    → Research Synthesis (60s, cached 7 days)
    → ML Router (select agents, 20ms)
    → 4 Parallel Agents (40s)
    → Synthesis (12s)
    Total: ~153s

All paths → Cache results (1-7 day TTL)
```

---

## ML Routing Performance

```
Overall Accuracy: 77%

Per-Agent F1 Scores:
 Market:     1.000  (perfect)
 Financial:  0.875   (good)
 Operations: 0.867   (good)
 LeadGen:    0.833   (needs improvement)

Speed: 20ms (vs 500ms GPT-5)
Cost: $0 (vs $0.01 GPT-5)
```

---

## Documentation Map

### Core Documentation
- `PROJECT_STATUS.md` - Complete system status
- `QUICK_REFERENCE.md` - This guide
- `README.md` - Main project overview

### Feature Guides
- `DOCUMENT_AUTOMATION.md` - PPT + Excel generation
- `PARALLEL_EXECUTION.md` - Performance optimization
- `CACHING_LAYER.md` - Redis caching setup
- `DEEPSEEK_INTEGRATION.md` - Cost optimization

### Development
- `DEVELOPMENT_TIMELINE.md` - Day-by-day history
- `PHASE_2_ROADMAP.md` - Complete roadmap
- `API_REFERENCE.md` - API documentation

---

## Useful Commands

### Development

```bash
# Format code
black src/ eval/ *.py

# Type check
mypy src/ --ignore-missing-imports

# Check git status
git status

# View recent commits
git log --oneline -10
```

### Monitoring

```bash
# Watch Docker logs
docker-compose logs -f

# Check Redis
docker exec -it bi-redis redis-cli KEYS "bi:*"

# Monitor API
watch -n 1 'curl -s http://localhost:8000/health | jq'
```

### Testing

```bash
# Quick smoke test
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 2+2?"}'

# Cache test (run twice, second should be instant)
time curl -X POST http://localhost:8000/query \
  -d '{"query": "Test query"}' -o /dev/null -s
```

---

## ⏱ Time Estimates

| Task | Time |
|------|------|
| Run 5-query eval | 15 min |
| Run 25-query eval | 90 min |
| Update documentation | 2-3 hours |
| ML routing improvement | 1-2 hours |
| Add authentication | 1 day |
| Add monitoring | 1-2 days |
| Load testing | 1 day |

---

## ROI Calculator

```python
queries_per_day = 100

# Current costs
gpt5_cost = 0.30 * queries_per_day  # $30/day
hybrid_cost = 0.043 * queries_per_day  # $4.30/day

# Savings
daily_savings = gpt5_cost - hybrid_cost
monthly_savings = daily_savings * 30
annual_savings = monthly_savings * 12

print(f"Daily savings: ${daily_savings:.2f}")
print(f"Monthly savings: ${monthly_savings:.2f}")
print(f"Annual savings: ${annual_savings:.2f}")

# Output:
# Daily savings: $25.70
# Monthly savings: $771.00
# Annual savings: $9,252.00
```

---

## System Health Check

```bash
# One-command health check
python -c "
import requests
import sys

try:
    # Check API
    health = requests.get('http://localhost:8000/health', timeout=5)
    assert health.status_code == 200

    # Check cache
    stats = requests.get('http://localhost:8000/cache/stats', timeout=5)
    cache_enabled = stats.json()['stats']['enabled']

    print(' API: Healthy')
    print(f' Cache: {\"Enabled\" if cache_enabled else \"Disabled\"}')
    print(' System: Operational')

except Exception as e:
    print(f' Error: {e}')
    sys.exit(1)
"
```

---

## Quick Links

- **LangSmith Dashboard**: https://smith.langchain.com
- **FastAPI Docs**: http://localhost:8000/docs
- **GitHub Repo**: [Your repo URL]
- **Documentation**: `docs_cleaned/` folder

---

**System Status**:  Production-Ready (Phase 3 Complete)
**Cost Savings**: 90% vs GPT-5 only
**Performance**: 2.1x faster (parallel execution)
**Next Priority**: Authentication + Monitoring

