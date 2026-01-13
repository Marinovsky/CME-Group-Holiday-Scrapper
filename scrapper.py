from openai import OpenAI
from pydantic import BaseModel, RootModel
from typing import Dict, List

client = OpenAI()

class DateWithTime(BaseModel):
    date: str
    hour: str

class HolidayCalendarEntry(BaseModel):
    holidays: List[str]
    bankHolidays: List[str]
    earlyCloses: List[DateWithTime]
    reopens: List[DateWithTime]


class HolidayCalendar(BaseModel):
    grains: HolidayCalendarEntry

prompt2 = """
You are a data extraction agent.

TASK:
Search the official CME Group website for the CME Group Holiday Calendar for the year 2026 and
extract ALL available 2026 information related to:
- Full holidays (this is, the market does not open again before closed on that day)
- Early market closes
- Reopens (this is, the market opens again before closed on that holiday, usually at night and for next day trading)
- Bank holidays (this is, market re opens again before closed)
- Asset classes: Grains

RULES:
- Use only CME Group official domains.
- Dates must be M/D/YYYY (no leading zeros).
- Times must be HH:MM:SS (24h)
- If a value is not available, omit it.
- Do NOT invent missing data.
- Return JSON only.
"""

second_response = client.responses.parse(
    model = "gpt-5.2",
    tools=[{"type": "web_search"}],
    input = [{"role": "user", "content": prompt2}],
    text_format=HolidayCalendar
)

print(second_response.output_text)
print("==========================================")