"""Lina's AI provider.

The API key is read from the OPENAI_API_KEY environment variable.
Never put the key directly in this file or commit it to GitHub.
"""

import json
import os
import urllib.error
import urllib.request


class OpenAIProvider:
    """Small dependency-free client for Lina's text generation."""

    def __init__(self, model=None):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-5-mini")

    def reply(self, user_message, system_prompt=None):
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        instructions = system_prompt or (
            "Sen Lina'sın. Canlı yayında izleyicilerle konuşan samimi, "
            "eğlenceli ve doğal bir yapay zeka karakterisin. Kısa, konuşma "
            "diline yakın cevaplar ver. Gereksiz açıklama yapma."
        )

        payload = {
            "model": self.model,
            "instructions": instructions,
            "input": user_message,
        }

        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"OpenAI API error ({exc.code}): {body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Network error while contacting OpenAI: {exc}"
            ) from exc

        text = data.get("output_text")

        if text:
            return text.strip()

        parts = []

        for item in data.get("output", []):
            for content in item.get("content", []):
                if (
                    content.get("type") == "output_text"
                    and content.get("text")
                ):
                    parts.append(content["text"])

        if parts:
            return "\n".join(parts).strip()

        raise RuntimeError("OpenAI returned no text output")
