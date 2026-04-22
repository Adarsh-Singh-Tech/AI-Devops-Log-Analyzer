from crewai import Task
from agents import log_analyzer, issue_investigator, solution_specialist

analyze_logs_task = Task(
    description="""
Analyze logs at {log_file_path}
Provide summary, issues, and evidence.
""",
    expected_output="Structured log analysis with issues and evidence",
    agent=log_analyzer,
)

investigate_issue_task = Task(
    description="Investigate issues from logs",
    expected_output="Root causes and references",
    agent=issue_investigator,
    context=[analyze_logs_task],
)

provide_solution_task = Task(
    description="Provide step-by-step solution",
    expected_output="Actionable solution plan",
    agent=solution_specialist,
    context=[analyze_logs_task, investigate_issue_task],
)