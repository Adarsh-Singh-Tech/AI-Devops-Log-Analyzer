import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.llm import LLM

from tools import log_reader_tool, exa_search_tool

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
issue_investigator = Agent(
    role="DevOps Issue Investigator",
    goal="Find real solutions from trusted sources",
    backstory="Expert in troubleshooting using docs and forums.",
    llm=llm,
    tools=[exa_search_tool],
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
