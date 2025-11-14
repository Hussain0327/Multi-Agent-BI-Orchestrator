"""
Structured schemas for agent outputs.

Enables document automation (PowerPoint, Excel generation) by enforcing
canonical JSON output format from all agents.
"""

from .agent_output import (
    Metric,
    DataTable,
    ChartSpec,
    Recommendation,
    Citation,
    Findings,
    AgentMetadata,
    AgentOutput,
    SynthesisOutput
)

from .validators import (
    ValidationResult,
    validate_agent_output,
    validate_synthesis_output,
    check_output_quality,
    validate_chart_spec,
    validate_data_table,
    validate_metrics_consistency,
    validate_json_file,
    export_json_schema
)

__all__ = [
    # Models
    "Metric",
    "DataTable",
    "ChartSpec",
    "Recommendation",
    "Citation",
    "Findings",
    "AgentMetadata",
    "AgentOutput",
    "SynthesisOutput",

    # Validators
    "ValidationResult",
    "validate_agent_output",
    "validate_synthesis_output",
    "check_output_quality",
    "validate_chart_spec",
    "validate_data_table",
    "validate_metrics_consistency",
    "validate_json_file",
    "export_json_schema",
]
