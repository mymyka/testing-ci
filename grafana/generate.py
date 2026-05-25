"""Run this script to regenerate all dashboard JSON files."""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from grafana import system_monitoring, web_app_overview, business_kpis

HERE = pathlib.Path(__file__).parent

dashboards = {
    "system_monitoring.json": system_monitoring.build,
    "web_app_overview.json": web_app_overview.build,
    "business_kpis.json": business_kpis.build,
}

for filename, builder in dashboards.items():
    path = HERE / filename
    data = builder()
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"  wrote {path.relative_to(HERE.parent)}")

print("Done.")
