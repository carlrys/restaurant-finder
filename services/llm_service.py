import os
import re
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

async def parse_message_to_json(message: str) -> dict:
    system_prompt = (
        "You are a strict JSON generator. I need you to convert the user's natural-language restaurant search"
        "into a JSON object using this schema:\n"
        '{"action": "restaurant_search, "paramters": {'
        '"query": \"example\",'
        '"near": \"example\",'
        '"price": \"1\",'
        '"open_now": true }}\n'
        "Return ONLY the JSON object, with no additional explanatory text."
    )

    payload = {
        "model": GROQ_MODEL,
        "messages": [{
            "role": "user",
            "content": f"{system_prompt}\n User prompt: {message}"
        }],
        "temperature": 0
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    async with httpx.AsyncClient(timeout = 30.0) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    if content.startswith("```"):
        content = re.sub(r"^```(json)?|```$", "", content, flags = re.MULTILINE).strip()
    try:
        parsed = json.loads(content)
    except Exception as e:
        raise RuntimeError(f"LLM returned invalid JSON")

    return parsed
