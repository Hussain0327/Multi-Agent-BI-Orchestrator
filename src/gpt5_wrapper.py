"""GPT-5 Responses API wrapper for unified interface."""
import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
from src.config import Config


class GPT5Wrapper:
    """Wrapper for GPT-5 Responses API with fallback to Chat Completions."""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.is_gpt5 = Config.is_gpt5()

    def generate(
        self,
        messages: List[Dict[str, str]] = None,
        input_text: str = None,
        instructions: str = None,
        reasoning_effort: str = None,
        text_verbosity: str = None,
        max_output_tokens: int = None,
        tools: List[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a response using GPT-5 Responses API or Chat Completions.

        Args:
            messages: List of message dicts (for Chat Completions compatibility)
            input_text: Direct input string (for Responses API)
            instructions: System instructions (Responses API equivalent of system message)
            reasoning_effort: GPT-5 reasoning effort (minimal, low, medium, high)
            text_verbosity: GPT-5 output verbosity (low, medium, high)
            max_output_tokens: Maximum tokens to generate
            tools: List of tools for function calling

        Returns:
            Generated text response
        """
        try:
            if self.is_gpt5:
                return self._generate_gpt5(
                    messages=messages,
                    input_text=input_text,
                    instructions=instructions,
                    reasoning_effort=reasoning_effort or Config.REASONING_EFFORT,
                    text_verbosity=text_verbosity or Config.TEXT_VERBOSITY,
                    max_output_tokens=max_output_tokens or Config.MAX_OUTPUT_TOKENS,
                    tools=tools,
                )
            else:
                return self._generate_chat_completions(
                    messages=messages,
                    max_tokens=max_output_tokens or Config.MAX_OUTPUT_TOKENS,
                    tools=tools,
                )
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _generate_gpt5(
        self,
        messages: List[Dict[str, str]] = None,
        input_text: str = None,
        instructions: str = None,
        reasoning_effort: str = "medium",
        text_verbosity: str = "medium",
        max_output_tokens: int = 2000,
        tools: List[Dict[str, Any]] = None,
    ) -> str:
        """Generate using GPT-5 Responses API."""
        # Convert messages to input if needed
        if input_text is None and messages:
            # Extract system message as instructions
            system_msgs = [m for m in messages if m.get("role") == "system"]
            if system_msgs and not instructions:
                instructions = system_msgs[0]["content"]

            # Convert remaining messages to input
            user_msgs = [m for m in messages if m.get("role") != "system"]
            if user_msgs:
                input_text = user_msgs if len(user_msgs) > 1 else user_msgs[0]["content"]
            else:
                input_text = ""

        # Build Responses API request
        request_params = {
            "model": self.model,
            "input": input_text,
            "reasoning": {"effort": reasoning_effort},
            "text": {"verbosity": text_verbosity},
            "max_output_tokens": max_output_tokens,
        }

        if instructions:
            request_params["instructions"] = instructions

        if tools:
            # Convert Chat Completions tool format to Responses API format
            request_params["tools"] = self._convert_tools_to_gpt5(tools)

        response = self.client.responses.create(**request_params)

        # Extract text from response
        return self._extract_text_from_response(response)

    def _generate_chat_completions(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2000,
        tools: List[Dict[str, Any]] = None,
    ) -> str:
        """Generate using Chat Completions API (fallback for GPT-4/3.5)."""
        request_params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }

        if tools:
            request_params["tools"] = tools

        response = self.client.chat.completions.create(**request_params)
        return response.choices[0].message.content

    def _convert_tools_to_gpt5(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert Chat Completions tool format to Responses API format.

        Chat Completions:
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "...",
                "parameters": {...}
            }
        }

        Responses API:
        {
            "type": "function",
            "name": "get_weather",
            "description": "...",
            "parameters": {...}
        }
        """
        converted_tools = []
        for tool in tools:
            if tool.get("type") == "function" and "function" in tool:
                # Flatten structure
                func = tool["function"]
                converted_tools.append({
                    "type": "function",
                    "name": func.get("name"),
                    "description": func.get("description"),
                    "parameters": func.get("parameters", {}),
                })
            else:
                # Already in correct format or different type
                converted_tools.append(tool)
        return converted_tools

    def _extract_text_from_response(self, response: Any) -> str:
        """Extract text from GPT-5 Responses API response."""
        # GPT-5 Responses API returns output as a list of items
        if hasattr(response, "output_text"):
            # Use convenience helper if available
            return response.output_text

        # Manual extraction from output array
        if hasattr(response, "output"):
            for item in response.output:
                if item.get("type") == "message":
                    # Extract text from message content
                    content = item.get("content", [])
                    for content_item in content:
                        if content_item.get("type") == "output_text":
                            return content_item.get("text", "")

        return "No text output found in response"
