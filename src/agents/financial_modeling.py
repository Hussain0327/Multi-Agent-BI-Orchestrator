"""Financial Modeling Agent - specializes in financial analysis and projections."""
from typing import Dict, Any
import json
import re
from datetime import datetime
from src.unified_llm import UnifiedLLM
from src.schemas import AgentOutput, Findings, Metric, AgentMetadata


class FinancialModelingAgent:
    """Specialized agent for financial modeling and analysis."""

    def __init__(self):
        self.llm = UnifiedLLM(agent_type="financial")
        self.name = "financial_modeling_agent"
        self.description = "Specialized agent for financial modeling, ROI calculations, revenue projections, cost analysis, and financial planning."

        self.system_prompt = """You are a Financial Modeling Agent specializing in financial analysis and projections.

Your expertise includes:
- Financial modeling and forecasting
- ROI and NPV calculations
- Revenue and cost projections
- Profitability analysis
- Budget planning and optimization
- Financial risk assessment
- Investment evaluation and decision support

When creating financial models, provide:
1. Clear financial assumptions and methodology
2. Revenue projections with growth scenarios
3. Cost structure analysis and optimization opportunities
4. ROI calculations and payback periods
5. Profitability metrics and financial KPIs
6. Risk factors and sensitivity analysis
7. Financial recommendations with supporting data

**Citation Requirements**:
- When academic research is provided, reference it to support your financial models
- Format citations as: [Your insight] (Source: Author et al., Year)
- Include a "References" section at the end with full citations

Use the calculator tool for precise financial calculations. Present findings with clear metrics and actionable financial guidance."""

    def model_financials(
        self,
        query: str,
        calculator_results: Dict[str, Any] = None,
        research_context: str = None
    ) -> str:
        """Create detailed financial models and analysis.

        Args:
            query: Business query requiring financial analysis
            calculator_results: Optional calculation results to incorporate
            research_context: Optional academic research context with citations

        Returns:
            Financial analysis and recommendations (with citations if research provided)
        """
        user_prompt = f"""Create detailed financial models and analysis for the following business query:

{query}"""

        if research_context:
            user_prompt += f"\n\n{research_context}"

        if calculator_results:
            user_prompt += f"\n\nCalculation Results:\n{calculator_results}"

        user_prompt += """

Provide comprehensive financial analysis including:
- Revenue and cost projections
- ROI calculations and metrics
- Profitability assessment
- Budget recommendations
- Financial risks and opportunities
- Actionable financial guidance

Use specific numbers and financial metrics where possible."""

        if research_context:
            user_prompt += "\n\nCRITICAL CITATION REQUIREMENTS:"
            user_prompt += "\n- Use the EXACT citation format: (Source: Author et al., Year)"
            user_prompt += "\n- Cite sources for EVERY major claim or recommendation"
            user_prompt += "\n- Include a 'References' section at the end with full citations"

        try:
            return self.llm.generate(
                input_text=user_prompt,
                instructions=self.system_prompt,
                reasoning_effort="low",  # Fixed: "medium" uses all tokens for reasoning, no output
                text_verbosity="high",
                max_tokens=1500
            )

        except Exception as e:
            return f"Error in financial modeling: {str(e)}"

    def model_financials_structured(
        self,
        query: str,
        calculator_results: Dict[str, Any] = None,
        research_context: str = None
    ) -> AgentOutput:
        """
        Create financial analysis with structured JSON output.

        This method generates structured data suitable for document automation
        (PowerPoint, Excel generation).

        Args:
            query: Business query requiring financial analysis
            calculator_results: Optional calculation results
            research_context: Optional research context

        Returns:
            AgentOutput: Structured output conforming to schema
        """
        # First, get the text analysis
        text_analysis = self.model_financials(query, calculator_results, research_context)

        # Build structured prompt for data extraction
        extraction_prompt = f"""Given this financial analysis, extract structured data in JSON format:

ANALYSIS:
{text_analysis}

Extract the following in valid JSON format:

{{
  "executive_summary": "1-2 paragraph summary",
  "metrics": {{
    "metric_name": {{"value": number, "unit": "string", "confidence": "high|medium|low", "source": "calculation|assumption"}},
    ...
  }},
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "risks": ["risk 1", "risk 2"],
  "recommendations": [
    {{
      "title": "recommendation title",
      "priority": "high|medium|low",
      "impact": "expected impact description",
      "rationale": "why this recommendation",
      "action_items": ["action 1", "action 2"]
    }}
  ]
}}

Extract ALL metrics mentioned (CAC, LTV, ROI, revenue, costs, etc.) with their actual values.
Return ONLY valid JSON, no additional text."""

        try:
            # Get structured data from LLM
            json_response = self.llm.generate(
                input_text=extraction_prompt,
                instructions="You are a data extraction assistant. Extract structured financial data from analysis text. Return ONLY valid JSON.",
                reasoning_effort="low",
                max_tokens=2000
            )

            # Clean and parse JSON
            json_str = json_response.strip()
            # Remove markdown code blocks if present
            json_str = re.sub(r'```json\s*', '', json_str)
            json_str = re.sub(r'```\s*$', '', json_str)

            extracted_data = json.loads(json_str)

            # Convert to Pydantic models
            metrics = {}
            for key, val in extracted_data.get("metrics", {}).items():
                metrics[key] = Metric(**val)

            findings = Findings(
                executive_summary=extracted_data.get("executive_summary", ""),
                metrics=metrics,
                narrative=text_analysis,  # Full text analysis as narrative
                key_findings=extracted_data.get("key_findings", []),
                risks=extracted_data.get("risks", []),
                recommendations=extracted_data.get("recommendations", [])
            )

            metadata = AgentMetadata(
                confidence="high",
                model=self.llm.get_current_provider(),
                tokens_used=None,  # TODO: Track tokens
                cost_usd=None,  # TODO: Track cost
                processing_time_seconds=None  # TODO: Track time
            )

            return AgentOutput(
                query=query,
                agent="financial",
                timestamp=datetime.now(),
                findings=findings,
                research_citations=[],  # TODO: Extract citations
                metadata=metadata
            )

        except json.JSONDecodeError as e:
            # Fallback: create minimal structured output from text
            print(f"⚠️  JSON extraction failed: {e}")
            print(f"Response was: {json_response[:200]}...")

            fallback_findings = Findings(
                executive_summary="See narrative for full analysis",
                narrative=text_analysis,
                key_findings=["Analysis generated successfully - see narrative"],
                recommendations=[]
            )

            return AgentOutput(
                query=query,
                agent="financial",
                timestamp=datetime.now(),
                findings=fallback_findings,
                metadata=AgentMetadata(
                    confidence="medium",
                    model=self.llm.get_current_provider()
                )
            )

        except Exception as e:
            # Error fallback
            error_findings = Findings(
                executive_summary=f"Error during financial analysis: {str(e)}",
                narrative=str(e),
                key_findings=[],
                recommendations=[]
            )

            return AgentOutput(
                query=query,
                agent="financial",
                timestamp=datetime.now(),
                findings=error_findings,
                metadata=AgentMetadata(
                    confidence="low",
                    model="error"
                )
            )
