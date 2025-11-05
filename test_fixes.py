#!/usr/bin/env python3
"""Test all fixes end-to-end."""

from src.langgraph_orchestrator import LangGraphOrchestrator

print("="*70)
print("TESTING ALL FIXES")
print("="*70)

# Test non-RAG mode
print("\n=== TEST 1: Non-RAG Mode ===")
orch = LangGraphOrchestrator(enable_rag=False)
result = orch.orchestrate("What pricing model should I use for a new SaaS product?", use_memory=False)

print(f"\nAgents consulted: {result['agents_consulted']}")
print(f"Recommendation length: {len(result['recommendation'])} chars")
print(f"Recommendation preview: {result['recommendation'][:200]}")

print(f"\nDetailed findings:")
for agent, finding in result['detailed_findings'].items():
    print(f"  {agent}: {len(finding)} chars")

# Check if all expected agents ran
expected = set(result['agents_consulted'])
found = set([k.replace('_', '') for k, v in result['detailed_findings'].items() if v])
print(f"\nExpected agents: {expected}")
print(f"Agents with output: {found}")

success_check = (
    len(result['recommendation']) > 100 and
    len(result['detailed_findings']['market_analysis']) > 100 and
    len(result['detailed_findings']['financial_modeling']) > 100
)

if success_check:
    print("\n✅ ALL FIXES WORKING! Agents produce output and synthesis works!")
else:
    print("\n❌ FIXES NOT WORKING - still getting empty output")

print("\n" + "="*70)
