#!/usr/bin/env python3
"""Test script to verify the Phase 1 implementation."""
import sys
from src.config import Config
from src.langgraph_orchestrator import LangGraphOrchestrator

def main():
    print("=" * 70)
    print("Business Intelligence Orchestrator v2 - System Test")
    print("=" * 70)
    print()

    # Test 1: Configuration
    print("✓ Test 1: Configuration")
    print(f"  Model: {Config.OPENAI_MODEL}")
    print(f"  GPT-5: {Config.is_gpt5()}")
    print(f"  LangSmith Tracing: {Config.LANGCHAIN_TRACING_V2}")
    print()

    # Test 2: Orchestrator Initialization
    print("✓ Test 2: Initializing LangGraph Orchestrator")
    try:
        orchestrator = LangGraphOrchestrator()
        print("  LangGraph orchestrator initialized successfully")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        sys.exit(1)
    print()

    # Test 3: Simple Query (if user wants to test with real API)
    print("Test 3: Query Execution")
    print("  Note: This will make actual API calls to OpenAI")
    print()

    response = input("  Do you want to test a query? (y/n): ").strip().lower()

    if response == 'y':
        test_query = "What are the best practices for pricing a SaaS product?"
        print(f"\n  Query: {test_query}")
        print("  Processing...")
        print()

        try:
            result = orchestrator.orchestrate(test_query, use_memory=False)

            print("  ✓ Query processed successfully!")
            print(f"  Agents consulted: {', '.join(result['agents_consulted'])}")
            print()
            print("  Recommendation (first 500 chars):")
            print("  " + "-" * 66)
            print("  " + result['recommendation'][:500] + "...")
            print()

        except Exception as e:
            print(f"  ✗ Error during query execution: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("  Skipping query test")
        print()

    print("=" * 70)
    print("System test complete!")
    print()
    print("Next steps:")
    print("  1. Get LangSmith API key: https://smith.langchain.com/settings")
    print("  2. Add to .env: LANGCHAIN_API_KEY=your_key")
    print("  3. Start CLI: python cli.py")
    print("  4. Start API: uvicorn src.main:app --reload")
    print("  5. View traces: https://smith.langchain.com")
    print("=" * 70)

if __name__ == "__main__":
    main()
