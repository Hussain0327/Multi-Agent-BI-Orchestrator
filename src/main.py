"""FastAPI application for Business Intelligence Orchestrator."""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from src.langgraph_orchestrator import LangGraphOrchestrator
from src.config import Config

# Load environment variables
load_dotenv()

# Validate configuration (raises error if OpenAI key missing)
Config.validate()

# Initialize FastAPI app
app = FastAPI(
    title="Business Intelligence Orchestrator v2",
    description="LangGraph-powered multi-agent system with GPT-5, LangSmith tracing, and parallel execution",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = LangGraphOrchestrator()


# Pydantic models
class QueryRequest(BaseModel):
    query: str
    use_memory: Optional[bool] = True


class QueryResponse(BaseModel):
    query: str
    agents_consulted: list
    recommendation: str
    detailed_findings: dict


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Business Intelligence Orchestrator v2",
        "version": "2.0.0",
        "description": "LangGraph-powered multi-agent system with GPT-5, LangSmith tracing, and parallel execution",
        "features": [
            "GPT-5 Responses API with 40-80% cost reduction via caching",
            "LangGraph state machine for intelligent routing",
            "LangSmith tracing and monitoring",
            "Parallel agent execution",
            "Semantic routing (not keyword-based)"
        ],
        "agents": ["Market Analysis", "Operations Audit", "Financial Modeling", "Lead Generation"],
        "endpoints": {
            "/query": "POST - Submit a business query for analysis",
            "/history": "GET - Get conversation history",
            "/clear": "POST - Clear conversation memory",
            "/health": "GET - Health check"
        }
    }


@app.post("/query", response_model=QueryResponse)
async def analyze_query(request: QueryRequest):
    """Analyze a business query using the multi-agent orchestrator.

    The orchestrator will automatically determine which specialized agents to consult
    based on the query content and synthesize their findings.
    """
    try:
        result = orchestrator.orchestrate(
            query=request.query,
            use_memory=request.use_memory
        )

        return QueryResponse(
            query=result["query"],
            agents_consulted=result["agents_consulted"],
            recommendation=result["recommendation"],
            detailed_findings=result["detailed_findings"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history():
    """Get the conversation history."""
    try:
        history = orchestrator.get_conversation_history()
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear")
async def clear_memory():
    """Clear the conversation memory."""
    try:
        orchestrator.clear_memory()
        return {"message": "Conversation memory cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "openai_configured": bool(Config.OPENAI_API_KEY),
        "openai_model": Config.OPENAI_MODEL,
        "using_gpt5": Config.is_gpt5(),
        "langsmith_tracing": Config.LANGCHAIN_TRACING_V2,
        "langsmith_project": Config.LANGCHAIN_PROJECT if Config.LANGCHAIN_TRACING_V2 else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
