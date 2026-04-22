from fastapi import FastAPI, UploadFile, File
import tempfile
from crewai import Crew, Process
from tasks import analyze_logs_task, investigate_issue_task, provide_solution_task
from agents import log_analyzer, issue_investigator, solution_specialist

app = FastAPI()

crew = Crew(
    agents=[log_analyzer, issue_investigator, solution_specialist],
    tasks=[analyze_logs_task, investigate_issue_task, provide_solution_task],
    process=Process.sequential,
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(await file.read())
        path = temp.name

    result = crew.kickoff(inputs={"log_file_path": path})

    return {"result": str(result)}