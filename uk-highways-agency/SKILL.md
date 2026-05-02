---
name: uk-highways-agency
description: Check planned road closures, roadworks, lane restrictions, or overnight works on a specific motorway or A-road in England's Strategic Road Network (managed by National Highways). Triggers on "is the M25 closed tonight", "any roadworks on the A30 this weekend", "A1 closures next Friday", "M5 overnight works". Covers up to 14 days ahead. Not for live traffic conditions, accidents, speed limits, or routing.
---

Query planned closures for a named road on a given date. **Scope: England's Strategic Road Network only** (motorways and major A-roads managed by National Highways). Data covers up to 14 days ahead.

Convert relative dates ("tonight", "tomorrow", "next Friday") to absolute dates before querying. **Timestamps in `where` clauses are UTC** — for late-night queries near midnight UK local time (BST/GMT), be careful which calendar day you mean.

## Endpoint — no auth required

```
GET https://services-eu1.arcgis.com/mZXeBXkkZpekxjXT/ArcGIS/rest/services/PublicScheduledRoadClosures/FeatureServer/0/query
```

### Worked example: A30 closures on 2026-05-01

```bash
curl -sG \
  --data-urlencode "where=road_number = 'A30' AND scheduledplannedenddate >= timestamp '2026-05-01 00:00:00' AND scheduledplannedstartdate <= timestamp '2026-05-01 23:59:59'" \
  --data-urlencode "outFields=description,road_number,eventtype,natureofworks,scheduledplannedstartdate,scheduledplannedenddate" \
  --data "returnGeometry=false&orderByFields=scheduledplannedstartdate&f=json" \
  "https://services-eu1.arcgis.com/mZXeBXkkZpekxjXT/ArcGIS/rest/services/PublicScheduledRoadClosures/FeatureServer/0/query"
```

`road_number` values are uppercase, no space: `A30`, `M25`, `A1(M)`. Widen the date range for multi-day queries.

If the response has `"exceededTransferLimit": true`, paginate with `resultOffset`.

## Response fields

- `road_number`, `eventtype`, `natureofworks`
- `description` — full closure text including diversion routes
- `scheduledplannedstartdate` / `scheduledplannedenddate` — Unix milliseconds UTC. Convert with `datetime.fromtimestamp(ms/1000, tz=timezone.utc)` then localise to Europe/London for display.

## Presenting results

- State total closure count for the road and date.
- For each closure: local time window (Europe/London), direction, nature of works, and diversion from `description`.
- If beyond 14 days ahead, warn data may not yet be published.
- Suggest travelling outside closure windows or using the stated diversion.
