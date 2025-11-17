# Deployment Guide

**Last Updated**: November 17, 2025

---

## Docker Compose (Recommended)

### Quick Start

```bash
# Clone repository
git clone <your-repo-url>
cd multi_agent_workflow

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Verify
curl http://localhost:8000/health
```

### Services

- **Redis**: Port 6379 (caching)
- **Orchestrator**: Port 8000 (API)

---

## Local Python

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python cli.py  # Interactive CLI
# OR
uvicorn src.main:app --reload  # API server
```

---

## Environment Variables

### Required

```bash
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-5-nano
```

### Recommended

```bash
DEEPSEEK_API_KEY=sk-...
MODEL_STRATEGY=hybrid
CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

### Optional

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
```

---

## Cloud Deployment

### AWS (ECS)

```bash
# Build image
docker build -t bi-orchestrator .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag bi-orchestrator:latest <account>.dkr.ecr.us-east-1.amazonaws.com/bi-orchestrator:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/bi-orchestrator:latest

# Deploy to ECS (use AWS Console or CLI)
```

### GCP (Cloud Run)

```bash
# Build and deploy
gcloud run deploy bi-orchestrator \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure (Container Instances)

```bash
# Build and push to ACR
az acr build --registry <registry-name> --image bi-orchestrator:latest .

# Deploy
az container create \
  --resource-group <rg-name> \
  --name bi-orchestrator \
  --image <registry-name>.azurecr.io/bi-orchestrator:latest \
  --ports 8000
```

---

## Production Considerations

- Use managed Redis (AWS ElastiCache, GCP Memorystore, Azure Cache)
- Set up HTTPS with reverse proxy (nginx)
- Configure authentication and rate limiting
- Enable monitoring (Prometheus + Grafana)
- Set resource limits in docker-compose.yml
- Use secrets management (not .env file)

---

For more details, see README.md Quick Start section.
