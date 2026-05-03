---
name: meteoblue-weather
description: Weather forecasts via Meteoblue meteograms — dense, single-image forecasts showing temperature, rain, wind, cloud cover, and sunshine across 7 days. Use for any current or upcoming weather question — single location, comparing places, weekend plans, surf, gardening, air quality. Triggers on prompts like "weather in Polzeath", "what's the forecast for Exeter?", "which has better weather, X or Y?", "surf forecast for Croyde", "is it going to rain this weekend?". Not for historical weather, climate questions, or "weather-resistant"-style metaphors.
---

# Meteoblue Weather (Meteogram-first)

A meteogram is a dense visual forecast — temperature, precipitation, wind, cloud cover, and sunshine over a multi-day window in a single image. For the vast majority of weather questions, the meteogram is the answer. Reach for the JSON forecast only when the user needs something the image can't easily show (a specific number, a side-by-side comparison verdict, an unusual variable).

## Steps

### 1. Identify the place(s)

Extract the place name(s) from the user's prompt. Can be one place or several. If no place is mentioned, ask for one.

For each place, derive a filesystem-safe slug (lowercase, spaces and punctuation → underscores) — used for image filenames in step 5. e.g. "St Ives" → `st_ives`, "Bangkok, Thailand" → `bangkok_thailand`.

### 2. Check API key

```bash
echo ${METEOBLUE_API_KEY:?Please set METEOBLUE_API_KEY — get one at https://www.meteoblue.com/en/weather-api}
```

### 3. Geocode each place

Use OpenStreetMap Nominatim to resolve each place name to coordinates. URL-encode the query so place names with spaces or commas work:

```bash
curl -sG "https://nominatim.openstreetmap.org/search" \
  --data-urlencode "q=PLACE_NAME" \
  --data "format=json&limit=1" \
  -H "User-Agent: meteoblue-skill"
```

Extract `lat` and `lon` from the first result. If empty, tell the user and ask them to be more specific (e.g. "Polkerris, Cornwall"). Do not proceed until all places are geocoded.

### 4. Choose the right meteogram

Default to **`meteogram_extended`** (7-day forecast). This is the workhorse — use it unless there's a clear reason to pick a different variant.

Other variants, with when to use each:

- **`meteogram`** — standard 5-day. Use only if the user explicitly wants a shorter horizon.
- **`meteogram_surf`** — wave height, swell, wind on water. Use when the user mentions surf, waves, swell, sailing, kitesurfing, paddleboarding, or the place is a recognisable surf/beach destination and the user is clearly planning a coastal activity.
- **`meteogram_air`** — air quality (PM2.5, ozone, pollen). Use when the user mentions pollution, asthma, allergies, AQI, smog, or city air.
- **`meteogram_agro`** — soil moisture, evapotranspiration. Use for gardening, farming, irrigation, or "is the ground dry enough to plant" prompts.

If multiple variants are clearly relevant (e.g. a surf weekend → extended + surf), fetch both. Don't be stingy — meteograms are cheap.

### 5. Fetch and display the meteogram(s)

For each chosen variant, for each place:

```bash
curl -sG "https://my.meteoblue.com/images/meteogram_extended" \
  --data "lat=LAT&lon=LON&apikey=$METEOBLUE_API_KEY" \
  --data-urlencode "location_name=PLACE_NAME" \
  -o "/tmp/SLUG_extended.png"
```

(Substitute `meteogram_extended` and the filename suffix for whichever variant you're fetching.)

Display each PNG using the **Read** tool — reading a PNG surfaces the image to the user. The image is the primary deliverable; show it before any prose.

### 6. Brief written commentary

After showing the image(s), add a short prose answer to the user's actual question. The image carries the data; your job here is the verdict, not a regurgitation of every number.

Good commentary:
- Names the day(s) in question
- Picks out the one or two things that actually matter (a wet Saturday, a wind shift Tuesday afternoon, UV spiking Sunday)
- Stays under 4–5 lines unless the user asked for detail

Bad commentary:
- Day-by-day rehash of what's already visible in the chart
- "Expect", "looks like", "it appears" hedging — meteograms convey uncertainty visually via the predictability band

### 7. (Optional) Fetch JSON for specific numbers

Only fetch the `basic-day` JSON when the user wants something the meteogram can't easily answer:
- A specific numeric threshold ("will it hit 25°C on Tuesday?")
- A multi-place comparison verdict where you need to cite hard numbers
- An unusual variable not on the chart

```bash
curl -sG "https://my.meteoblue.com/packages/basic-day" \
  --data "lat=LAT&lon=LON&tz=auto&apikey=$METEOBLUE_API_KEY" \
  --data-urlencode "name=PLACE_NAME"
```

The `data_day` object has parallel arrays indexed by day. Useful fields:

- `time` — date for each day
- `temperature_max`, `temperature_min` — °C
- `precipitation` — mm total
- `precipitation_probability` — %
- `predictability` — model confidence (0–100); flag low values
- `uvindex`
- `windspeed_max`, `winddirection`
- `pictocode` — Meteoblue's icon code

Full schema: [Forecast API docs](https://docs.meteoblue.com/en/weather-apis/forecast-api/overview). Image variants: [Image API docs](https://docs.meteoblue.com/en/weather-apis/images-api/overview).

### 8. Compare (if multiple places)

Show every meteogram first (one image per place), then give an honest verdict:

- Name the winner clearly for the date(s) in question
- One or two concrete differences ("Polzeath has half the rainfall and 3°C warmer afternoons")
- If it depends on activity (sheltered walk vs. exposed beach), say so
- If it's genuinely a coin-flip, say that too — don't manufacture a winner
