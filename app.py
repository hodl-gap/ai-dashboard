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
.tag-type-news {
    background-color: #e3f2fd;
    color: #1565c0;
}
.tag-type-tips {
    background-color: #e8f5e9;
    color: #2e7d32;
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


def combine_data(tips_data, news_data) -> list:
    """Combine tips and news into a single list. News first, then Tips."""
    combined = []

    # Handle both list and dict formats
    news_list = news_data if isinstance(news_data, list) else news_data.get("articles", [])
    tips_list = tips_data if isinstance(tips_data, list) else tips_data.get("articles", [])

    # News first
    for article in news_list:
        raw_category = article.get("category", "")
        raw_layer = article.get("layer", "")
        combined.append({
            "type": "News",
            "title": article.get("title", ""),
            "description": article.get("summary", "") or article.get("contents", ""),
            "url": article.get("url", ""),
            "source": article.get("source", ""),
            "date": article.get("pub_date", "") or article.get("date", ""),
            "category": f"News - {raw_category}" if raw_category else "—",
            "category_display": raw_category or "—",
            "layer": f"News - {raw_layer}" if raw_layer else "—",
            "layer_display": raw_layer or "—",
            "region": article.get("region", "—") or "—",
            "source_type": article.get("source_type", "—") or "—",
        })

    # Tips at bottom
    for article in tips_list:
        raw_category = article.get("category", "")
        raw_layer = article.get("layer", "")
        combined.append({
            "type": "Tips",
            "title": article.get("title", ""),
            "description": article.get("summary", "") or article.get("contents", ""),
            "url": article.get("url", ""),
            "source": article.get("source", ""),
            "date": article.get("pub_date", "") or article.get("date", ""),
            "category": f"Tips - {raw_category}" if raw_category else "—",
            "category_display": raw_category or "—",
            "layer": f"Tips - {raw_layer}" if raw_layer else "—",
            "layer_display": raw_layer or "—",
            "region": article.get("region", "—") or "—",
            "source_type": article.get("source_type", "—") or "—",
        })

    return combined


def render_card(item: dict) -> None:
    """Render an item as a styled card."""
    title = item.get("title", "No Title")
    description = item.get("description", "")
    url = item.get("url", "#")
    item_type = item.get("type", "")
    category_display = item.get("category_display", "")
    layer_display = item.get("layer_display", "")
    region = item.get("region", "")
    source_type = item.get("source_type", "")
    date = item.get("date", "")

    # Build tags HTML (use display versions without prefix)
    type_class = "tag-type-news" if item_type == "News" else "tag-type-tips"
    tags_html = f'<span class="tag {type_class}">{item_type}</span>'
    if category_display and category_display != "—":
        tags_html += f'<span class="tag tag-category">{category_display}</span>'
    if layer_display and layer_display != "—":
        tags_html += f'<span class="tag tag-layer">{layer_display}</span>'
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


def main():
    st.title("AI Intelligence Dashboard")

    # Load data
    tips_data = load_json("data/tips.json")
    news_data = load_json("data/news.json")

    # Combine into single dataset
    all_items = combine_data(tips_data, news_data)

    # Extract unique values for filters
    types = sorted(set(item["type"] for item in all_items))
    categories = sorted(set(item["category"] for item in all_items if item["category"] != "—"))
    layers = sorted(set(item["layer"] for item in all_items if item["layer"] != "—"))
    regions = sorted(set(item["region"] for item in all_items if item["region"] != "—"))
    source_types = sorted(set(item["source_type"] for item in all_items if item["source_type"] != "—"))

    # Filters - Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_types = st.multiselect(
            "Type",
            options=types,
            default=types,
        )

    with col2:
        selected_categories = st.multiselect(
            "Category",
            options=categories,
            default=[],
            placeholder="All categories",
        )

    with col3:
        selected_layers = st.multiselect(
            "Layer",
            options=layers,
            default=[],
            placeholder="All layers",
        )

    # Filters - Row 2
    col4, col5, col6 = st.columns(3)

    with col4:
        selected_regions = st.multiselect(
            "Region",
            options=regions,
            default=[],
            placeholder="All regions",
        )

    with col5:
        selected_source_types = st.multiselect(
            "Source Type",
            options=source_types,
            default=[],
            placeholder="All source types",
        )

    st.markdown("---")

    # Filter data
    filtered_items = []
    for item in all_items:
        # Type filter
        if item["type"] not in selected_types:
            continue

        # Category filter (if any selected)
        if selected_categories and item["category"] not in selected_categories and item["category"] != "—":
            continue

        # Layer filter (if any selected)
        if selected_layers and item["layer"] not in selected_layers and item["layer"] != "—":
            continue

        # Region filter (if any selected)
        if selected_regions and item["region"] not in selected_regions and item["region"] != "—":
            continue

        # Source type filter (if any selected)
        if selected_source_types and item["source_type"] not in selected_source_types and item["source_type"] != "—":
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


if __name__ == "__main__":
    main()
