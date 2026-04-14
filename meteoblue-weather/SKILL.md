---
name: meteoblue
description: Weather forecasts using the free Meteoblue Forecast & Image APIs (Meteograms). Use this skill for any weather-related question — a single location forecast, comparing two places, weekend plans, surf conditions, or anything involving weather. Triggers on prompts like "weather in Polzeath", "what's the forecast for Exeter?", "which has better weather, X or Y?", etc.
---

# Meteoblue Weather (Forecast & Image API)

Get weather forecasts and meteogram images for one or more places.

## Steps

### 1. Identify the place(s)

Extract the place name(s) from the user's prompt. Can be one place or several. If no place is mentioned, ask for one.

### 2. Check API key

```bash
echo ${METEOBLUE_API_KEY:?Please set METEOBLUE_API_KEY — get one at https://www.meteoblue.com/en/weather-api}
```

### 3. Geocode each place

Use OpenStreetMap Nominatim to resolve each place name to coordinates:

```bash
curl -s "https://nominatim.openstreetmap.org/search?q=PLACE_NAME&format=json&limit=1" \
  -H "User-Agent: meteoblue-skill"
```

Extract `lat` and `lon` from the first result. If empty, tell the user and ask them to be more specific (e.g. "Polkerris, Cornwall"). Do not proceed until all places are geocoded.

### 4. Fetch weather forecasts (Forecast API)

For each place, fetch the **basic-day** package:

```bash
curl -s "https://my.meteoblue.com/packages/basic-day?lat=LAT&lon=LON&name=PLACE_NAME&tz=Europe%2FLondon&apikey=$METEOBLUE_API_KEY"
```

### 5. Fetch meteogram images (Image API)

For each place, download the **standard meteogram**:

```bash
curl -s "https://my.meteoblue.com/images/meteogram?lat=LAT&lon=LON&location_name=PLACE_NAME&apikey=$METEOBLUE_API_KEY" \
  -o /tmp/PLACENAME_meteogram.png
```

Display it inline using the **read** tool.

#### Surf meteogram (coastal places only)

If a place is coastal (use your general knowledge), also fetch the **surf meteogram**:

```bash
curl -s "https://my.meteoblue.com/images/meteogram_surf?lat=LAT&lon=LON&location_name=PLACE_NAME&apikey=$METEOBLUE_API_KEY" \
  -o /tmp/PLACENAME_surf.png
```

Display inline with the read tool.

### 6. Summarise the forecast

Detect the user's time intent (e.g. "today", "this weekend", "next week"). If unspecified, summarise the next 3 days.

Interpret the JSON response fields directly — refer to the [Forecast API docs](https://docs.meteoblue.com/en/weather-apis/forecast-api/overview) and [Image API docs](https://docs.meteoblue.com/en/weather-apis/images-api/overview) for field definitions if needed.

### 7. Compare (if multiple places)

If the user asked about more than one place, compare them and give an honest verdict:
- Name the winner clearly
- Explain key differences (e.g. "Polzeath has half the rainfall and higher UV")
- If it's close or depends on activity (hiking vs. beach), say so
- Mention the specific date(s) compared

Keep it concise and practical.
