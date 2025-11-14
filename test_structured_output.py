#!/usr/bin/env python3
"""
Test script for Phase 1: Structured Agent Output

Tests that Financial Agent can output valid structured JSON
conforming to the AgentOutput schema.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.financial_modeling import FinancialModelingAgent
from src.schemas import validate_agent_output, check_output_quality


def test_structured_output():
    """Test Financial Agent structured output."""

    print("=" * 70)
    print("PHASE 1 TEST: Structured Agent Output")
    print("=" * 70)
    print()

    # Initialize agent
    print("1. Initializing Financial Agent...")
    agent = FinancialModelingAgent()
    print("   ✓ Agent initialized")
    print()

    # Test query
    query = "What are the unit economics for a SaaS company with $100 MRR per customer, 5% monthly churn, and $500 CAC?"

    print(f"2. Running analysis on query:")
    print(f"   '{query}'")
    print()

    try:
        # Get structured output
        print("3. Generating structured output...")
        output = agent.model_financials_structured(query)
        print("   ✓ Structured output generated")
        print()

        # Convert to dict for validation
        output_dict = output.model_dump()

        # Validate schema
        print("4. Validating against schema...")
        validation_result = validate_agent_output(output_dict)

        if validation_result.valid:
            print("   ✓ Schema validation PASSED")
        else:
            print("   ✗ Schema validation FAILED")
            for error in validation_result.errors:
                print(f"     - {error}")
            return False

        # Quality checks
        if validation_result.warnings:
            print(f"\n   ⚠️  {len(validation_result.warnings)} warnings:")
            for warning in validation_result.warnings:
                print(f"     - {warning}")

        print()

        # Display results
        print("5. Output Preview:")
        print("-" * 70)

        print(f"\n   Query: {output.query}")
        print(f"   Agent: {output.agent}")
        print(f"   Timestamp: {output.timestamp}")
        print(f"   Model: {output.metadata.model}")
        print(f"   Confidence: {output.metadata.confidence}")

        print(f"\n   Executive Summary:")
        print(f"   {output.findings.executive_summary[:200]}...")

        print(f"\n   Metrics ({len(output.findings.metrics)}):")
        for name, metric in list(output.findings.metrics.items())[:5]:
            print(f"     - {name}: {metric.value} {metric.unit} (confidence: {metric.confidence})")

        print(f"\n   Key Findings ({len(output.findings.key_findings)}):")
        for finding in output.findings.key_findings[:3]:
            print(f"     - {finding}")

        print(f"\n   Recommendations ({len(output.findings.recommendations)}):")
        for rec in output.findings.recommendations[:2]:
            print(f"     - [{rec.priority}] {rec.title}")
            print(f"       Impact: {rec.impact}")

        print()
        print("-" * 70)

        # Save to file
        output_file = "test_output.json"
        with open(output_file, 'w') as f:
            json.dump(output_dict, f, indent=2, default=str)

        print(f"\n6. Saved output to: {output_file}")
        print(f"   File size: {Path(output_file).stat().st_size} bytes")

        # Final summary
        print()
        print("=" * 70)
        print("✅ PHASE 1 TEST PASSED")
        print("=" * 70)
        print("\nNext steps:")
        print("  - Review test_output.json")
        print("  - Run: python src/schemas/validators.py test_output.json")
        print("  - Proceed to Phase 2: PowerPoint Generation")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_structured_output()
    sys.exit(0 if success else 1)
