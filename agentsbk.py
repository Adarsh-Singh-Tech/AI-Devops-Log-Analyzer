import os
from dotenv import load_dotenv
from crewai import Agent

from tools import log_reader_tool, exa_search_tool, tavily_search_tool

load_dotenv()

# ❌ REMOVE LLM CONFIG (no import of crewai.llm)

log_analyzer = Agent(
    role="Strict DevOps Log Analyzer",
    goal="Analyze logs strictly based on evidence",
    backstory="Expert in log analysis. No assumptions allowed.",
    tools=[log_reader_tool],
    verbose=True,
    max_iter=2,
)

search_provider = os.getenv("SEARCH_PROVIDER", "both").lower()
if search_provider == "tavily":
    _search_tools = [tavily_search_tool]
elif search_provider == "exa":
    _search_tools = [exa_search_tool]
else:
    _search_tools = [exa_search_tool, tavily_search_tool]

issue_investigator = Agent(
    role="DevOps Issue Investigator",
    goal="Find real solutions from trusted sources",
    backstory="Expert in troubleshooting using docs and forums.",
    tools=_search_tools,
    verbose=True,
)

solution_specialist = Agent(
    role="DevOps Solution Specialist",
    goal="Provide actionable solutions",
    backstory="Expert in production-grade fixes.",
    verbose=True,
)