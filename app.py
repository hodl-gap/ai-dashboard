import json
import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS for card styling
st.markdown("""
<style>
.card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}
.card-title a {
    color: #1a73e8;
    text-decoration: none;
}
.card-title a:hover {
    text-decoration: underline;
}
.badge {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
}
.badge-source {
    background-color: #e3f2fd;
    color: #1565c0;
}
.badge-date {
    background-color: #f3e5f5;
    color: #7b1fa2;
}
.badge-category {
    background-color: #fff3e0;
    color: #e65100;
}
.badge-region {
    background-color: #e8f5e9;
    color: #2e7d32;
}
.badge-layer {
    background-color: #fce4ec;
    color: #c2185b;
}
.card-content {
    color: #495057;
    font-size: 0.9rem;
    line-height: 1.6;
}
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e9ecef;
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


def render_tip_card(article: dict) -> None:
    """Render a tip article as a styled card."""
    title = article.get("title", "No Title")
    url = article.get("url", "#")
    source = article.get("source", "Unknown")
    source_type = article.get("source_type", "")
    date = article.get("date", "")
    contents = article.get("contents", "")

    html = f"""
    <div class="card">
        <div class="card-title">
            <a href="{url}" target="_blank">{title}</a>
        </div>
        <div>
            <span class="badge badge-source">{source}</span>
            <span class="badge badge-date">{date}</span>
            {f'<span class="badge badge-category">{source_type}</span>' if source_type else ''}
        </div>
        <div class="card-content" style="margin-top: 0.5rem;">
            {contents}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_news_card(article: dict) -> None:
    """Render a news article as a styled card."""
    title = article.get("title", "No Title")
    url = article.get("url", "#")
    source = article.get("source", "Unknown")
    date = article.get("date", "")
    region = article.get("region", "")
    category = article.get("category", "")
    layer = article.get("layer", "")
    contents = article.get("contents", "")

    badges_html = f'<span class="badge badge-source">{source}</span>'
    badges_html += f'<span class="badge badge-date">{date}</span>'
    if region:
        badges_html += f'<span class="badge badge-region">{region}</span>'
    if category:
        badges_html += f'<span class="badge badge-category">{category}</span>'
    if layer:
        badges_html += f'<span class="badge badge-layer">{layer}</span>'

    html = f"""
    <div class="card">
        <div class="card-title">
            <a href="{url}" target="_blank">{title}</a>
        </div>
        <div>
            {badges_html}
        </div>
        <div class="card-content" style="margin-top: 0.5rem;">
            {contents}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def main():
    # Header
    st.title("AI Intelligence Dashboard")
    st.markdown("---")

    # Load data
    tips_data = load_json("data/tips.json")
    news_data = load_json("data/news.json")

    tips_articles = tips_data.get("articles", [])
    news_articles = news_data.get("articles", [])

    # Display metadata
    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        tips_meta = tips_data.get("metadata", {})
        st.metric("Total Tips", tips_meta.get("total", len(tips_articles)))
    with col_meta2:
        news_meta = news_data.get("metadata", {})
        st.metric("Total News", news_meta.get("total_articles", len(news_articles)))

    st.markdown("---")

    # Two-column layout for Tips and News
    col_tips, col_news = st.columns(2)

    with col_tips:
        st.markdown('<div class="section-header">Tips</div>', unsafe_allow_html=True)
        if tips_articles:
            for article in tips_articles:
                render_tip_card(article)
        else:
            st.info("No tips available.")

    with col_news:
        st.markdown('<div class="section-header">News</div>', unsafe_allow_html=True)
        if news_articles:
            for article in news_articles:
                render_news_card(article)
        else:
            st.info("No news available.")


if __name__ == "__main__":
    main()
