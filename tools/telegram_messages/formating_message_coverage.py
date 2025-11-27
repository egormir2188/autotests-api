import json
import re
from typing import Dict, Any


def extract_coverage_data(html_file_path: str) -> Dict[str, Any]:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    script_pattern = r'<script id="state" type="application/json">(.*?)</script>'
    match = re.search(script_pattern, html_content, re.DOTALL)

    json_data = json.loads(match.group(1))
    services_coverage = json_data.get('servicesCoverage', {})

    service_key = next(iter(services_coverage.keys()))
    service_data = services_coverage[service_key]
    endpoints = service_data.get('endpoints', [])

    total_endpoints = len(endpoints)
    covered_endpoints = [e for e in endpoints if e.get('coverage') == 'COVERED']

    coverage_data = {
        'total_coverage': f"{service_data.get('totalCoverage', 0)}%",
        'covered': len(covered_endpoints),
        'total': total_endpoints
    }

    return coverage_data


def format_coverage_message(coverage_data):
    message = (
        f"📊 API Coverage Report:\n\n"
        f"🔹 Total Coverage: {coverage_data['total_coverage']}\n"
        f"🔹 Covered: {coverage_data['covered']}\n"
        f"🔹 Total Endpoints: {coverage_data['total']}\n\n"
    )

    return message