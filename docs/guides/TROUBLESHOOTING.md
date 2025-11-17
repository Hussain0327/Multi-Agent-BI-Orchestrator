# Troubleshooting Guide

**Last Updated**: November 17, 2025

---

## Common Issues

### Empty Agent Outputs

**Symptom**: Agents return 0-character responses

**Cause**: `reasoning_effort` set too high (uses all tokens for thinking)

**Solution**:  Already fixed! All agents use `reasoning_effort="low"`

---

### DeepSeek API Error: 401

**Symptom**: `DEEPSEEK_API_KEY` error

**Solutions**:
1. Check `.env` file has `DEEPSEEK_API_KEY=sk-...`
2. Verify API key is valid at https://platform.deepseek.com
3. Fallback: Set `MODEL_STRATEGY=gpt5` to use only GPT-5

---

### Redis Connection Failed

**Symptom**: `Connection refused on port 6379`

**Solutions**:
1. Check Redis is running: `docker ps | grep redis`
2. Start Redis: `docker-compose up redis -d`
3. System auto-falls back to file cache (check logs)

**Verification**:
```bash
curl http://localhost:8000/cache/stats
```

---

### Semantic Scholar Rate Limit

**Symptom**: `Rate limit exceeded` from Semantic Scholar

**Solutions**:
- Wait 1 minute between rapid tests
- System automatically falls back to arXiv
- 7-day caching reduces API calls by 60%

**Prevention**: Don't run more than 20 queries in 5 minutes

---

### Module Not Found

**Symptom**: `ModuleNotFoundError: No module named 'xyz'`

**Solution**:
```bash
pip install -r requirements.txt
```

---

### Docker Build Slow

**Symptom**: First build takes 10-15 minutes

**Explanation**: Installing ML dependencies (torch, transformers, etc.)

**Solutions**:
- Subsequent builds use cache (faster)
- Pre-built image coming soon
- Use `docker-compose build --parallel` for faster builds

---

### Cache Not Working

**Symptom**: Every query is slow, no cache hits

**Diagnosis**:
```bash
curl http://localhost:8000/cache/stats
```

**Solutions**:
1. Check `CACHE_ENABLED=true` in `.env`
2. Verify Redis is running
3. Check cache stats show hits/misses
4. System should fall back to file cache automatically

---

### Citation Formatting Issues

**Status**:  Fixed (November 5, 2025)

**Previous Issue**: Inconsistent citation format

**Solution Applied**:
- Agent prompts updated with "CRITICAL CITATION REQUIREMENTS"
- APA format examples added
- 100% citation accuracy now

---

### Cost Higher Than Expected

**Diagnosis**:
```bash
# Check which model strategy is active
python -c "from src.config import Config; print(Config.MODEL_STRATEGY)"
```

**Solutions**:
1. Verify `MODEL_STRATEGY=hybrid` (not `gpt5`)
2. Check `DEEPSEEK_API_KEY` is set correctly
3. Review LangSmith traces for model usage
4. Cache hit rate should be 60%+ (reduces costs)

---

### Parallel Execution Not Working

**Status**:  Fixed (November 13, 2025)

**Previous Issue**: Agents still ran sequentially

**Solution**: Used `asyncio.run_in_executor()` with thread pools

**Verification**:
- Business queries should take ~69s (not 145s)
- Check logs show "parallel_agents" node

---

## Performance Issues

### Slow Queries

**Expected Times**:
- Simple: 5s
- Business: 69s
- Complex: 153s
- Cached: 0.1-1s

**If slower**:
1. Check cache hit rate (should be 60%+)
2. Verify parallel execution is working
3. Check network latency to APIs
4. Review LangSmith traces for bottlenecks

---

### High Memory Usage

**Expected**: 2-4 GB RAM

**If higher**:
1. Check ChromaDB collection size
2. Clear old cache entries
3. Restart services: `docker-compose restart`

---

## Development Tips

### View Logs

```bash
# Docker logs
docker-compose logs -f

# Specific service
docker-compose logs -f orchestrator
docker-compose logs -f redis
```

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
uvicorn src.main:app --reload --log-level debug
```

### Test Individual Components

```bash
# Test RAG system
python test_rag_system.py

# Test DeepSeek
python test_deepseek.py

# Test document automation
python test_document_automation.py
```

### Check Configuration

```bash
# Verify config
python -c "from src.config import Config; Config.validate()"

# Check model strategy
python -c "from src.config import Config; print(f'Strategy: {Config.MODEL_STRATEGY}')"
```

---

## API Errors

### 500 Internal Server Error

**Diagnosis**: Check server logs

**Common Causes**:
1. Invalid API keys
2. Model selection error
3. Agent error

**Solution**: Review logs for stack trace

---

### 429 Rate Limit

**Source**: External APIs (Semantic Scholar, OpenAI, DeepSeek)

**Solutions**:
- Wait before retrying
- Caching should prevent repeated calls
- Check if API key is valid

---

## Database Issues

### ChromaDB Errors

**Solution**:
```bash
# Clear and recreate
rm -rf chroma_db/
# System will recreate on next query
```

---

### Redis Data Corruption

**Solution**:
```bash
# Flush Redis
docker exec -it bi-redis redis-cli FLUSHDB

# Or restart with clean state
docker-compose down -v
docker-compose up -d
```

---

## Getting Help

1. **Check logs**: `docker-compose logs -f`
2. **Review tests**: Run test suite
3. **LangSmith**: Check traces at https://smith.langchain.com
4. **Documentation**: See docs_cleaned/ folder
5. **GitHub Issues**: Create issue with logs and error message

---

## Health Check Script

```bash
#!/bin/bash
# System health check

echo "=== System Health Check ==="

# Check API
if curl -s http://localhost:8000/health > /dev/null; then
    echo " API: Healthy"
else
    echo " API: Not responding"
fi

# Check Redis
if docker ps | grep redis > /dev/null; then
    echo " Redis: Running"
else
    echo " Redis: Not running"
fi

# Check cache
CACHE_ENABLED=$(curl -s http://localhost:8000/cache/stats | jq -r '.stats.enabled')
if [ "$CACHE_ENABLED" = "true" ]; then
    echo " Cache: Enabled"
else
    echo "  Cache: Disabled or not responding"
fi

echo ""
echo "For details: curl http://localhost:8000/health | jq"
```

---

## Common Warnings (Safe to Ignore)

- `UserWarning: TypedStorage is deprecated` - PyTorch warning, safe
- `pydantic deprecation warnings` - Non-critical
- `langchain UserWarning` - Informational only

---

**Need more help?** See QUICK_REFERENCE.md for commands and configuration
