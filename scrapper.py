import json
from openai import OpenAI

client = OpenAI()

prompt = """
You are a web discovery agent.

TASK:
Search the official CME Group website for the CME Group Holiday Calendar for the year 2026.

RETURN:
- A list of official CME Group URLs that contain holiday, early close, or late open information for 2026.
- If the 2026 calendar is not published, explicitly say: "CME 2026 calendar not yet published".

FORMAT:
Return JSON only in the following format:

{
  "published": true | false,
  "urls": ["https://...", "..."]
}

RULES:
- Use only CME Group official domains.
- Do not guess or infer dates.
- Do not include explanations.
"""

history = [
  {
    "role": "user",
    "content": prompt
  }
]

response = client.responses.create(
    model="gpt-5-mini",
    tools=[{"type": "web_search"}],
    input=history
)

print(response.output_text)
print("======================================")

prompt2 = """
You are a data extraction agent.

TASK:
Using the official CME Group URLs provided, extract ALL available 2026 information related to:
- Full holidays
- Early market closes
- Late market opens (this is, the market opens again before closed)
- Bank holidays
- Asset classes: Grains and Livestock

FORMAT:
Return JSON only, with this flexible structure:

{
  "grains": {
    "earlyCloses": [{"date": "M/D/YYYY", "time": "HH:MM:SS"}],
    "lateOpens": [{"date": "M/D/YYYY", "time": "HH:MM:SS"}],
    "holidays": ["M/D/YYYY"],
  },
  "...": {}
}

RULES:
- Dates must be M/D/YYYY (no leading zeros).
- Times must be HH:MM:SS (24h).
- If a value is not available, omit it.
- Do NOT invent missing data.
- Return JSON only.

"""

second_response = client.responses.create(
    model = "gpt-5",
    previous_response_id=response.id,
    tools=[{"type": "web_search"}],
    input = [{"role": "user", "content": prompt2}]
)

print(second_response.output_text)
print("==========================================")

prompt3 = """
You are a data validation agent.

TASK:
Validate the provided CME Group 2026 JSON file.

CHECKS:
- All dates are in year 2026
- No duplicate dates inside the same category
- No holiday is in early Closes or late Opens
- JSON is syntactically valid

OUTPUT FORMAT:
Return JSON only:

{
  "valid": true | false,
  "errors": []
}

"""

third_response = client.responses.create(
    model = "gpt-5-mini",
    previous_response_id=second_response.id,
    tools=[{"type": "web_search"}],
    input = [{"role": "user", "content": prompt3}]
)

print(third_response.output_text)
print("==========================================")