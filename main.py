"""
Grafana Panel health-check monitor.
Runs periodically via monitor_mrs_agent.
Checks Grafana connectivity and outputs status JSON.
"""

import json
import os
import sys
import urllib.request
import urllib.error


def report_progress(pct: int, msg: str = "") -> None:
    print(json.dumps({"_progress": pct, "_message": msg}, ensure_ascii=False), flush=True)


def main() -> None:
    # Read grafana_base_url from env (set by mywant via state.goal fields)
    # Fall back to env var, then default.
    base_url = (
        os.environ.get("MYWANT_STATE_GRAFANA_BASE_URL")
        or os.environ.get("GRAFANA_BASE_URL")
        or "http://localhost:3000"
    ).rstrip("/")

    report_progress(50, f"checking {base_url}")

    try:
        req = urllib.request.urlopen(f"{base_url}/api/health", timeout=5)
        body = json.loads(req.read().decode())
        db_ok = body.get("database") == "ok"
        status = "ok" if db_ok else f"degraded: {body}"
    except urllib.error.URLError as e:
        status = f"unreachable: {e.reason}"
    except Exception as e:
        status = f"error: {e}"

    report_progress(100, status)
    print(json.dumps({"status": status}, ensure_ascii=False))


if __name__ == "__main__":
    main()
