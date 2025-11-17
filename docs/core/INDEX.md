# Documentation Index

**Business Intelligence Orchestrator v2.0** - Complete Documentation Map

Last Updated: November 17, 2025

---

## Start Here

**New to the project?** Start with these in order:

1. **[README.md](../../README.md)** - Project overview and quick start
2. **[PROJECT_STATUS.md](core/PROJECT_STATUS.md)** - Current status and what's been built
3. **[QUICK_REFERENCE.md](core/QUICK_REFERENCE.md)** - Commands and common tasks
4. **[DEVELOPMENT_TIMELINE.md](guides/DEVELOPMENT_TIMELINE.md)** - Day-by-day project history

---

## Documentation Structure

```
docs_cleaned/
 core/               # Essential documents
    INDEX.md       # This file
    PROJECT_STATUS.md
    QUICK_REFERENCE.md

 features/          # Feature-specific guides
    DOCUMENT_AUTOMATION.md
    PARALLEL_EXECUTION.md
    CACHING_LAYER.md
    DEEPSEEK_INTEGRATION.md
    RAG_SYSTEM.md

 guides/            # How-to guides
    DEVELOPMENT_TIMELINE.md
    API_REFERENCE.md
    DEPLOYMENT_GUIDE.md
    TROUBLESHOOTING.md

 archive/           # Historical documents
     sessions/      # Daily work logs
     experiments/   # Test results
     legacy/        # Outdated docs
```

---

## Core Documentation

### [PROJECT_STATUS.md](core/PROJECT_STATUS.md)
**Complete system status and capabilities**

- All completed phases (1, 2, 3)
- Performance metrics
- Cost analysis
- Tech stack
- Known issues
- What's remaining

**When to read**: Want to understand current state

---

### [QUICK_REFERENCE.md](core/QUICK_REFERENCE.md)
**Commands, configs, and quick answers**

- Quick start commands
- Cost comparisons
- Model strategy configuration
- Performance metrics
- Common issues
- API endpoints
- Useful commands

**When to read**: Need a quick answer or command

---

### [INDEX.md](core/INDEX.md)
**This file - Documentation map**

- Complete docs structure
- Where to find everything
- Recommended reading order

**When to read**: Looking for specific documentation

---

## Feature Documentation

### [DOCUMENT_AUTOMATION.md](features/DOCUMENT_AUTOMATION.md)
**PowerPoint + Excel generation**

- How document automation works
- Pydantic schema architecture
- PowerPoint template structure
- Excel workbook layout
- Usage examples
- Complete automation pipeline

**When to read**: Want to understand or use document generation

---

### [PARALLEL_EXECUTION.md](features/PARALLEL_EXECUTION.md)
**Performance optimization (2.1x speedup)**

- Query complexity classification
- Parallel agent execution
- Fast-answer path
- Performance benchmarks
- Implementation details

**When to read**: Want to understand performance improvements

---

### [CACHING_LAYER.md](features/CACHING_LAYER.md)
**Redis caching (60-138x speedup)**

- Multi-layer caching strategy
- Redis + file fallback
- Cache TTLs and invalidation
- Performance gains
- Docker integration

**When to read**: Want to understand caching system

---

### [DEEPSEEK_INTEGRATION.md](features/DEEPSEEK_INTEGRATION.md)
**90% cost savings via hybrid routing**

- DeepSeek API integration
- Hybrid routing strategy
- Cost analysis
- Per-agent configuration
- Automatic fallback

**When to read**: Want to understand cost optimization

---

### [RAG_SYSTEM.md](features/RAG_SYSTEM.md)
**Research-augmented generation**

- ChromaDB vector store
- Semantic Scholar + arXiv integration
- Research synthesis agent
- Citation formatting
- Caching strategy

**When to read**: Want to understand research features

---

## Guides

### [DEVELOPMENT_TIMELINE.md](guides/DEVELOPMENT_TIMELINE.md)
**Complete day-by-day project history**

- Phase 0: Foundation (Oct 30)
- Phase 1: Modernization (Nov 4)
- Phase 2 Week 1: RAG (Nov 5)
- Phase 2 Week 2: ML + Eval (Nov 6-7)
- Phase 2 Week 3: Performance (Nov 13-15)
- Phase 3: Automation (Nov 14-15)
- Decisions made and lessons learned

**When to read**: Want to understand how the project evolved

---

### [API_REFERENCE.md](guides/API_REFERENCE.md)
**Complete API documentation**

- All endpoints documented
- Request/response examples
- Authentication (when implemented)
- Rate limiting
- Error codes

**When to read**: Building integrations or using the API

---

### [DEPLOYMENT_GUIDE.md](guides/DEPLOYMENT_GUIDE.md)
**How to deploy**

- Docker Compose (local/testing)
- Cloud deployment (AWS, GCP, Azure)
- Environment variables
- Monitoring setup
- Production considerations

**When to read**: Deploying to production

---

### [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md)
**Common issues and solutions**

- Error messages and fixes
- Performance problems
- Configuration issues
- Development tips
- Debugging strategies

**When to read**: Something isn't working

---

## Archive

Historical documents moved here for reference:

### `archive/sessions/`
- Daily work logs (PICKUP_HERE.md, TODAY_*.md, etc.)
- Session planning documents
- Temporary notes

### `archive/experiments/`
- Bug reports (BUG_FIX_REPORT.md)
- Test findings (PHASE2_TEST_FINDINGS.md)
- Experiment results

### `archive/legacy/`
- Outdated documentation
- Previous versions
- Replaced guides

**When to access**: Historical context or specific details from development

---

## Documentation by Use Case

### "I want to understand what this project does"
1. [README.md](../../README.md)
2. [PROJECT_STATUS.md](core/PROJECT_STATUS.md)
3. [DEVELOPMENT_TIMELINE.md](guides/DEVELOPMENT_TIMELINE.md)

### "I want to run the system"
1. [README.md](../../README.md) - Quick Start section
2. [QUICK_REFERENCE.md](core/QUICK_REFERENCE.md)
3. [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md)

### "I want to use document automation"
1. [DOCUMENT_AUTOMATION.md](features/DOCUMENT_AUTOMATION.md)
2. `test_document_automation.py` (code example)
3. [API_REFERENCE.md](guides/API_REFERENCE.md)

### "I want to understand the cost savings"
1. [DEEPSEEK_INTEGRATION.md](features/DEEPSEEK_INTEGRATION.md)
2. [QUICK_REFERENCE.md](core/QUICK_REFERENCE.md) - Cost section
3. [PROJECT_STATUS.md](core/PROJECT_STATUS.md) - Cost analysis

### "I want to deploy to production"
1. [DEPLOYMENT_GUIDE.md](guides/DEPLOYMENT_GUIDE.md)
2. [QUICK_REFERENCE.md](core/QUICK_REFERENCE.md) - Config section
3. [PROJECT_STATUS.md](core/PROJECT_STATUS.md) - What's remaining

### "Something is broken"
1. [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md)
2. [QUICK_REFERENCE.md](core/QUICK_REFERENCE.md) - Common issues
3. `test_*.py` files for diagnostics

---

## Documentation Statistics

- **Total files**: 36 markdown files
- **Total lines**: ~12,000+ lines
- **Core docs**: 3 files (essential reading)
- **Feature docs**: 5 files (feature-specific)
- **Guides**: 4 files (how-to)
- **Archived**: 24 files (historical reference)

---

## Quick Search

### By Topic

**Performance**:
- [PARALLEL_EXECUTION.md](features/PARALLEL_EXECUTION.md)
- [CACHING_LAYER.md](features/CACHING_LAYER.md)

**Cost**:
- [DEEPSEEK_INTEGRATION.md](features/DEEPSEEK_INTEGRATION.md)
- [PROJECT_STATUS.md](core/PROJECT_STATUS.md) - Cost analysis

**Features**:
- [DOCUMENT_AUTOMATION.md](features/DOCUMENT_AUTOMATION.md)
- [RAG_SYSTEM.md](features/RAG_SYSTEM.md)

**Development**:
- [DEVELOPMENT_TIMELINE.md](guides/DEVELOPMENT_TIMELINE.md)
- [PROJECT_STATUS.md](core/PROJECT_STATUS.md)

**Operations**:
- [DEPLOYMENT_GUIDE.md](guides/DEPLOYMENT_GUIDE.md)
- [TROUBLESHOOTING.md](guides/TROUBLESHOOTING.md)
- [API_REFERENCE.md](guides/API_REFERENCE.md)

---

## Documentation Quality Standards

All cleaned documentation follows these standards:

-  **Accurate**: Reflects current system state (Nov 17, 2025)
-  **Complete**: No "TODO" or placeholder sections
-  **Organized**: Clear structure with headers
-  **Concise**: No redundant information
-  **Actionable**: Includes examples and commands
-  **Up-to-date**: References correct file names and paths

---

## Contributing to Documentation

When updating docs:

1. Update "Last Updated" date
2. Keep consistent formatting
3. Use absolute paths for links
4. Test all code examples
5. Update this INDEX if adding new docs

---

## Additional Resources

- **Code Repository**: `/workspaces/multi_agent_workflow/`
- **Tests**: `test_*.py` files in root
- **Evaluation**: `eval/` directory
- **Docker**: `docker-compose.yml`
- **LangSmith**: https://smith.langchain.com

---

**Last Updated**: November 17, 2025
**Version**: 2.0
**Status**: Documentation cleaned and organized
