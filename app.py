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
    background-color: #e3f2fd;
    color: #1565c0;
}
.tag-layer {
    background-color: #fff3e0;
    color: #e65100;
}
.tag-region {
    background-color: #e8f5e9;
    color: #2e7d32;
}
.filter-section {
    padding: 1rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #e9ecef;
}
</style>
""", unsafe_allow_html=True)


def load_json(filepath: str) -> dict:
    """Load JSON file and return data."""
    path = Path(filepath)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"articles": [], "metadata": {}}


def combine_data(tips_data: dict, news_data: dict) -> list:
    """Combine tips and news into a single list with category field. News first, then Tips."""
    combined = []

    # News first
    for article in news_data.get("articles", []):
        combined.append({
            "category": "News",
            "title": article.get("title", ""),
            "description": article.get("contents", ""),
            "url": article.get("url", ""),
            "source": article.get("source", ""),
            "date": article.get("date", ""),
            "layer": article.get("layer", "—"),
            "region": article.get("region", "—"),
        })

    # Tips at bottom
    for article in tips_data.get("articles", []):
        combined.append({
            "category": "Tips",
            "title": article.get("title", ""),
            "description": article.get("contents", ""),
            "url": article.get("url", ""),
            "source": article.get("source", ""),
            "date": article.get("date", ""),
            "layer": article.get("layer", "—"),
            "region": article.get("region", "—"),
        })

    return combined


def render_card(item: dict) -> None:
    """Render an item as a styled card."""
    title = item.get("title", "No Title")
    description = item.get("description", "")
    url = item.get("url", "#")
    category = item.get("category", "")
    layer = item.get("layer", "")
    region = item.get("region", "")

    # Build tags HTML
    tags_html = f'<span class="tag tag-category">{category}</span>'
    if layer and layer != "—":
        tags_html += f'<span class="tag tag-layer">{layer}</span>'
    if region and region != "—":
        tags_html += f'<span class="tag tag-region">{region}</span>'

    html = f"""
    <div class="card">
        <div class="card-title">{title}</div>
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
    categories = sorted(set(item["category"] for item in all_items))
    layers = sorted(set(item["layer"] for item in all_items if item["layer"] != "—"))
    regions = sorted(set(item["region"] for item in all_items if item["region"] != "—"))

    # Filters
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_categories = st.multiselect(
            "Category",
            options=categories,
            default=categories,
        )

    with col2:
        selected_layers = st.multiselect(
            "Layer",
            options=layers,
            default=[],
            placeholder="All layers",
        )

    with col3:
        selected_regions = st.multiselect(
            "Region",
            options=regions,
            default=[],
            placeholder="All regions",
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Filter data
    filtered_items = []
    for item in all_items:
        # Category filter
        if item["category"] not in selected_categories:
            continue

        # Layer filter (if any selected)
        if selected_layers and item["layer"] not in selected_layers and item["layer"] != "—":
            continue

        # Region filter (if any selected)
        if selected_regions and item["region"] not in selected_regions and item["region"] != "—":
            continue

        filtered_items.append(item)

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
