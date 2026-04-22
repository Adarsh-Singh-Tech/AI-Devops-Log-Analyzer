def parse_logs(raw_logs: str):
    lines = raw_logs.split("\n")

    parsed = {
        "total": 0,
        "errors": [],
        "warnings": [],
        "critical": [],
    }

    for line in lines:
        if not line.strip():
            continue

        parsed["total"] += 1
        upper = line.upper()

        if "CRITICAL" in upper:
            parsed["critical"].append(line)
        elif "ERROR" in upper:
            parsed["errors"].append(line)
        elif "WARNING" in upper:
            parsed["warnings"].append(line)

    return parsed


def generate_summary(parsed_logs):
    return f"""
Log Summary:
- Total Logs: {parsed_logs['total']}
- Errors: {len(parsed_logs['errors'])}
- Warnings: {len(parsed_logs['warnings'])}
- Critical: {len(parsed_logs['critical'])}
"""