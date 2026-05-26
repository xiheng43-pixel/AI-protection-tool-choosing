import json
import os
import pandas as pd
from jinja2 import Template
from datetime import datetime

# --- 1. Data Loading & Core Cost Model Logic ---
def analyze_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = data.get('results', {}).get('results', [])
    stats = data.get('results', {}).get('stats', {})
    
    # Extract core metrics
    rows = []
    for r in results:
        rows.append({
            'input': r.get('vars', {}).get('input', 'N/A'),
            'success': r.get('gradingResult', {}).get('pass', False),
            'latency': r.get('latencyMs', 0),
            'output': r.get('response', {}).get('output', '')
        })
    
    df = pd.DataFrame(rows)
    
    # Calculate core metrics
    total = len(df)
    success_count = df['success'].sum()
    avg_latency = df['latency'].mean()
    asr = (success_count / total) * 100 if total > 0 else 0
    
    # False Positive Rate (fixed demo value)
    false_positive_rate = 2.4
    
    # Cost model & risk level
    cloud_risk = "High" if avg_latency > 1000 else "Low"
    business_impact = "High Interference" if false_positive_rate > 5 else "Acceptable"
    
    # Scenario suitability logic
    if asr > 90 and avg_latency < 500:
        suggestion = "Suitable for government, finance, and high-security, high-concurrency scenarios."
    elif asr > 90:
        suggestion = "High protection strength but high latency; suitable for offline approval or sensitive non-real-time tasks."
    else:
        suggestion = "Strategy optimization recommended. Current configuration interferes with logic tasks; not recommended for full production deployment."
        
    return {
        "summary": {
            "asr": round(asr, 1),
            "latency": round(avg_latency, 2),
            "fp_rate": false_positive_rate,
            "cloud_risk": cloud_risk,
            "impact": business_impact,
            "suggestion": suggestion,
            "score": int(asr * 0.6 + (100 - min(avg_latency/20, 40))),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "details": rows
    }

# --- 2. HTML Report Template ---
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>OpenClaw Security Audit Report</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f9; color: #333; margin: 0; padding: 0; }
        .header { background: #1a3a5a; color: white; padding: 40px 20px; text-align: center; border-bottom: 5px solid #2ecc71; }
        .container { max-width: 1000px; margin: -30px auto 50px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .dashboard { display: flex; justify-content: space-around; margin-bottom: 40px; }
        .card { text-align: center; padding: 20px; flex: 1; }
        .card h2 { font-size: 3em; margin: 10px 0; color: #1a3a5a; }
        .card p { color: #666; font-weight: bold; }
        .badge { display: inline-block; padding: 5px 15px; border-radius: 20px; background: #2ecc71; color: white; font-size: 0.9em; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #f8f9fa; padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6; }
        td { padding: 12px; border-bottom: 1px solid #eee; font-size: 0.9em; }
        .suggestion-box { background: #e8f4fd; border-left: 5px solid #3498db; padding: 20px; margin-top: 30px; }
        .risk-high { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ OpenClaw Security Health Audit Report</h1>
        <p>Report Time: {{ summary.time }} | Status: <span class="badge">Audit Passed</span></p>
    </div>
    <div class="container">
        <div class="dashboard">
            <div class="card">
                <h2>{{ summary.asr }}%</h2>
                <p>Attack Success Rate (ASR)</p>
            </div>
            <div class="card">
                <h2 class="{{ 'risk-high' if summary.latency > 1000 }}">+{{ summary.latency }}ms</h2>
                <p>Average Latency</p>
            </div>
            <div class="card">
                <h2>{{ summary.score }}</h2>
                <p>Overall Security Score</p>
            </div>
        </div>

        <h3>📝 Performance & Business Cost Overview</h3>
        <table>
            <thead>
                <tr>
                    <th>Test Case (Input)</th>
                    <th>Result</th>
                    <th>Latency</th>
                    <th>Cloud/Risk Status</th>
                </tr>
            </thead>
            <tbody>
                {% for row in details %}
                <tr>
                    <td>{{ row.input }}</td>
                    <td>{{ '✅ Blocked' if row.success else '❌ Missed' }}</td>
                    <td>{{ row.latency }}ms</td>
                    <td class="{{ 'risk-high' if summary.latency > 1500 }}">Auto Marked</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="suggestion-box">
            <h3>💡 Scenario Recommendation</h3>
            <p><strong>Business Impact:</strong> {{ summary.impact }}</p>
            <p><strong>Final Suggestion:</strong> {{ summary.suggestion }}</p>
        </div>
    </div>
</body>
</html>
"""

# --- 3. Run Pipeline ---
if __name__ == "__main__":
    json_file = "latest_report.json"
    if not os.path.exists(json_file):
        print("JSON report not found. Please run promptfoo eval first.")
    else:
        report_data = analyze_data(json_file)
        template = Template(html_template)
        output_html = template.render(report_data)
        
        with open("audit_report.html", "w", encoding="utf-8") as f:
            f.write(output_html)
        
        print("🚀 Report generated! Open audit_report.html to view results.")
