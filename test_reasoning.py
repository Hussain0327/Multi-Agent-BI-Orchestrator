#!/usr/bin/env python3
"""Test with different reasoning efforts."""

from src.config import Config
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)

for effort in ["minimal", "low", "medium", "high"]:
    print(f"\n=== Testing with reasoning_effort={effort}, max_tokens=1500 ===")

    response = client.responses.create(
        model=Config.OPENAI_MODEL,
        input='Explain SaaS pricing strategies.',
        instructions='You are a business consultant.',
        reasoning={"effort": effort},
        text={"verbosity": "high"},
        max_output_tokens=1500
    )

    print(f"Status: {response.status}")
    print(f"output_text length: {len(response.output_text)}")
    print(f"output_tokens: {response.usage.output_tokens}")
    print(f"reasoning_tokens: {response.usage.output_tokens_details.reasoning_tokens}")

    if response.status == 'incomplete':
        print(f"Incomplete reason: {response.incomplete_details.reason if response.incomplete_details else 'unknown'}")

    if response.output_text:
        print(f"Preview: {response.output_text[:100]}")
