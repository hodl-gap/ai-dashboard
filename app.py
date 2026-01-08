import json
import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
.card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    border: 1px solid #e9ecef;
}
.card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 0.4rem;
    line-height: 1.4;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;
}
.card-title-text {
    flex: 1;
}
.card-date {
    font-size: 0.8rem;
    font-weight: 400;
    color: #888;
    white-space: nowrap;
}
.card-body {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 1rem;
}
.card-description {
    color: #555;
    font-size: 0.85rem;
    line-height: 1.5;
    flex: 1;
}
.card-url {
    flex-shrink: 0;
}
.card-url a {
    color: #1a73e8;
    text-decoration: none;
    font-size: 0.85rem;
    white-space: nowrap;
}
.card-url a:hover {
    text-decoration: underline;
}
.card-tags {
    margin-top: 0.5rem;
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}
.tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 500;
}
.tag-category {
    background-color: #f3e5f5;
    color: #7b1fa2;
}
.tag-layer {
    background-color: #fff3e0;
    color: #e65100;
}
.tag-region {
    background-color: #e8f5e9;
    color: #2e7d32;
}
.tag-source-type {
    background-color: #fce4ec;
    color: #c2185b;
}
</style>
""", unsafe_allow_html=True)


def load_json(filepath: str):
    """Load JSON file and return data."""
    path = Path(filepath)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def parse_articles(data, item_type: str) -> list:
    """Parse articles from data into a standardized format."""
    articles = []

    # Handle both list and dict formats
    article_list = data if isinstance(data, list) else data.get("articles", [])

    for article in article_list:
        articles.append({
            "type": item_type,
            "title": article.get("title", ""),
            "description": article.get("summary", "") or article.get("contents", ""),
            "url": article.get("url", ""),
            "source": article.get("source", ""),
            "date": article.get("pub_date", "") or article.get("date", ""),
            "category": article.get("category", "—"),
            "layer": article.get("layer", "—"),
            "region": article.get("region", "—"),
            "source_type": article.get("source_type", "—"),
        })

    return articles


def render_card(item: dict) -> None:
    """Render an item as a styled card."""
    title = item.get("title", "No Title")
    description = item.get("description", "")
    url = item.get("url", "#")
    category = item.get("category", "")
    layer = item.get("layer", "")
    region = item.get("region", "")
    source_type = item.get("source_type", "")
    date = item.get("date", "")

    # Build tags HTML
    tags_html = ""
    if category and category != "—":
        tags_html += f'<span class="tag tag-category">{category}</span>'
    if layer and layer != "—":
        tags_html += f'<span class="tag tag-layer">{layer}</span>'
    if region and region != "—":
        tags_html += f'<span class="tag tag-region">{region}</span>'
    if source_type and source_type != "—":
        tags_html += f'<span class="tag tag-source-type">{source_type}</span>'

    html = f"""
    <div class="card">
        <div class="card-title">
            <span class="card-title-text">{title}</span>
            <span class="card-date">{date}</span>
        </div>
        <div class="card-body">
            <div class="card-description">{description}</div>
            <div class="card-url">
                <a href="{url}" target="_blank">🔗 Source</a>
            </div>
        </div>
        <div class="card-tags">{tags_html}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_tab(items: list, tab_key: str) -> None:
    """Render a tab with filters and cards."""

    # Extract unique values for filters
    categories = sorted(set(item["category"] for item in items if item["category"] != "—"))
    layers = sorted(set(item["layer"] for item in items if item["layer"] != "—"))
    regions = sorted(set(item["region"] for item in items if item["region"] != "—"))
    source_types = sorted(set(item["source_type"] for item in items if item["source_type"] != "—"))

    # Filters - only show if there are options
    filter_cols = []
    if categories:
        filter_cols.append(("Category", categories, f"{tab_key}_category"))
    if layers:
        filter_cols.append(("Layer", layers, f"{tab_key}_layer"))
    if regions:
        filter_cols.append(("Region", regions, f"{tab_key}_region"))
    if source_types:
        filter_cols.append(("Source Type", source_types, f"{tab_key}_source_type"))

    selected_filters = {}

    if filter_cols:
        cols = st.columns(len(filter_cols))
        for i, (label, options, key) in enumerate(filter_cols):
            with cols[i]:
                selected_filters[key] = st.multiselect(
                    label,
                    options=options,
                    default=[],
                    placeholder=f"All {label.lower()}s",
                    key=key,
                )

        st.markdown("---")

    # Filter data
    filtered_items = []
    for item in items:
        # Category filter
        cat_key = f"{tab_key}_category"
        if cat_key in selected_filters and selected_filters[cat_key]:
            if item["category"] not in selected_filters[cat_key] and item["category"] != "—":
                continue

        # Layer filter
        layer_key = f"{tab_key}_layer"
        if layer_key in selected_filters and selected_filters[layer_key]:
            if item["layer"] not in selected_filters[layer_key] and item["layer"] != "—":
                continue

        # Region filter
        region_key = f"{tab_key}_region"
        if region_key in selected_filters and selected_filters[region_key]:
            if item["region"] not in selected_filters[region_key] and item["region"] != "—":
                continue

        # Source type filter
        source_key = f"{tab_key}_source_type"
        if source_key in selected_filters and selected_filters[source_key]:
            if item["source_type"] not in selected_filters[source_key] and item["source_type"] != "—":
                continue

        filtered_items.append(item)

    # Sort by date (newest first)
    filtered_items.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Display count
    st.markdown(f"**Showing {len(filtered_items)} items**")
    st.markdown("---")

    # Render cards
    if filtered_items:
        for item in filtered_items:
            render_card(item)
    else:
        st.info("No items match the selected filters.")


def main():
    st.title("AI Intelligence Dashboard")

    # Load data
    tips_data = load_json("data/tips.json")
    news_data = load_json("data/news.json")

    # Parse into standardized format
    news_items = parse_articles(news_data, "News")
    tips_items = parse_articles(tips_data, "Tips")

    # Create tabs
    tab_news, tab_tips = st.tabs([f"📰 News ({len(news_items)})", f"💡 Tips ({len(tips_items)})"])

    with tab_news:
        render_tab(news_items, "news")

    with tab_tips:
        render_tab(tips_items, "tips")


if __name__ == "__main__":
    main()
