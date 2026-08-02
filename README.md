# mywant-grafana-plugin

MyWant custom type plugin that embeds a single Grafana dashboard panel directly into a mywant want card.

## Overview

`grafana_panel` is a **monitor want** that:
1. Periodically checks Grafana connectivity (via `/api/health`)
2. Renders the configured panel as an iframe inside the want card
3. Supports maximize — the panel expands to fill the overlay

## Installation

```bash
cd ~/.mywant/custom-types
git clone https://github.com/onelittlenightmusic/mywant-grafana-plugin
```

The plugin is auto-loaded by mywant on next server start.

## Requirements

- Python 3 (stdlib only — no extra packages needed)
- Grafana running with anonymous access enabled (`GF_AUTH_ANONYMOUS_ENABLED=true`)
- Grafana iframe embedding enabled (`GF_SECURITY_ALLOW_EMBEDDING=true`)

For the bundled `tools/otel/docker-compose.yaml` both are already configured.

## Usage

Deploy a want with type `grafana_panel` and specify the panel coordinates:

```yaml
metadata:
  name: claude-cost-panel
  type: grafana_panel
spec:
  params:
    dashboard_uid: claude-code-telemetry   # from Grafana dashboard URL
    panel_id: 7                            # from Grafana panel share → Embed
    time_from: now-6h                      # Grafana time range (from)
    refresh: 30s                           # auto-refresh interval
    grafana_base_url: http://localhost:3000
```

### Finding `dashboard_uid` and `panel_id`

1. Open the dashboard in Grafana
2. Click the panel title → **Share** → **Embed**
3. The embed URL contains both values:
   ```
   http://localhost:3000/d-solo/<dashboard_uid>/<slug>?orgId=1&panelId=<panel_id>
   ```

### CLI deploy

```bash
./bin/mywant wants create -f my_grafana_panel.yaml
```

## State fields

| Field | Label | Description |
|---|---|---|
| `grafana_base_url` | goal | Grafana base URL (default: `http://localhost:3000`) |
| `dashboard_uid` | goal | Dashboard UID |
| `panel_id` | goal | Panel ID to embed |
| `time_from` | goal | Time range start (e.g. `now-6h`) |
| `refresh` | goal | Auto-refresh interval (e.g. `30s`) |
| `grafana_status` | current | Connectivity: `ok` / `unreachable: …` |

## How the iframe URL is constructed

```
{grafana_base_url}/d-solo/{dashboard_uid}?orgId=1&panelId={panel_id}&from={time_from}&to=now&refresh={refresh}
```

The frontend card plugin (`GrafanaCardPlugin.tsx`) builds this URL from the want's goal state and renders it as an `<iframe>`.
