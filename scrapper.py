from openai import OpenAI
import asyncio
from agents import Agent, Runner, WebSearchTool, ModelSettings
from pydantic import BaseModel, Field
from typing import List
from openai.types.responses.web_search_tool import Filters
from openai.types.shared.reasoning import Reasoning

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
- It's for QuantConnect LEAN Engine
- Use only CME Group official domains.
- If a value is not available, omit it.
- Do NOT invent missing data."""


response = client.responses.parse(
    model = "gpt-5.2",
    reasoning = {"effort": "medium"},
    tools=[{"type": "web_search"}],
    input = [{"role": "user", "content": prompt2}],
    text_format=HolidayCalendar
)

print(response.output_text)
with open("client_response.json", "w") as f:
    f.write(str(response.output_text))
print("==========================================")

async def create_and_run_agent():  
  agent = Agent(
      name = "Scrappy",
      instructions = "You are data extraction agent. You extract CME Group Holiday calendar",
      model = "gpt-5.2",
      output_type = HolidayCalendar,
      tools = [
            WebSearchTool(
                filters=Filters(
                    allowed_domains=[
                        "cmegroup.com",
                        "crosstrade.io"
                    ],
                ),
                search_context_size="medium",
            )
        ],
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium"),
            response_include=["web_search_call.action.sources"]
        )
  )

  agent_response = await Runner.run(agent, "Extract CME Holiday Calendar for 2026 for the asset class Grains")
  print(agent_response.final_output)
  with open("agent_response.json", "w") as f:
    f.write(str(agent_response.final_output))

asyncio.run(create_and_run_agent())