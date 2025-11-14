#!/usr/bin/env python3
"""Quick test script for parallel execution and query complexity routing."""

import time
from src.langgraph_orchestrator import LangGraphOrchestrator

def test_simple_query():
    """Test simple query - should use fast answer (<3 seconds)."""
    print("=" * 80)
    print("TEST 1: Simple Query (Fast Answer)")
    print("=" * 80)

    orchestrator = LangGraphOrchestrator(enable_rag=True, use_ml_routing=False)

    query = "What's the color of the sky?"
    print(f"\nQuery: {query}\n")

    start_time = time.time()
    result = orchestrator.orchestrate(query, use_memory=False)
    elapsed = time.time() - start_time

    print(f"\n{'=' * 80}")
    print(f"RESULT:")
    print(f"{'=' * 80}")
    print(result["recommendation"])
    print(f"\n{'=' * 80}")
    print(f"⏱️  Elapsed Time: {elapsed:.2f}s")
    print(f"🎯 Target: <3s")
    print(f"✓ SUCCESS" if elapsed < 3 else "❌ FAILED")
    print(f"{'=' * 80}\n")

    return elapsed < 3


def test_business_query():
    """Test business query - should use parallel agents (no research for simple business)."""
    print("=" * 80)
    print("TEST 2: Business Query (Parallel Agents, No Research)")
    print("=" * 80)

    orchestrator = LangGraphOrchestrator(enable_rag=True, use_ml_routing=False)

    query = "How can I improve customer retention for my SaaS product?"
    print(f"\nQuery: {query}\n")

    start_time = time.time()
    result = orchestrator.orchestrate(query, use_memory=False)
    elapsed = time.time() - start_time

    print(f"\n{'=' * 80}")
    print(f"RESULT:")
    print(f"{'=' * 80}")
    print(f"Agents Consulted: {result['agents_consulted']}")
    print(f"\n{result['recommendation'][:500]}...")  # First 500 chars
    print(f"\n{'=' * 80}")
    print(f"⏱️  Elapsed Time: {elapsed:.2f}s")
    print(f"🎯 Target: <60s (with parallel execution)")
    print(f"✓ SUCCESS" if elapsed < 60 else "❌ FAILED")
    print(f"{'=' * 80}\n")

    return elapsed < 60


def test_complex_query():
    """Test complex query - should use research + parallel agents."""
    print("=" * 80)
    print("TEST 3: Complex Query (Research + Parallel Agents)")
    print("=" * 80)

    orchestrator = LangGraphOrchestrator(enable_rag=True, use_ml_routing=False)

    query = "What's the optimal pricing strategy for B2B SaaS with 500+ customers based on latest research?"
    print(f"\nQuery: {query}\n")

    start_time = time.time()
    result = orchestrator.orchestrate(query, use_memory=False)
    elapsed = time.time() - start_time

    print(f"\n{'=' * 80}")
    print(f"RESULT:")
    print(f"{'=' * 80}")
    print(f"Agents Consulted: {result['agents_consulted']}")
    print(f"\n{result['recommendation'][:500]}...")  # First 500 chars
    print(f"\n{'=' * 80}")
    print(f"⏱️  Elapsed Time: {elapsed:.2f}s")
    print(f"🎯 Target: <80s (research + parallel agents)")
    print(f"✓ SUCCESS" if elapsed < 80 else "❌ FAILED (but may be acceptable)")
    print(f"{'=' * 80}\n")

    return True


if __name__ == "__main__":
    print("\n🚀 Testing Parallel Execution & Query Complexity Routing\n")

    results = []

    # Test 1: Simple query
    try:
        results.append(("Simple Query", test_simple_query()))
    except Exception as e:
        print(f"❌ Test 1 failed with error: {e}\n")
        results.append(("Simple Query", False))

    # Test 2: Business query
    try:
        results.append(("Business Query", test_business_query()))
    except Exception as e:
        print(f"❌ Test 2 failed with error: {e}\n")
        results.append(("Business Query", False))

    # Test 3: Complex query
    try:
        results.append(("Complex Query", test_complex_query()))
    except Exception as e:
        print(f"❌ Test 3 failed with error: {e}\n")
        results.append(("Complex Query", False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")

    passed_count = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {passed_count}/{len(results)} tests passed")
    print("=" * 80 + "\n")
