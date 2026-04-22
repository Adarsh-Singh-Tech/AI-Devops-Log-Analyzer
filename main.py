import os
import traceback
from crewai import Crew, Process

from tasks import (
    analyze_logs_task,
    investigate_issue_task,
    provide_solution_task,
)
from agents import (
    log_analyzer,
    issue_investigator,
    solution_specialist,
)
from progress_tracker import simulate_progress, estimate_time
from report_generator import generate_report, ask_for_export


# =========================
# 🔧 Crew Setup
# =========================
def create_crew():
    return Crew(
        agents=[log_analyzer, issue_investigator, solution_specialist],
        tasks=[
            analyze_logs_task,
            investigate_issue_task,
            provide_solution_task,
        ],
        process=Process.sequential,
        verbose=True,
    )


# =========================
# 🏃 Pipeline
# =========================
def run_pipeline(log_path: str):
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Log file not found: {log_path}")

    print(f"\n⏳ Estimated Time: {estimate_time(log_path)}")
    simulate_progress()

    crew = create_crew()

    print("\n🤖 Running AI analysis...\n")

    result = crew.kickoff(
        inputs={"log_file_path": log_path}
    )

    return result


# =========================
# 🚀 Main
# =========================
def main():
    print("🚀 DevOps AI Analyzer\n")

    try:
        log_path = input("📂 Enter log file path: ").strip()

        if not log_path:
            log_path = "logs/sample_logs.log"

        result = run_pipeline(log_path)

        print("\n📊 FINAL RESULT:\n")
        print(result)

        # ✅ Generate report
        report_path, report_content = generate_report(result, log_path)

        print(f"\n📁 Report generated: {report_path}")

        # ✅ Ask for export
        ask_for_export(report_content, report_path)

        print("\n🎉 Analysis completed!")

    except Exception as e:
        print("\n❌ ERROR OCCURRED\n")
        print(str(e))

        print("\n🔍 Debug Info:")
        traceback.print_exc()


if __name__ == "__main__":
    main()