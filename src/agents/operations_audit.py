"""Operations Audit Agent - specializes in process optimization and operational efficiency."""
from typing import Dict, Any
from src.gpt5_wrapper import GPT5Wrapper


class OperationsAuditAgent:
    """Specialized agent for operations audit and process optimization."""

    def __init__(self):
        self.gpt5 = GPT5Wrapper()
        self.name = "operations_audit_agent"
        self.description = "Specialized agent for operations audit, process optimization, efficiency analysis, workflow improvement, and operational excellence."

        self.system_prompt = """You are an Operations Audit Agent specializing in process optimization and operational efficiency.

Your expertise includes:
- Process analysis and workflow optimization
- Efficiency assessment and bottleneck identification
- Operational best practices and frameworks
- Scalability and capacity planning
- Automation opportunities and digital transformation
- Quality management and continuous improvement

When auditing operations, provide:
1. Current state assessment of processes and workflows
2. Identification of inefficiencies, bottlenecks, and pain points
3. Process optimization recommendations
4. Automation and technology opportunities
5. Scalability considerations and growth planning
6. Implementation roadmap and priorities

Focus on practical, actionable improvements that drive efficiency and scalability."""

    def audit(self, query: str) -> str:
        """Perform comprehensive operations audit.

        Args:
            query: Business query focused on operations

        Returns:
            Operations audit findings and optimization recommendations
        """
        user_prompt = f"""Perform a thorough operations audit for the following business query:

{query}

Analyze current processes, identify inefficiencies, and recommend optimizations focusing on:
- Efficiency improvements
- Bottleneck elimination
- Automation opportunities
- Scalability enhancements
- Best practices implementation

Provide specific, actionable recommendations with implementation priorities."""

        try:
            return self.gpt5.generate(
                input_text=user_prompt,
                instructions=self.system_prompt,
                reasoning_effort="medium",
                text_verbosity="high",
                max_output_tokens=1500
            )

        except Exception as e:
            return f"Error in operations audit: {str(e)}"
