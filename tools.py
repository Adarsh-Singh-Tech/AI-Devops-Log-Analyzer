import os
from dotenv import load_dotenv
from crewai_tools import EXASearchTool
from crewai.tools import tool

from log_analyzer import parse_logs, generate_summary

load_dotenv()

@tool("Log Reader Tool")
def log_reader_tool(file_path: str) -> str:
    """Reads log file and returns summary + raw logs"""

    if not os.path.exists(file_path):
        return "File not found"

    with open(file_path, "r") as f:
        raw_logs = f.read()

    parsed = parse_logs(raw_logs)
    summary = generate_summary(parsed)

    return f"{summary}\n\nRAW LOGS:\n{raw_logs[:3000]}"


os.environ["EXA_API_KEY"] = os.getenv("EXA_API_KEY")
exa_search_tool = EXASearchTool()