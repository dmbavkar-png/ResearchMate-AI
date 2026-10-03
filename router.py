import json
import requests


class ToolRouter:

    def __init__(
        self,
        model="qwen2.5:3b",
        ollama_url="http://localhost:11434/api/generate"
    ):
        self.model = model
        self.ollama_url = ollama_url

    def route(self, user_input):

        prompt = f"""
You are a routing system for a personal AI assistant.

Your ONLY job is to classify the user's request.

Available intents:

chat
email_list
email_search
email_read
email_draft
email_send

Return ONLY valid JSON.

Required format:

{{
    "intent": "intent_name",
    "parameter": ""
}}

Rules:

1. If user wants to see inbox or emails:
   intent = email_list

2. If user wants to search/find emails:
   intent = email_search
   parameter = search keyword

3. If user wants to open/read a numbered email:
   intent = email_read
   parameter = email number

4. If user wants to write/draft/prepare an email:
   intent = email_draft
   parameter = the original request

5. If user explicitly asks to send the current draft:
   intent = email_send

6. Everything else:
   intent = chat

Examples:

User: Show my inbox
{{
    "intent": "email_list",
    "parameter": ""
}}

User: Any emails about research?
{{
    "intent": "email_search",
    "parameter": "research"
}}

User: Open email 2
{{
    "intent": "email_read",
    "parameter": "2"
}}

User: Write an email to Dr. Sharma about our meeting
{{
    "intent": "email_draft",
    "parameter": "Write an email to Dr. Sharma about our meeting"
}}

User: Send this email
{{
    "intent": "email_send",
    "parameter": ""
}}

User: Explain machine learning
{{
    "intent": "chat",
    "parameter": ""
}}

User request:
{user_input}

JSON:
"""

        try:

            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )

            response.raise_for_status()

            result = response.json()

            raw_output = result["response"].strip()

            parsed = json.loads(raw_output)

            return parsed

        except Exception as e:

            print("Router error:", e)

            # Safe fallback
            return {
                "intent": "chat",
                "parameter": ""
            }