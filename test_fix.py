#!/usr/bin/env python3
"""Test with different max_output_tokens values."""

from src.config import Config
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)

for max_tokens in [20, 50, 100, 200]:
    print(f"\n=== Testing with max_output_tokens={max_tokens} ===")

    response = client.responses.create(
        model=Config.OPENAI_MODEL,
        input='What is 2+2?',
        max_output_tokens=max_tokens
    )

    print(f"Status: {response.status}")
    print(f"output_text length: {len(response.output_text)}")
    print(f"output_text: '{response.output_text}'")
    print(f"output_tokens used: {response.usage.output_tokens}")
    print(f"reasoning_tokens used: {response.usage.output_tokens_details.reasoning_tokens}")
