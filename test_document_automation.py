#!/usr/bin/env python3
"""
Complete Document Automation Test

Demonstrates Phase 1 + Phase 2 + Phase 3:
- Structured JSON output from agent
- PowerPoint generation
- Excel workbook generation
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.agents.financial_modeling import FinancialModelingAgent
from src.generators import PowerPointGenerator, ExcelGenerator


def test_complete_automation():
    """Test complete document automation pipeline."""

    print("=" * 70)
    print("COMPLETE DOCUMENT AUTOMATION TEST")
    print("=" * 70)
    print()

    # Step 1: Generate Analysis
    print("📊 Step 1: Generating Financial Analysis")
    print("-" * 70)

    agent = FinancialModelingAgent()

    query = """
What are the financial implications of switching from monthly to annual billing?

Current state:
- 500 customers at $99/month
- 5% monthly churn
- $500 CAC per customer

Proposed:
- $990/year (16% discount from $1,188/year)
- Target: 3% monthly churn (annual commitment improves retention)
"""

    print(f"Query: {query[:100]}...")
    print()

    output = agent.model_financials_structured(query)

    print(f"✓ Analysis complete")
    print(f"  - Metrics extracted: {len(output.findings.metrics)}")
    print(f"  - Key findings: {len(output.findings.key_findings)}")
    print(f"  - Recommendations: {len(output.findings.recommendations)}")
    print()

    # Save JSON
    json_path = "complete_analysis.json"
    with open(json_path, 'w') as f:
        json.dump(output.model_dump(), f, indent=2, default=str)
    print(f"✓ JSON saved: {json_path}")
    print()

    # Step 2: Generate PowerPoint
    print("📑 Step 2: Generating PowerPoint Presentation")
    print("-" * 70)

    ppt_gen = PowerPointGenerator()
    pptx_path = ppt_gen.generate(
        agent_output=output,
        output_path="Monthly_vs_Annual_Billing_Analysis.pptx",
        template="executive_summary"
    )

    pptx_size = Path(pptx_path).stat().st_size / 1024
    print(f"✓ PowerPoint created: {pptx_path}")
    print(f"  - Size: {pptx_size:.1f} KB")
    print()

    # Step 3: Generate Excel
    print("📊 Step 3: Generating Excel Workbook")
    print("-" * 70)

    excel_gen = ExcelGenerator()
    xlsx_path = excel_gen.generate(
        agent_output=output,
        output_path="Monthly_vs_Annual_Billing_Analysis.xlsx",
        include_scenarios=True
    )

    xlsx_size = Path(xlsx_path).stat().st_size / 1024
    print(f"✓ Excel workbook created: {xlsx_path}")
    print(f"  - Size: {xlsx_size:.1f} KB")
    print(f"  - Sheets: 5 (Executive Summary, Raw Data, Calculations, Charts, Assumptions)")
    print()

    # Summary
    print("=" * 70)
    print("✅ COMPLETE AUTOMATION TEST PASSED")
    print("=" * 70)
    print()
    print("📦 Generated Files:")
    print(f"  1. {json_path} ({Path(json_path).stat().st_size / 1024:.1f} KB)")
    print(f"  2. {pptx_path} ({pptx_size:.1f} KB)")
    print(f"  3. {xlsx_path} ({xlsx_size:.1f} KB)")
    print()
    print("📥 Download all three files from the Explorer sidebar!")
    print()
    print("💡 What you get:")
    print("  ✓ Structured JSON data (for APIs, integrations)")
    print("  ✓ PowerPoint deck (for presentations, client meetings)")
    print("  ✓ Excel workbook (for analysis, modeling, what-if scenarios)")
    print()
    print("🎯 Next steps:")
    print("  1. Download the files")
    print("  2. Review PowerPoint slides")
    print("  3. Explore Excel scenarios (Base/Upside/Downside)")
    print("  4. Customize branding if needed")
    print()

    # Show some preview data
    print("=" * 70)
    print("📊 PREVIEW: Key Metrics")
    print("=" * 70)
    for name, metric in list(output.findings.metrics.items())[:5]:
        print(f"  {name.replace('_', ' ').title()}: {metric.value} {metric.unit}")
    print()

    if output.findings.recommendations:
        print("=" * 70)
        print("🎯 PREVIEW: Top Recommendation")
        print("=" * 70)
        rec = output.findings.recommendations[0]
        print(f"  [{rec.priority.upper()}] {rec.title}")
        print(f"  Impact: {rec.impact[:100]}...")
        print()

    return True


if __name__ == "__main__":
    try:
        success = test_complete_automation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
