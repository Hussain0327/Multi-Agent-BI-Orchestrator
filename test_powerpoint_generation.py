#!/usr/bin/env python3
"""
Test PowerPoint generation from structured agent output.

Phase 2 demonstration: Financial analysis → PowerPoint deck
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.agents.financial_modeling import FinancialModelingAgent
from src.generators import PowerPointGenerator
from src.schemas import AgentOutput


def test_powerpoint_generation():
    """Test PowerPoint generation end-to-end."""

    print("=" * 70)
    print("PHASE 2 TEST: PowerPoint Generation")
    print("=" * 70)
    print()

    # Step 1: Generate fresh analysis (or load existing)
    print("1. Generating financial analysis...")

    use_existing = Path("test_output.json").exists()

    if use_existing:
        print("   Loading existing test_output.json")
        with open("test_output.json", "r") as f:
            output_dict = json.load(f)
        agent_output = AgentOutput(**output_dict)
    else:
        print("   Running new financial analysis...")
        agent = FinancialModelingAgent()
        agent_output = agent.model_financials_structured(
            "What are the unit economics for a SaaS company with $100 MRR per customer, 5% monthly churn, and $500 CAC?"
        )

    print(f"   ✓ Analysis complete")
    print(f"     - {len(agent_output.findings.metrics)} metrics")
    print(f"     - {len(agent_output.findings.key_findings)} key findings")
    print(f"     - {len(agent_output.findings.recommendations)} recommendations")
    print()

    # Step 2: Generate PowerPoint
    print("2. Generating PowerPoint presentation...")

    generator = PowerPointGenerator()

    pptx_path = generator.generate(
        agent_output=agent_output,
        output_path="financial_analysis_deck.pptx",
        template="executive_summary"
    )

    print(f"   ✓ PowerPoint generated: {pptx_path}")
    print()

    # Step 3: Summary
    print("3. Presentation Summary:")
    print("-" * 70)

    # Count slides (approximate based on content)
    slide_count = 1  # Title
    slide_count += 1  # Executive summary
    slide_count += 1  # Context
    slide_count += 1  # Key findings

    # Metrics slides (1 per 6 metrics)
    if agent_output.findings.metrics:
        slide_count += (len(agent_output.findings.metrics) + 5) // 6

    # Risks
    if agent_output.findings.risks:
        slide_count += 1

    # Recommendations (1 per recommendation)
    slide_count += len(agent_output.findings.recommendations)

    # Next steps
    slide_count += 1

    # Appendix
    if agent_output.research_citations:
        slide_count += 1

    print(f"   Estimated slides: {slide_count}")
    print(f"   File: {pptx_path}")
    print(f"   Size: {Path(pptx_path).stat().st_size / 1024:.1f} KB")
    print()

    print("-" * 70)
    print()

    # Step 4: What's in the deck
    print("4. Deck Contents:")
    print("-" * 70)
    slides = [
        "1. Title Slide (Branded cover)",
        "2. Executive Summary (High-level overview + top metrics)",
        "3. Context (Question, why it matters, analysis details)",
        "4. Key Findings (Bullet points)",
        f"5-{4 + (len(agent_output.findings.metrics) + 5) // 6}. Key Metrics (Visual metrics)",
    ]

    current_slide = 5 + (len(agent_output.findings.metrics) + 5) // 6

    if agent_output.findings.risks:
        slides.append(f"{current_slide}. Risks & Considerations")
        current_slide += 1

    for i, rec in enumerate(agent_output.findings.recommendations):
        slides.append(f"{current_slide + i}. Recommendation: {rec.title} ({rec.priority} priority)")

    current_slide += len(agent_output.findings.recommendations)
    slides.append(f"{current_slide}. Next Steps (Action items)")

    if agent_output.research_citations:
        current_slide += 1
        slides.append(f"{current_slide}. References (Citations)")

    for slide_desc in slides:
        print(f"   {slide_desc}")

    print()
    print("-" * 70)
    print()

    # Final instructions
    print("=" * 70)
    print("✅ PHASE 2 TEST PASSED")
    print("=" * 70)
    print()
    print("📊 Your PowerPoint is ready!")
    print()
    print("Next steps:")
    print(f"  1. Open: {pptx_path}")
    print("  2. Review the slides")
    print("  3. Customize branding if needed")
    print("  4. Share with clients!")
    print()
    print("💡 To generate with different data:")
    print("   - Modify query in test_structured_output.py")
    print("   - Run: python test_structured_output.py")
    print("   - Run: python test_powerpoint_generation.py")
    print()

    return True


if __name__ == "__main__":
    try:
        success = test_powerpoint_generation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
