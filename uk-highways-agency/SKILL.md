---
name: uk highway agency information
description: Check National Highways for planned road closures and roadworks on England's Strategic Road Network (motorways and major A-roads). Use whenever the user asks about road closures, roadworks, travelling or driving on a named road, whether a route is clear, or journey planning on any motorway or A-road in England.
---

Query planned closures for a named road on a given date. **Scope: England's Strategic Road Network only** (motorways and major A-roads managed by National Highways). Data covers up to 14 days ahead.

Convert relative dates ("tonight", "tomorrow", "next Friday") to absolute dates before querying.

## Endpoint — no auth required

```
GET https://services-eu1.arcgis.com/mZXeBXkkZpekxjXT/ArcGIS/rest/services/PublicScheduledRoadClosures/FeatureServer/0/query
```

Key parameters:
- `where` — e.g. `road_number = 'A30' AND scheduledplannedenddate >= timestamp '2026-05-01 00:00:00' AND scheduledplannedstartdate <= timestamp '2026-05-01 23:59:59'`  
  Widen the date range for multi-day queries (e.g. a full week).
- `outFields` — `description,road_number,eventtype,natureofworks,scheduledplannedstartdate,scheduledplannedenddate`
- `returnGeometry=false`, `orderByFields=scheduledplannedstartdate`, `f=json`

Timestamps are Unix milliseconds UTC — convert with `datetime.fromtimestamp(ms/1000)`.  
If `"exceededTransferLimit": true`, paginate with `resultOffset`.

## Response fields

- `road_number`, `eventtype`, `natureofworks`
- `description` — full closure text including diversion routes
- `scheduledplannedstartdate` / `scheduledplannedenddate` — closure window in Unix ms

## Developer API (richer data, includes unplanned closures)

Set `NATIONAL_HIGHWAYS_KEY` from https://developer.data.nationalhighways.co.uk/profile and pass as `Ocp-Apim-Subscription-Key`. The exact endpoint path is only visible once signed in to the developer portal.

## Presenting results

- State total closure count for the road and date.
- For each closure: local time window, direction, nature of works, and diversion from `description`.
- If beyond 14 days ahead, warn data may not yet be published.
- Suggest travelling outside closure windows or using the stated diversion.
