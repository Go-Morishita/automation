import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_schema():
    schema_path = Path(__file__).with_name("schema.json")
    with schema_path.open(encoding="utf-8") as f:
        return json.load(f)

def generate_structured_json(prompt, model="gpt-4o-mini"):
    schema_config = load_schema()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Return only JSON following the provided schema.",
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema_config["name"],
                "schema": schema_config["schema"],
                "strict": True,
            },
        },
    )
    
    content = response.choices[0].message.content or "{}"

    return json.loads(content)