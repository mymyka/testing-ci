"""
System Monitoring Dashboard — CPU, memory, network, disk metrics via Prometheus/node_exporter.
Designed for Linux hosts; works with Grafana Cloud's hosted Prometheus.
"""

import json
from grafana_foundation_sdk.builders.dashboard import Dashboard, Row, QueryVariable
from grafana_foundation_sdk.builders.prometheus import Dataquery as PrometheusQuery
from grafana_foundation_sdk.builders.timeseries import Panel as Timeseries
from grafana_foundation_sdk.builders.stat import Panel as Stat
from grafana_foundation_sdk.builders.gauge import Panel as Gauge
from grafana_foundation_sdk.cog.encoder import JSONEncoder
from grafana_foundation_sdk.models.common import TimeZoneBrowser
from grafana_foundation_sdk.models import dashboard as models


def build() -> dict:
    dashboard = (
        Dashboard("System Monitoring")
        .uid("system-monitoring")
        .tags(["linux", "node-exporter", "generated"])
        .description("CPU, memory, disk, and network metrics from node_exporter")
        .refresh("30s")
        .time("now-1h", "now")
        .timezone(TimeZoneBrowser)
        .editable()

        # Variable: job
        .with_variable(
            QueryVariable("job")
            .label("Job")
            .datasource(models.DataSourceRef(type_val="prometheus", uid="${datasource}"))
            .query("label_values(up, job)")
            .refresh(models.VariableRefresh(2))
            .include_all(True)
            .multi(True)
        )

        # ── Overview stats ───────────────────────────────────────────────────────
        .with_row(Row("Overview"))

        .with_panel(
            Stat()
            .title("CPU Usage")
            .description("Average CPU utilisation across all cores")
            .unit("percent")
            .span(6)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle",job=~"$job"}[5m])) * 100)')
                .legend_format("{{ instance }}")
                .instant()
            )
        )

        .with_panel(
            Stat()
            .title("Memory Usage")
            .description("Used RAM as a percentage of total")
            .unit("percent")
            .span(6)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('100 * (1 - (node_memory_MemAvailable_bytes{job=~"$job"} / node_memory_MemTotal_bytes{job=~"$job"}))')
                .legend_format("{{ instance }}")
                .instant()
            )
        )

        .with_panel(
            Stat()
            .title("Disk Usage")
            .description("Root filesystem usage")
            .unit("percent")
            .span(6)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('100 - ((node_filesystem_avail_bytes{job=~"$job",mountpoint="/",fstype!="rootfs"} / node_filesystem_size_bytes{job=~"$job",mountpoint="/",fstype!="rootfs"}) * 100)')
                .legend_format("{{ instance }}")
                .instant()
            )
        )

        .with_panel(
            Stat()
            .title("System Uptime")
            .unit("s")
            .span(6)
            .height(4)
            .with_target(
                PrometheusQuery()
                .expr('time() - node_boot_time_seconds{job=~"$job"}')
                .legend_format("{{ instance }}")
                .instant()
            )
        )

        # ── CPU ──────────────────────────────────────────────────────────────────
        .with_row(Row("CPU"))

        .with_panel(
            Timeseries()
            .title("CPU Usage %")
            .unit("percent")
            .min(0)
            .max(100)
            .span(12)
            .height(8)
            .fill_opacity(10)
            .with_target(
                PrometheusQuery()
                .expr('100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle",job=~"$job"}[5m])) * 100)')
                .legend_format("{{ instance }}")
            )
        )

        .with_panel(
            Timeseries()
            .title("CPU by Mode")
            .unit("percent")
            .min(0)
            .span(12)
            .height(8)
            .fill_opacity(10)
            .with_target(
                PrometheusQuery()
                .expr('avg by (mode) (rate(node_cpu_seconds_total{job=~"$job"}[5m])) * 100')
                .legend_format("{{ mode }}")
            )
        )

        # ── Memory ───────────────────────────────────────────────────────────────
        .with_row(Row("Memory"))

        .with_panel(
            Timeseries()
            .title("Memory Usage")
            .unit("bytes")
            .min(0)
            .span(12)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('node_memory_MemTotal_bytes{job=~"$job"} - node_memory_MemAvailable_bytes{job=~"$job"}')
                .legend_format("Used — {{ instance }}")
            )
            .with_target(
                PrometheusQuery()
                .expr('node_memory_MemAvailable_bytes{job=~"$job"}')
                .legend_format("Available — {{ instance }}")
            )
        )

        # ── Network ──────────────────────────────────────────────────────────────
        .with_row(Row("Network"))

        .with_panel(
            Timeseries()
            .title("Network Received")
            .unit("Bps")
            .min(0)
            .span(6)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('rate(node_network_receive_bytes_total{job=~"$job",device!="lo"}[5m])')
                .legend_format("{{ instance }} — {{ device }}")
            )
        )

        .with_panel(
            Timeseries()
            .title("Network Transmitted")
            .unit("Bps")
            .min(0)
            .span(6)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('rate(node_network_transmit_bytes_total{job=~"$job",device!="lo"}[5m])')
                .legend_format("{{ instance }} — {{ device }}")
            )
        )

        # ── Disk ─────────────────────────────────────────────────────────────────
        .with_row(Row("Disk I/O"))

        .with_panel(
            Timeseries()
            .title("Disk Read Throughput")
            .unit("Bps")
            .min(0)
            .span(6)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('rate(node_disk_read_bytes_total{job=~"$job"}[5m])')
                .legend_format("{{ instance }} — {{ device }}")
            )
        )

        .with_panel(
            Timeseries()
            .title("Disk Write Throughput")
            .unit("Bps")
            .min(0)
            .span(6)
            .height(8)
            .with_target(
                PrometheusQuery()
                .expr('rate(node_disk_written_bytes_total{job=~"$job"}[5m])')
                .legend_format("{{ instance }} — {{ device }}")
            )
        )
    ).build()

    return json.loads(JSONEncoder().encode(dashboard))


if __name__ == "__main__":
    out = "grafana/system_monitoring.json"
    with open(out, "w") as f:
        json.dump(build(), f, indent=2)
    print(f"Written: {out}")
