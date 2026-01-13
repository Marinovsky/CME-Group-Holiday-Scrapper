from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

client = OpenAI()

class DateWithTime(BaseModel):
    date: str = Field(description="Dates must be M/D/YYYY (no leading zeros)")
    hour: str = Field(description="Times must be HH:MM:SS (24h)")

class HolidayCalendarEntry(BaseModel):
    holidays: List[str] = Field(description="Full holidays, this is, the market does not open again before closed on that day")
    bankHolidays: List[str] = Field(description="Bank Holidays, this is, market reopens again before closed on that day")
    earlyCloses: List[DateWithTime] = Field(description="Early market closes, this is, the market closes before the regular hour")
    reopens: List[DateWithTime] = Field(description="Reopens, this is, the market opens again before closed on that holiday, usually at night and for next day trading")


class HolidayCalendar(BaseModel):
    grains: HolidayCalendarEntry = Field(description="CME Group asset class 'Grains'")

prompt2 = """
You are a data extraction agent.

TASK:
Search the official CME Group website for the CME Group Holiday Calendar for the year 2026 and
extract ALL available 2026 information related to holiday schedule for CME group asset class
'Grains'

RULES:
- Use only CME Group official domains.
- If a value is not available, omit it.
- Do NOT invent missing data.
"""

second_response = client.responses.parse(
    model = "gpt-5.2",
    reasoning = {"effort": "medium"},
    tools=[{"type": "web_search"}],
    input = [{"role": "user", "content": prompt2}],
    text_format=HolidayCalendar
)

print(second_response.output_text)
print("==========================================")