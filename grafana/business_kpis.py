"""
Business KPIs Dashboard — revenue, signups, active users, and conversion funnel.
Uses TestData datasource so it works out-of-the-box in any Grafana instance
(no external data source required). Swap `type_val="testdata"` for your real source.
"""

import json
from grafana_foundation_sdk.builders.dashboard import Dashboard, Row
from grafana_foundation_sdk.builders.testdata import Dataquery as TestDataQuery
from grafana_foundation_sdk.builders.stat import Panel as Stat
from grafana_foundation_sdk.builders.timeseries import Panel as Timeseries
from grafana_foundation_sdk.builders.bargauge import Panel as BarGauge
from grafana_foundation_sdk.builders.gauge import Panel as Gauge
from grafana_foundation_sdk.builders.text import Panel as Text
from grafana_foundation_sdk.cog.encoder import JSONEncoder
from grafana_foundation_sdk.models.common import TimeZoneBrowser
from grafana_foundation_sdk.models import dashboard as models
from grafana_foundation_sdk.models import testdata as testdata_models


TESTDATA_DS = models.DataSourceRef(type_val="testdata", uid="grafana-testdata-datasource")


def random_walk(alias: str) -> TestDataQuery:
    return (
        TestDataQuery()
        .scenario_id(testdata_models.TestDataQueryType.RANDOM_WALK)
        .alias(alias)
        .datasource(TESTDATA_DS)
    )


def csv_metric_values(values: str, alias: str) -> TestDataQuery:
    return (
        TestDataQuery()
        .scenario_id(testdata_models.TestDataQueryType.CSV_METRIC_VALUES)
        .csv_content(values)
        .alias(alias)
        .datasource(TESTDATA_DS)
    )


def build() -> dict:
    dashboard = (
        Dashboard("Business KPIs")
        .uid("business-kpis")
        .tags(["business", "kpi", "generated"])
        .description("Revenue, signups, active users, and conversion metrics (TestData — no external source needed)")
        .refresh("5m")
        .time("now-7d", "now")
        .timezone(TimeZoneBrowser)
        .editable()

        # ── Header text ───────────────────────────────────────────────────────────
        .with_panel(
            Text()
            .title("")
            .content("## Business KPI Dashboard\nReal-time snapshot of key business metrics. Data refreshes every 5 minutes.")
            .transparent(True)
            .span(24)
            .height(3)
        )

        # ── Today's headline stats ────────────────────────────────────────────────
        .with_row(Row("Today at a Glance"))

        .with_panel(
            Stat()
            .title("Daily Revenue")
            .unit("currencyUSD")
            .span(6)
            .height(4)
            .with_target(csv_metric_values("42500", "Revenue"))
        )

        .with_panel(
            Stat()
            .title("New Signups")
            .unit("short")
            .span(6)
            .height(4)
            .with_target(csv_metric_values("312", "Signups"))
        )

        .with_panel(
            Stat()
            .title("Active Users (24h)")
            .unit("short")
            .span(6)
            .height(4)
            .with_target(csv_metric_values("8741", "Active Users"))
        )

        .with_panel(
            Stat()
            .title("Conversion Rate")
            .unit("percent")
            .span(6)
            .height(4)
            .with_target(csv_metric_values("3.8", "Conversion"))
        )

        # ── Trends ────────────────────────────────────────────────────────────────
        .with_row(Row("Trends"))

        .with_panel(
            Timeseries()
            .title("Revenue Over Time")
            .unit("currencyUSD")
            .min(0)
            .fill_opacity(15)
            .span(12)
            .height(8)
            .with_target(random_walk("Revenue"))
        )

        .with_panel(
            Timeseries()
            .title("Daily Active Users")
            .unit("short")
            .min(0)
            .fill_opacity(15)
            .span(12)
            .height(8)
            .with_target(random_walk("DAU"))
        )

        .with_panel(
            Timeseries()
            .title("Signups vs Churn")
            .unit("short")
            .min(0)
            .span(12)
            .height(8)
            .with_target(random_walk("Signups"))
            .with_target(random_walk("Churn"))
        )

        # ── Funnel / distribution ─────────────────────────────────────────────────
        .with_row(Row("Funnel & Distribution"))

        .with_panel(
            BarGauge()
            .title("Conversion Funnel")
            .unit("short")
            .min(0)
            .span(12)
            .height(8)
            .with_target(
                TestDataQuery()
                .scenario_id(testdata_models.TestDataQueryType.CSV_METRIC_VALUES)
                .csv_content("10000,6200,1800,680,312")
                .alias("Funnel")
                .datasource(TESTDATA_DS)
            )
        )

        .with_panel(
            Gauge()
            .title("MRR Goal Progress")
            .description("Monthly Recurring Revenue target: $500k")
            .unit("currencyUSD")
            .min(0)
            .max(500000)
            .span(6)
            .height(8)
            .with_target(csv_metric_values("382000", "MRR"))
        )

        .with_panel(
            Gauge()
            .title("NPS Score")
            .description("Net Promoter Score target: 60+")
            .unit("short")
            .min(-100)
            .max(100)
            .span(6)
            .height(8)
            .with_target(csv_metric_values("54", "NPS"))
        )
    ).build()

    return json.loads(JSONEncoder().encode(dashboard))


if __name__ == "__main__":
    out = "grafana/business_kpis.json"
    with open(out, "w") as f:
        json.dump(build(), f, indent=2)
    print(f"Written: {out}")
