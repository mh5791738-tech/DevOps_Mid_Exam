
from flask import Flask, request, jsonify
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import hmac

app = Flask(__name__)

REPORT_FILE = Path(__file__).parent / "test-report.json"
REPORT_TOKEN = os.environ.get("REPORT_RECEIVER_TOKEN")

@app.route("/report", methods=["POST"])
def receive_report():
    if not REPORT_TOKEN:
        return jsonify({"error": "Receiver token is not configured"}), 500

    supplied_token = request.headers.get("Authorization", "")
    expected_token = f"Bearer {REPORT_TOKEN}"

    if not hmac.compare_digest(supplied_token, expected_token):
        return jsonify({"error": "Unauthorized"}), 401

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    required_fields = [
        "repository", "branch", "commit_sha", "run_id",
        "timestamp", "tests", "total", "passed", "failed", "status"
    ]

    if not all(field in report for field in required_fields):
        return jsonify({"error": "Missing report fields"}), 400

    report["received_at"] = datetime.now(timezone.utc).isoformat()

    REPORT_FILE.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print("Test report received successfully!")

    return jsonify({
        "message": "Report saved successfully",
        "file": str(REPORT_FILE)
    }), 200


@app.route("/", methods=["GET"])
def home():
    return "DevOps Test Report Receiver is running!"


if __name__ == "__main__":
    if not REPORT_TOKEN:
        raise RuntimeError("Set REPORT_RECEIVER_TOKEN before starting receiver")

    app.run(host="0.0.0.0", port=5001)
