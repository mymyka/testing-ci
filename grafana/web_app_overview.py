"""
Web Application Overview Dashboard — request rate, error rate, and latency (RED method).
Targets Prometheus metrics exposed by a typical HTTP service (e.g., FastAPI + prometheus_fastapi_instrumentator).
"""

import json
from grafana_foundation_sdk.builders.dashboard import Dashboard, Row, CustomVariable
from grafana_foundation_sdk.builders.prometheus import Dataquery as PrometheusQuery
from grafana_foundation_sdk.builders.timeseries import Panel as Timeseries
from grafana_foundation_sdk.builders.stat import Panel as Stat
from grafana_foundation_sdk.builders.gauge import Panel as Gauge
from grafana_foundation_sdk.cog.encoder import JSONEncoder
from grafana_foundation_sdk.models.common import TimeZoneBrowser
from grafana_foundation_sdk.models import dashboard as models


def build() -> dict:
    dashboard = (
        Dashboard("Web App Overview")
        .uid("web-app-overview")
        .tags(["web", "red-method", "generated"])
        .description("Rate, Error, Duration — the three RED signals for HTTP services")
        .refresh("15s")
        .time("now-1h", "now")
        .timezone(TimeZoneBrowser)
        .editable()

        # Variable: environment
        .with_variable(
            CustomVariable("env")
            .label("Environment")
            .values("production,staging,development")
        )

        # ── Headline numbers ──────────────────────────────────────────────────────
        .with_row(Row("Summary"))

        .with_panel(
            Stat()
            .title("Request Rate")
            .description("HTTP requests per second (all status codes)")
            .unit("reqps")
            .span(4)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('sum(rate(http_requests_total{env=~"$env"}[5m]))')
                .legend_format("req/s")
                .instant()
            )
        )

        .with_panel(
            Stat()
            .title("Error Rate")
            .description("Percentage of 5xx responses over the last 5 minutes")
            .unit("percent")
            .span(4)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('100 * sum(rate(http_requests_total{env=~"$env",status=~"5.."}[5m])) / sum(rate(http_requests_total{env=~"$env"}[5m]))')
                .legend_format("error %")
                .instant()
            )
        )

        .with_panel(
            Stat()
            .title("p99 Latency")
            .description("99th-percentile request duration")
            .unit("s")
            .span(4)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{env=~"$env"}[5m])))')
                .legend_format("p99")
                .instant()
            )
        )

        # ── Traffic ───────────────────────────────────────────────────────────────
        .with_row(Row("Traffic"))

        .with_panel(
            Timeseries()
            .title("Request Rate by Status")
            .unit("reqps")
            .min(0)
            .span(12)
            .height(8)
            .fill_opacity(10)
            .with_target(
                PrometheusQuery()
                .expr('sum by (status) (rate(http_requests_total{env=~"$env"}[5m]))')
                .legend_format("HTTP {{ status }}")
            )
        )

        # ── Errors ────────────────────────────────────────────────────────────────
        .with_row(Row("Errors"))

        .with_panel(
            Timeseries()
            .title("Error Rate %")
            .unit("percent")
            .min(0)
            .max(100)
            .span(12)
            .height(8)
            .fill_opacity(10)
            .with_target(
                PrometheusQuery()
                .expr('100 * sum by (route) (rate(http_requests_total{env=~"$env",status=~"5.."}[5m])) / sum by (route) (rate(http_requests_total{env=~"$env"}[5m]))')
                .legend_format("{{ route }}")
            )
        )

        # ── Latency ───────────────────────────────────────────────────────────────
        .with_row(Row("Latency"))

        .with_panel(
            Timeseries()
            .title("Request Duration Percentiles")
            .unit("s")
            .min(0)
            .span(12)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket{env=~"$env"}[5m])))')
                .legend_format("p50")
            )
            .with_target(
                PrometheusQuery()
                .expr('histogram_quantile(0.90, sum by (le) (rate(http_request_duration_seconds_bucket{env=~"$env"}[5m])))')
                .legend_format("p90")
            )
            .with_target(
                PrometheusQuery()
                .expr('histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{env=~"$env"}[5m])))')
                .legend_format("p99")
            )
        )

        .with_panel(
            Gauge()
            .title("p99 Latency SLO")
            .description("Target: requests under 500ms")
            .unit("s")
            .min(0)
            .max(1)
            .span(6)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{env=~"$env"}[5m])))')
                .legend_format("p99")
                .instant()
            )
        )

        .with_panel(
            Timeseries()
            .title("Latency by Route")
            .unit("s")
            .min(0)
            .span(6)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('histogram_quantile(0.95, sum by (le, route) (rate(http_request_duration_seconds_bucket{env=~"$env"}[5m])))')
                .legend_format("p95 — {{ route }}")
            )
        )
    ).build()

    return json.loads(JSONEncoder().encode(dashboard))


if __name__ == "__main__":
    out = "grafana/web_app_overview.json"
    with open(out, "w") as f:
        json.dump(build(), f, indent=2)
    print(f"Written: {out}")
