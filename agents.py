import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.llm import LLM

from tools import log_reader_tool, exa_search_tool, tavily_search_tool

load_dotenv()

#  OpenRouter LLM config
llm = LLM(
    model="openai/gpt-4o-mini",  # OpenRouter supported model
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# =========================
# Log Analyzer
# =========================
log_analyzer = Agent(
    role="Strict DevOps Log Analyzer",
    goal="Analyze logs strictly based on evidence",
    backstory="Expert in log analysis. No assumptions allowed.",
    llm=llm,
    tools=[log_reader_tool],
    verbose=True,
    max_iter=2,
)

# =========================
#  Investigator
# =========================
search_provider = os.getenv("SEARCH_PROVIDER", "exa").lower()
if search_provider == "tavily":
    _search_tools = [tavily_search_tool]
elif search_provider == "both":
    _search_tools = [exa_search_tool, tavily_search_tool]
else:
    _search_tools = [exa_search_tool]
_search_tools = [t for t in _search_tools if t is not None]

issue_investigator = Agent(
    role="DevOps Issue Investigator",
    goal="Find real solutions from trusted sources",
    backstory="Expert in troubleshooting using docs and forums.",
    llm=llm,
    tools=_search_tools,
    verbose=True,
)

# =========================
#  Solution Specialist
# =========================
solution_specialist = Agent(
    role="DevOps Solution Specialist",
    goal="Provide actionable solutions",
    backstory="Expert in production-grade fixes.",
    llm=llm,
    verbose=True,
)
