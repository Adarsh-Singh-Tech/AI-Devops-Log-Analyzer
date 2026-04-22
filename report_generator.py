import os
import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document


# =========================
#  Severity Detection
# =========================
def detect_severity(result: str):
    text = str(result).lower()

    if "critical" in text:
        return ("2 - Critical", "High priority; fix immediately")
    elif "error" in text:
        return ("3 - Error", "Requires investigation")
    elif "warning" in text:
        return ("4 - Warning", "Monitor system")
    else:
        return ("6 - Informational", "No immediate action required")


# =========================
#  Confidence Score
# =========================
def calculate_confidence(result: str):
    text = str(result).lower()

    if "critical" in text or "error" in text:
        return 0.85
    elif "warning" in text:
        return 0.7
    return 0.6


# =========================
#  Convert to PDF
# =========================
def convert_to_pdf(md_content: str, filename: str):
    pdf_file = filename.replace(".md", ".pdf")

    doc = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()

    elements = []
    for line in md_content.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))

    doc.build(elements)
    return pdf_file


# =========================
#  Convert to DOCX
# =========================
def convert_to_docx(md_content: str, filename: str):
    docx_file = filename.replace(".md", ".docx")

    doc = Document()

    for line in md_content.split("\n"):
        doc.add_paragraph(line)

    doc.save(docx_file)
    return docx_file


# =========================
#  Ask user for export
# =========================
def ask_for_export(md_content: str, filename: str):
    choice = input("\n Do you want this report in PDF/DOCX? (Y/N): ").strip().lower()

    if choice == "y":
        format_choice = input("Choose format (pdf/docx): ").strip().lower()

        if format_choice == "pdf":
            pdf_path = convert_to_pdf(md_content, filename)
            print(f" PDF generated: {pdf_path}")

        elif format_choice == "docx":
            docx_path = convert_to_docx(md_content, filename)
            print(f" DOCX generated: {docx_path}")

        else:
            print(" Invalid format selected")

    else:
        print(" Skipping export")


# =========================
#  Generate Report
# =========================
def generate_report(result: str, log_path: str):
    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/devops_report_{timestamp}.md"

    severity, action = detect_severity(result)
    confidence = calculate_confidence(result)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("#  DevOps AI Analysis Report\n\n")

        f.write("##  Input Log File\n")
        f.write(f"`{log_path}`\n\n")

        # Severity
        f.write("##  Severity Assessment\n")
        f.write(f"**Level:** {severity}\n\n")
        f.write(f"**Action Required:** {action}\n\n")

        # Analysis
        f.write("##  Analysis Output\n\n")
        f.write(str(result))

        # Step-by-step solution
        f.write("\n\n---\n")
        f.write("##  Step-by-Step Solution\n\n")
        f.write(str(result))

        # Monitoring
        f.write("\n\n---\n")
        f.write("##  Monitoring & Prevention\n\n")
        f.write("- Set alerts for recurring issues\n")
        f.write("- Monitor logs continuously\n")
        f.write("- Add retry mechanisms\n")
        f.write("- Track system metrics\n")

        # Call to action
        f.write("\n\n---\n")
        f.write("## ⚡ Recommended Next Actions\n\n")
        f.write("1. Fix critical issues immediately\n")
        f.write("2. Validate system\n")
        f.write("3. Deploy monitoring\n")
        f.write("4. Document incident\n")

        # Confidence
        f.write("\n\n---\n")
        f.write(f"###  Confidence Score: {confidence}\n")

        # Severity Guide
        f.write("\n\n---\n")
        f.write("## 📘 Severity Guide\n\n")
        f.write("| Level | Name | Description | Action |\n")
        f.write("|------|------|------------|--------|\n")
        f.write("| 0 | Emergency | System unusable | Immediate response |\n")
        f.write("| 1 | Alert | Immediate action needed | Immediate fix |\n")
        f.write("| 2 | Critical | Major failure | High priority |\n")
        f.write("| 3 | Error | Runtime issue | Investigate |\n")
        f.write("| 4 | Warning | Non-critical issue | Monitor |\n")
        f.write("| 5 | Notice | Important event | Track |\n")
        f.write("| 6 | Informational | Routine logs | None |\n")
        f.write("| 7 | Debug | Debug info | Dev only |\n")

        f.write("\n---\n")
        f.write(f"_Generated at {timestamp}_\n")

    # return both path + content
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    return filename, content
