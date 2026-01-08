# AI Intelligence Dashboard

A Streamlit-based dashboard for viewing AI-related news and tips from various sources.

## Live Demo

Deployed on Streamlit Community Cloud: [https://hodl-gap-ai-dashboard.streamlit.app](https://hodl-gap-ai-dashboard.streamlit.app)

---

## Project Structure

```
ai-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── data/
    ├── news.json       # AI news articles
    └── tips.json       # AI tips and tutorials
```

---

## Data Schema

### news.json / tips.json

Both files are JSON arrays with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Original article URL |
| `title` | string | Article title |
| `summary` | string | Article description/summary |
| `source` | string | Source name (e.g., "36Kr", "Marktechpost") |
| `source_type` | string | Source type: `rss` or `twitter` |
| `pub_date` | string | Publication date (YYYY-MM-DD) |
| `region` | string | Geographic region (e.g., "east_asia", "north_america") |
| `category` | string | Content category (e.g., "strategy", "product_launch") |
| `layer` | string | AI layer (e.g., "b2b_apps", "infrastructure") |
| `created_at` | string | Record creation timestamp |

---

## Features

- **Unified View**: News and Tips displayed in a single, scrollable list
- **5 Filters**: Type, Category, Layer, Region, Source Type
- **Card Layout**: Each item shows:
  - Title (with date on the right)
  - Description
  - Source link
  - Color-coded tags
- **Sorted by Date**: Newest items appear first

### Tag Colors

| Tag | Color | Description |
|-----|-------|-------------|
| Type | Blue | News or Tips |
| Category | Purple | Content category |
| Layer | Orange | AI stack layer |
| Region | Green | Geographic region |
| Source Type | Pink | RSS or Twitter |

---

## Local Development

```bash
# Install dependencies
pip install streamlit

# Run locally
streamlit run app.py
```

Opens at: http://localhost:8501

---

## Deployment (Streamlit Cloud)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository: `hodl-gap/ai-dashboard`
4. Set main file: `app.py`
5. Deploy

---

## Changelog

### 2026-01-08

- **v1.0.0** - Initial release
  - Basic two-column layout (Tips | News)
  - Card styling with clickable URLs

- **v1.1.0** - Single list layout
  - Merged Tips and News into unified list
  - Added filters: Category, Layer, Region
  - Added color-coded tags below each card

- **v1.2.0** - Enhanced filters and tags
  - Renamed "Category" filter to "Type" (News/Tips)
  - Added actual "Category" filter (strategy, product_launch, etc.)
  - Added "Source Type" filter (rss, twitter)
  - All 5 tags now displayed on cards

- **v1.3.0** - Date improvements
  - Added publication date to card title
  - Sort items by date (newest first)
  - Fixed JSON format compatibility (list vs dict)
  - Support both `summary`/`contents` and `pub_date`/`date` fields
