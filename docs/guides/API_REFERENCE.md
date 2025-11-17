# API Reference

**Last Updated**: November 17, 2025

---

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### POST /query

**Description**: Execute a business intelligence query

**Request**:
```json
{
  "query": "How can I improve customer retention?",
  "use_rag": true,
  "use_ml_routing": true
}
```

**Response**:
```json
{
  "synthesis": "Comprehensive analysis...",
  "agents_consulted": ["market", "operations", "financial", "leadgen"],
  "query_complexity": "business",
  "research_used": false,
  "cache_hit": false,
  "processing_time": 69.2,
  "cost_usd": 0.043
}
```

---

### GET /health

**Description**: Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "cache": {"enabled": true, "backend": "Redis"},
  "models": {"strategy": "hybrid"},
  "timestamp": "2025-11-17T01:00:00Z"
}
```

---

### GET /cache/stats

**Description**: Cache statistics

**Response**:
```json
{
  "stats": {
    "enabled": true,
    "backend": "RedisCache",
    "hits": 150,
    "misses": 100,
    "hit_rate_percent": 60.0,
    "cost_savings_estimate": 45.0
  }
}
```

---

### POST /cache/clear

**Description**: Clear all cache

**Response**:
```json
{
  "message": "Cache cleared",
  "entries_removed": 42
}
```

---

### GET /docs

**Description**: Interactive API documentation (Swagger UI)

---

## Authentication

**Status**: Not yet implemented

**Planned**: JWT tokens + API keys

---

For more details, visit: http://localhost:8000/docs
