import base64
import html
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="ORBITAL ATLAS",
    layout="wide",
    initial_sidebar_state="expanded"
)

RED = "#AB6F74"
LIGHT_RED = "#FF8592"
DARK_RED = "#F398A5"
ROSE = "#F5B0BA"
DEEP = "#ECA3AE"

CHART_COLORS = [RED, LIGHT_RED, DARK_RED, ROSE, DEEP]

BASE_DIR = Path(__file__).resolve().parent


# ==================================================
# 2. THEME (CSS + BACKGROUND IMAGE)
# ==================================================

@st.cache_data
def get_background_css():

    image_data = None

    for name in ["bg_space2.jpeg", "bg_space2.jpg", "bg_space2.png"]:

        path = BASE_DIR / name

        if path.exists():

            mime = "image/png" if name.endswith(".png") else "image/jpeg"
            encoded = base64.b64encode(path.read_bytes()).decode()
            image_data = f"data:{mime};base64,{encoded}"
            break

    overlay = (
        "linear-gradient(180deg, rgba(20,6,12,0.45) 0%, "
        "rgba(28,8,16,0.60) 55%, rgba(14,4,9,0.80) 100%)"
    )

    if image_data:
        return f"{overlay}, url('{image_data}')"

    return (
        "radial-gradient(circle at 20% 0%, #3A1220 0%, "
        "#1A0810 45%, #0E0408 100%)"
    )


THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- Background ---------- */
.stApp {
    background: __BACKGROUND__;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #FCE8EB;
}

header[data-testid="stHeader"] { background: transparent; }

#MainMenu, footer { visibility: hidden; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: rgba(22, 8, 14, 0.82);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(230, 57, 70, 0.25);
}

section[data-testid="stSidebar"] h1 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 4px;
    font-size: 1.5rem;
    color: #FFE3E7;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: __LIGHT_RED__;
    letter-spacing: 2px;
    font-size: 0.7rem;
}

/* ---------- Typography ---------- */
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: #FFE3E7; }
h2 { font-size: 1.5rem; font-weight: 600; }
h3 { font-size: 1.1rem; color: #FFD5DC; }
hr { border-color: rgba(230, 57, 70, 0.22); }

/* ---------- Hero ---------- */
.hero {
    padding: 2.4rem 2.2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(158, 38, 56, 0.35), rgba(24, 8, 14, 0.75));
    border: 1px solid rgba(230, 57, 70, 0.35);
    backdrop-filter: blur(10px);
    margin-bottom: 1.6rem;
}

.hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 4px;
    color: __LIGHT_RED__;
    margin-bottom: 0.6rem;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: 8px;
    line-height: 1.1;
    background: linear-gradient(90deg, #FFE3E7, __LIGHT_RED__, __RED__);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem;
}

.hero-text {
    color: #E5B8BF;
    font-size: 1rem;
    max-width: 680px;
    line-height: 1.7;
}

/* ---------- Section headings ---------- */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 600;
    color: #FFE3E7;
    margin: 1.2rem 0 0.15rem 0;
    padding-left: 0.8rem;
    border-left: 4px solid __RED__;
}

.section-sub {
    color: #C99AA3;
    font-size: 0.88rem;
    margin: 0 0 1rem 0.95rem;
}

/* ---------- Insight box (under every chart) ---------- */
.insight {
    margin-top: 0.4rem;
    padding: 0.85rem 1.1rem;
    border-radius: 12px;
    background: linear-gradient(90deg, rgba(255, 133, 146, 0.14), rgba(255, 133, 146, 0.03));
    border-left: 4px solid __LIGHT_RED__;
}

.insight-label {
    font-size: 0.66rem;
    letter-spacing: 3px;
    color: __LIGHT_RED__;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.insight-text {
    color: #F5D5DA;
    font-size: 0.93rem;
    line-height: 1.65;
}

.insight-text b { color: #FFFFFF; }

/* ---------- Narrative / story card ---------- */
.story {
    padding: 1.3rem 1.5rem;
    border-radius: 16px;
    background: rgba(26, 9, 17, 0.62);
    border: 1px solid rgba(230, 57, 70, 0.22);
    color: #F5D5DA;
    line-height: 1.85;
    font-size: 0.98rem;
}

.story b { color: #FFFFFF; }

/* ---------- Record cards ---------- */
.record-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 0.9rem;
    margin-top: 0.4rem;
}

.record {
    padding: 1rem 1.1rem;
    border-radius: 14px;
    background: rgba(30, 11, 20, 0.70);
    border: 1px solid rgba(230, 57, 70, 0.22);
    border-top: 3px solid __RED__;
}

.record-date { font-size: 0.72rem; letter-spacing: 2px; color: __LIGHT_RED__; }
.record-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; color: #FFE3E7; margin: 0.25rem 0 0.35rem 0; }
.record-line { font-size: 0.85rem; color: #E5B8BF; line-height: 1.6; }
.record-line b { color: #FFFFFF; font-weight: 500; }

.badge {
    display: inline-block;
    padding: 0.12rem 0.6rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 0.5rem;
}

.badge-success { background: rgba(245, 176, 186, 0.20); color: #F5B0BA; border: 1px solid rgba(245, 176, 186, 0.45); }
.badge-failure { background: rgba(158, 38, 56, 0.45); color: #FFD5DC; border: 1px solid rgba(255, 107, 122, 0.55); }
.badge-partial { background: rgba(171, 111, 116, 0.30); color: #ECA3AE; border: 1px solid rgba(236, 163, 174, 0.40); }
.badge-other   { background: rgba(255, 255, 255, 0.08); color: #E5B8BF; border: 1px solid rgba(255, 255, 255, 0.15); }


/* ---------- Chart header ---------- */
.chart-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #FFE3E7;
    margin: 0.2rem 0 0.7rem 0.2rem;
}

/* ---------- CSS bar charts ---------- */
.bars { padding: 0.2rem 0.2rem 0.4rem 0.2rem; }

.bar-row {
    display: grid;
    grid-template-columns: minmax(120px, 34%) 1fr 90px;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.55rem;
}

.bar-label { font-size: 0.85rem; color: #F5D5DA; text-align: right; line-height: 1.25; }

.bar-track {
    height: 16px;
    border-radius: 999px;
    background: rgba(255, 133, 146, 0.10);
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, __DARK_RED__, __RED__, __LIGHT_RED__);
}

.bar-value { font-size: 0.85rem; color: #FFE3E7; font-weight: 600; }

/* ---------- CSS heatmap ---------- */
.heat { width: 100%; border-collapse: separate; border-spacing: 4px; }
.heat th { font-size: 0.8rem; color: #D9A3AC; font-weight: 500; padding: 0.4rem; }
.heat td {
    text-align: center;
    padding: 1rem 0.4rem;
    border-radius: 10px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    color: #FFFFFF;
}
.heat td.rowlabel { background: none; font-size: 0.8rem; color: #D9A3AC; text-align: right; padding-right: 0.8rem; }


/* ---------- Transparent tables ---------- */
.table-wrap {
    overflow: auto;
    max-height: 480px;
    border-radius: 14px;
    background: transparent;
    border: 1px solid rgba(230, 57, 70, 0.22);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    background: transparent;
    font-size: 0.86rem;
    color: #F5D5DA;
}

.data-table th {
    position: sticky;
    top: 0;
    background: rgba(40, 12, 22, 0.88);
    backdrop-filter: blur(8px);
    color: __LIGHT_RED__;
    font-weight: 600;
    font-size: 0.72rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    text-align: left;
    padding: 0.7rem 0.9rem;
    border-bottom: 1px solid rgba(230, 57, 70, 0.35);
    white-space: nowrap;
}

.data-table td {
    padding: 0.6rem 0.9rem;
    border-bottom: 1px solid rgba(255, 133, 146, 0.10);
    background: transparent;
    white-space: nowrap;
}

.data-table tr:hover td { background: rgba(255, 133, 146, 0.08); }
.data-table td:first-child { color: #FFE3E7; font-weight: 500; }


/* ---------- Spacing between boxes ---------- */
[data-testid="stVerticalBlock"] { gap: 1.4rem; }
[data-testid="stHorizontalBlock"] { gap: 1.4rem; }

/* tighter spacing inside a card (title, chart, insight) */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] { gap: 0.9rem; }
[data-testid="stVerticalBlockBorderWrapper"] { padding: 0.4rem 0.5rem; }

.story { margin-bottom: 0.4rem; }
.record-grid { margin-bottom: 0.6rem; gap: 1.2rem; }
.insight { margin-top: 0.2rem; }

/* ---------- Metric cards ---------- */
[data-testid="stMetric"] {
    background: rgba(30, 11, 20, 0.70);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(230, 57, 70, 0.25);
    border-left: 4px solid __RED__;
    border-radius: 14px;
    padding: 1rem 1.2rem;
}

[data-testid="stMetricLabel"] {
    color: #D9A3AC;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 0.72rem;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif;
    color: #FFE3E7;
    font-weight: 600;
}

/* ---------- Bordered containers (glass cards) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(26, 9, 17, 0.62);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(230, 57, 70, 0.22) !important;
    border-radius: 16px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetric"] {
    background: none;
    border: none;
    padding: 0;
    backdrop-filter: none;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.4rem;
    border-bottom: 1px solid rgba(230, 57, 70, 0.25);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #D9A3AC;
    padding: 0.7rem 1.4rem;
    border-radius: 10px 10px 0 0;
    letter-spacing: 1px;
}

.stTabs [aria-selected="true"] {
    background: rgba(230, 57, 70, 0.18);
    color: #FFFFFF;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: __RED__;
    height: 3px;
}

/* ---------- Buttons ---------- */
.stDownloadButton button {
    background: linear-gradient(90deg, __DARK_RED__, __RED__);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    letter-spacing: 1px;
}

.stDownloadButton button:hover {
    background: linear-gradient(90deg, __RED__, __LIGHT_RED__);
    color: white;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    background: rgba(30, 11, 20, 0.70);
    border: 1px solid rgba(230, 57, 70, 0.25);
    border-radius: 12px;
}
</style>
"""


def apply_theme():

    css = (
        THEME_CSS
        .replace("__BACKGROUND__", get_background_css())
        .replace("__LIGHT_RED__", LIGHT_RED)
        .replace("__DARK_RED__", DARK_RED)
        .replace("__RED__", RED)
    )

    st.markdown(css, unsafe_allow_html=True)


apply_theme()


# ==================================================
# 3. SMALL HELPERS
# ==================================================

def esc(value):
    return html.escape(str(value))


def pct(part, whole):
    return part / whole * 100 if whole else 0.0


def fmt(value):
    """Readable number: thousands separators, 0 or 1 decimals."""
    if pd.isna(value):
        return "-"
    if abs(value) >= 1000:
        return f"{value:,.0f}"
    return f"{value:,.1f}"


def section(title, subtitle=""):

    st.markdown(
        f'<div class="section-title">{esc(title)}</div>'
        f'<div class="section-sub">{esc(subtitle)}</div>',
        unsafe_allow_html=True
    )


def insight_box(text):
    """Insight text may contain <b> tags (built by us); dynamic values are escaped."""

    st.markdown(
        '<div class="insight"><div class="insight-label">INSIGHT</div>'
        f'<div class="insight-text">{text}</div></div>',
        unsafe_allow_html=True
    )


# ==================================================
# 4. LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    csv_path = None

    for filename in ["Space_Cleaned.csv", "Space_cleaned2.csv", "Space_Cleaned2.csv"]:

        path = BASE_DIR / filename

        if path.exists():
            csv_path = path
            break

    if csv_path is None:

        matches = sorted(BASE_DIR.glob("[Ss]pace*.csv"))

        if matches:
            csv_path = matches[0]

    if csv_path is None:
        raise FileNotFoundError(
            "Space_Cleaned.csv was not found in the project folder."
        )

    data = pd.read_csv(csv_path, low_memory=False)

    data["rocket_launch_date_utc"] = pd.to_datetime(
        data["rocket_launch_date_utc"],
        errors="coerce",
        format="mixed",
        utc=True
    )

    data["launch_year"] = data["rocket_launch_date_utc"].dt.year

    numeric_columns = [
        "orbital_period_minutes",
        "orbital_inclination_degrees",
        "highest_orbital_altitude_km",
        "lowest_orbital_altitude_km"
    ]

    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    launch_df = data.drop_duplicates(subset=["launch_id"]).copy()

    satellite_df = (
        data.dropna(subset=["satellite_norad_id"])
        .drop_duplicates(subset=["satellite_norad_id"])
        .copy()
    )

    return data, launch_df, satellite_df


try:
    df, launch_df, satellite_df = load_data()

except Exception as e:
    st.error(f"Data Loading Error: {e}")
    st.stop()


# ==================================================
# 5. CHART HELPERS (pure Streamlit + CSS)
# ==================================================

def stretch(func, *args, **kwargs):

    # Works with both old and new Streamlit versions
    try:
        return func(*args, width="stretch", **kwargs)

    except Exception:
        return func(*args, use_container_width=True, **kwargs)


def chart_title(text):

    st.markdown(f'<div class="chart-title">{esc(text)}</div>', unsafe_allow_html=True)


def hbar_html(labels, values, value_fmt=None, max_value=None):
    """Ranked horizontal bars drawn with CSS only."""

    values = list(values)
    top = max_value or (max(values) if values else 1) or 1
    rows = []

    for label, value in zip(labels, values):

        width = max(value / top * 100, 0.6)
        text = value_fmt(value) if value_fmt else f"{value:,.0f}"

        rows.append(
            '<div class="bar-row">'
            f'<div class="bar-label">{esc(label)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{width:.1f}%"></div></div>'
            f'<div class="bar-value">{text}</div>'
            '</div>'
        )

    return '<div class="bars">' + "".join(rows) + '</div>'


def bar_card(title, labels, values, note=None, value_fmt=None, max_value=None):

    with st.container(border=True):

        chart_title(title)

        st.markdown(
            hbar_html(labels, values, value_fmt, max_value),
            unsafe_allow_html=True
        )

        if note:
            insight_box(note)


# Transparent charts drawn with Streamlit's own st.vega_lite_chart
VL_CONFIG = {
    "view": {"stroke": None},
    "axis": {
        "gridColor": "rgba(255, 133, 146, 0.12)",
        "domainColor": "rgba(255, 133, 146, 0.30)",
        "tickColor": "rgba(255, 133, 146, 0.30)",
        "labelColor": "#F5D5DA",
        "titleColor": "#F5D5DA",
        "labelFont": "Inter, sans-serif",
        "titleFont": "Inter, sans-serif",
        "labelFontSize": 12,
        "titleFontSize": 13,
        "titlePadding": 12
    }
}


def vl_chart(data, spec):

    full_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "background": "transparent",
        "config": VL_CONFIG,
        "width": "container",
    }
    full_spec.update(spec)

    stretch(st.vega_lite_chart, data, full_spec, theme=None)


AREA_GRADIENT = {
    "gradient": "linear",
    "x1": 1, "y1": 1, "x2": 1, "y2": 0,
    "stops": [
        {"offset": 0, "color": "rgba(230, 57, 70, 0.03)"},
        {"offset": 1, "color": "rgba(230, 57, 70, 0.38)"}
    ]
}


def area_spec(height=380):

    return {
        "height": height,
        "mark": {
            "type": "area",
            "color": AREA_GRADIENT,
            "line": {"color": RED, "strokeWidth": 3},
            "point": {"filled": True, "color": LIGHT_RED, "size": 45}
        },
        "encoding": {
            "x": {"field": "year", "type": "temporal", "title": "Launch Year",
                  "axis": {"format": "%Y", "grid": False}},
            "y": {"field": "launches", "type": "quantitative",
                  "title": "Number of Launches"},
            "tooltip": [
                {"field": "year", "type": "temporal", "title": "Year", "format": "%Y"},
                {"field": "launches", "type": "quantitative", "title": "Launches"}
            ]
        }
    }


def year_bar_spec(height=340):

    return {
        "height": height,
        "mark": {"type": "bar", "color": RED,
                 "cornerRadiusTopLeft": 3, "cornerRadiusTopRight": 3,
                 "width": {"band": 0.75}},
        "encoding": {
            "x": {"field": "year", "type": "temporal", "timeUnit": "year",
                  "title": "Launch Year",
                  "axis": {"format": "%Y", "grid": False}},
            "y": {"field": "satellites", "type": "quantitative",
                  "title": "Number of Satellites"},
            "tooltip": [
                {"field": "year", "type": "temporal", "timeUnit": "year",
                 "title": "Year", "format": "%Y"},
                {"field": "satellites", "type": "quantitative", "title": "Satellites"}
            ]
        }
    }


def scatter_spec(height=430):

    return {
        "height": height,
        "params": [{"name": "zoom", "select": "interval", "bind": "scales"}],
        "mark": {"type": "point", "filled": True, "color": RED,
                 "opacity": 0.55, "size": 28},
        "encoding": {
            "x": {"field": "altitude", "type": "quantitative",
                  "scale": {"type": "log"},
                  "title": "Highest Orbital Altitude (km)",
                  "axis": {"format": "~s"}},
            "y": {"field": "period", "type": "quantitative",
                  "scale": {"type": "log"},
                  "title": "Orbital Period (Minutes)",
                  "axis": {"format": "~s"}},
            "tooltip": [
                {"field": "name", "type": "nominal", "title": "Satellite"},
                {"field": "altitude", "type": "quantitative",
                 "title": "Highest altitude (km)", "format": ",.0f"},
                {"field": "period", "type": "quantitative",
                 "title": "Period (min)", "format": ",.1f"}
            ]
        }
    }


def native_card(title, draw, note=None):
    """draw() renders a native Streamlit chart inside the card."""

    with st.container(border=True):

        chart_title(title)

        draw()

        if note:
            insight_box(note)


def year_to_date(years):
    return pd.to_datetime(years.astype(int).astype(str), format="%Y")


def bin_counts(series, edges, labels):

    cut = pd.cut(series.dropna(), bins=edges, labels=labels, right=False)

    return cut.value_counts(sort=False)


def show_table(data, max_rows=None, **kwargs):
    """Transparent table drawn with HTML + CSS so it matches the theme."""

    d = data.head(max_rows) if max_rows else data

    def cell(v):
        if isinstance(v, float):
            return "" if pd.isna(v) else f"{v:,.2f}"
        if v is None or v is pd.NaT:
            return ""
        return esc(v)

    head = "".join(f"<th>{esc(c)}</th>" for c in d.columns)

    rows = "".join(
        "<tr>" + "".join(f"<td>{cell(v)}</td>" for v in rec) + "</tr>"
        for rec in d.itertuples(index=False)
    )

    st.markdown(
        '<div class="table-wrap"><table class="data-table">'
        f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True
    )


# ==================================================
# 6. SIDEBAR
# ==================================================

st.sidebar.title("ORBITAL ATLAS")

st.sidebar.caption("SPACE INTELLIGENCE DASHBOARD")

st.sidebar.write(
    "Explore rocket launches, satellite records, "
    "mission outcomes, and orbital characteristics."
)

st.sidebar.divider()

st.sidebar.subheader("Mission Filters")

available_years = launch_df["launch_year"].dropna()

if available_years.empty:
    st.error("No valid launch dates found.")
    st.stop()

min_year = int(available_years.min())
max_year = int(available_years.max())

selected_years = st.sidebar.slider(
    "Launch Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


def get_options(column):

    return sorted(
        launch_df[column].dropna().astype(str).unique().tolist()
    )


selected_countries = st.sidebar.multiselect(
    "Launch Country", get_options("launch_country")
)

selected_organizations = st.sidebar.multiselect(
    "Launch Organization", get_options("launch_organization")
)

selected_outcomes = st.sidebar.multiselect(
    "Launch Outcome", get_options("launch_outcome")
)

selected_orbits = st.sidebar.multiselect(
    "Orbit Category", get_options("launch_orbit_category")
)


# ==================================================
# 7. APPLY FILTERS
# ==================================================

filtered_launches = launch_df[
    launch_df["launch_year"].between(selected_years[0], selected_years[1])
].copy()

filters = {
    "launch_country": selected_countries,
    "launch_organization": selected_organizations,
    "launch_outcome": selected_outcomes,
    "launch_orbit_category": selected_orbits
}

for column, selected in filters.items():

    if selected:
        filtered_launches = filtered_launches[
            filtered_launches[column].astype(str).isin(selected)
        ]

filtered_satellites = satellite_df[
    satellite_df["launch_id"].isin(filtered_launches["launch_id"])
].copy()

filtered_df = df[
    df["launch_id"].isin(filtered_launches["launch_id"])
].copy()


# ==================================================
# 8. HERO HEADER
# ==================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-eyebrow">SPACE INTELLIGENCE PLATFORM</div>'
    '<div class="hero-title">ORBITAL ATLAS</div>'
    '<div class="hero-text">Explore the history of rocket launches, analyze '
    'mission outcomes, and discover satellite orbital patterns through '
    'interactive data.</div>'
    '</div>',
    unsafe_allow_html=True
)

if filtered_launches.empty:
    st.warning("No data matches the selected filters.")
    st.stop()


# ==================================================
# 9. KEY PERFORMANCE INDICATORS
# ==================================================

is_success = (
    filtered_launches["launch_outcome"].astype(str).str.lower().eq("success")
)

total_launches = len(filtered_launches)
total_satellites = filtered_satellites["satellite_norad_id"].nunique()
successful_launches = int(is_success.sum())
success_rate = pct(successful_launches, total_launches)
total_organizations = filtered_launches["launch_organization"].nunique()
total_countries = filtered_launches["launch_country"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Recorded Launches", f"{total_launches:,}")
k2.metric("Registered Satellites", f"{total_satellites:,}")
k3.metric("Launch Success Rate", f"{success_rate:.1f}%")
k4.metric("Launch Organizations", f"{total_organizations:,}")
k5.metric("Launch Countries", f"{total_countries:,}")

st.caption(
    f"Showing launches from {selected_years[0]} to {selected_years[1]}. "
    "Statistics are based on the available dataset records."
)

st.write("")


# ==================================================
# 10. DASHBOARD TABS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Launch Analysis",
    "Orbital Analysis",
    "Data Explorer"
])


# ---------------- TAB 1: OVERVIEW ----------------

with tab1:

    section(
        "Space Exploration Overview",
        "How launch activity changed over time."
    )

    yearly_launches = (
        filtered_launches
        .groupby("launch_year")
        .size()
        .reset_index(name="launch_count")
        .sort_values("launch_year")
    )

    peak_row = yearly_launches.loc[yearly_launches["launch_count"].idxmax()]
    last_year = int(yearly_launches["launch_year"].max())
    recent_cut = last_year - 9
    recent_launches = int(
        yearly_launches.loc[
            yearly_launches["launch_year"] >= recent_cut, "launch_count"
        ].sum()
    )

    yearly_plot = pd.DataFrame({
        "year": year_to_date(yearly_launches["launch_year"]),
        "launches": yearly_launches["launch_count"].values
    })

    native_card(
        "Rocket Launches Over the Years",
        lambda: vl_chart(yearly_plot, area_spec(380)),
        note=(
            f"Launch activity peaked in <b>{int(peak_row['launch_year'])}</b> "
            f"with <b>{int(peak_row['launch_count']):,}</b> launches. "
            f"The last 10 years ({recent_cut}-{last_year}) account for "
            f"<b>{pct(recent_launches, total_launches):.0f}%</b> of all launches "
            "in this selection, so activity is concentrated in the recent era. "
            "The latest year in the dataset may be incomplete."
        )
    )

    left, right = st.columns(2)

    with left:

        outcome_counts = filtered_launches["launch_outcome"].value_counts()
        failed = total_launches - successful_launches

        bar_card(
            "Rocket Launch Outcomes",
            outcome_counts.index,
            outcome_counts.values,
            note=(
                f"<b>{success_rate:.1f}%</b> of launches succeeded "
                f"({successful_launches:,} out of {total_launches:,}). "
                f"The remaining <b>{failed:,}</b> were failures or partial failures, "
                "which shows that launching to orbit is now mostly reliable."
            )
        )

    with right:

        country_counts = filtered_launches["launch_country"].value_counts().head(10)
        top3_share = pct(country_counts.head(3).sum(), total_launches)

        bar_card(
            "Top 10 Launch Countries",
            country_counts.index,
            country_counts.values,
            note=(
                f"<b>{esc(country_counts.index[0])}</b> leads with "
                f"<b>{int(country_counts.iloc[0]):,}</b> launches "
                f"({pct(country_counts.iloc[0], total_launches):.0f}% of the total). "
                f"The top 3 countries together make up <b>{top3_share:.0f}%</b> "
                "of launches, so spaceflight is concentrated in a few nations."
            )
        )

    sat_per_year = (
        filtered_satellites
        .dropna(subset=["launch_year"])
        .groupby("launch_year")
        .size()
        .reset_index(name="satellite_count")
    )

    if not sat_per_year.empty:

        sat_peak = sat_per_year.loc[sat_per_year["satellite_count"].idxmax()]
        last5 = int(
            sat_per_year.loc[
                sat_per_year["launch_year"] >= sat_per_year["launch_year"].max() - 4,
                "satellite_count"
            ].sum()
        )

        sat_plot = pd.DataFrame({
            "year": year_to_date(sat_per_year["launch_year"]),
            "satellites": sat_per_year["satellite_count"].values
        })

        native_card(
            "Satellites Launched per Year",
            lambda: vl_chart(sat_plot, year_bar_spec(340)),
            note=(
                f"The most satellites were launched in <b>{int(sat_peak['launch_year'])}</b> "
                f"(<b>{int(sat_peak['satellite_count']):,}</b>). "
                f"The last 5 years alone represent "
                f"<b>{pct(last5, total_satellites):.0f}%</b> of every satellite in "
                "this selection, a sign of the recent boom in satellite constellations."
            )
        )


# ---------------- TAB 2: LAUNCH ANALYSIS ----------------

with tab2:

    section(
        "Rocket Launch Analysis",
        "Who launches the most, into which orbits, and how reliable it is."
    )

    top_organizations = filtered_launches["launch_organization"].value_counts().head(10)
    top3_org_share = pct(top_organizations.head(3).sum(), total_launches)

    bar_card(
        "Top 10 Rocket Launch Organizations",
        top_organizations.index,
        top_organizations.values,
        note=(
            f"<b>{esc(top_organizations.index[0])}</b> is the most active organization "
            f"with <b>{int(top_organizations.iloc[0]):,}</b> launches "
            f"({pct(top_organizations.iloc[0], total_launches):.0f}% of all launches). "
            f"The top 3 organizations account for <b>{top3_org_share:.0f}%</b>, "
            "which reflects how long state programs dominated spaceflight."
        )
    )

    left, right = st.columns(2)

    with left:

        orbit_counts = filtered_launches["launch_orbit_category"].value_counts().head(10)

        bar_card(
            "Most Common Orbit Categories",
            orbit_counts.index,
            orbit_counts.values,
            note=(
                f"<b>{esc(orbit_counts.index[0])}</b> is the most common destination "
                f"with <b>{int(orbit_counts.iloc[0]):,}</b> launches "
                f"(<b>{pct(orbit_counts.iloc[0], total_launches):.0f}%</b>). "
                "Most missions target near-Earth orbits because they are cheaper "
                "and easier to reach."
            )
        )

    with right:

        type_counts = filtered_launches["launch_organization_type"].value_counts()

        bar_card(
            "Launches by Organization Type",
            type_counts.index,
            type_counts.values,
            note=(
                f"<b>{esc(type_counts.index[0]).capitalize()}</b> organizations performed "
                f"<b>{pct(type_counts.iloc[0], total_launches):.0f}%</b> of the launches. "
                "Use the year slider to see how commercial launches grow in "
                "the recent years."
            )
        )

    # ---- success rate by decade ----
    decade_df = filtered_launches.dropna(subset=["launch_year"]).copy()
    decade_df["decade"] = (decade_df["launch_year"] // 10 * 10).astype(int)
    decade_df["is_success"] = (
        decade_df["launch_outcome"].astype(str).str.lower().eq("success")
    )

    decade_rate = (
        decade_df.groupby("decade")
        .agg(success_rate=("is_success", "mean"), launches=("is_success", "size"))
        .reset_index()
    )
    decade_rate["success_rate"] = decade_rate["success_rate"] * 100

    first = decade_rate.iloc[0]
    last = decade_rate.iloc[-1]

    if len(decade_rate) > 1:
        decade_note = (
            f"The success rate moved from <b>{first['success_rate']:.0f}%</b> in the "
            f"{int(first['decade'])}s ({int(first['launches']):,} launches) to "
            f"<b>{last['success_rate']:.0f}%</b> in the {int(last['decade'])}s "
            f"({int(last['launches']):,} launches). Early decades have fewer launches, "
            "so their rates are less stable."
        )
    else:
        decade_note = (
            f"Only the {int(first['decade'])}s are in the selection, with a success "
            f"rate of <b>{first['success_rate']:.0f}%</b>."
        )

    bar_card(
        "Launch Success Rate by Decade",
        [f"{int(d)}s ({int(n):,} launches)" for d, n in zip(decade_rate["decade"], decade_rate["launches"])],
        decade_rate["success_rate"],
        note=decade_note,
        value_fmt=lambda v: f"{v:.0f}%",
        max_value=100
    )


# ---------------- TAB 3: ORBITAL ANALYSIS ----------------

with tab3:

    section(
        "Satellite Orbital Analysis",
        "Altitude, period, inclination, and how orbital values relate."
    )

    hide_outliers = st.checkbox(
        "Hide extreme deep-space outliers (above 100,000 km)",
        value=False,
        help="A few satellites are far beyond Earth orbit and stretch every chart. "
             "Tick this box to focus on Earth orbits."
    )

    orb_sat = filtered_satellites.copy()

    if hide_outliers:
        orb_sat = orb_sat[~(orb_sat["highest_orbital_altitude_km"] > 100000)]

    orbital_data = orb_sat.dropna(
        subset=["highest_orbital_altitude_km", "orbital_period_minutes"]
    ).copy()

    orbital_data = orbital_data[
        (orbital_data["highest_orbital_altitude_km"] > 0)
        & (orbital_data["orbital_period_minutes"] > 0)
    ]

    if orbital_data.empty:

        st.info("No orbital data matches the filters.")

    else:

        # Spearman = Pearson on ranks (no scipy needed)
        rho = orbital_data["highest_orbital_altitude_km"].rank().corr(
            orbital_data["orbital_period_minutes"].rank()
        )

        plot_df = pd.DataFrame({
            "altitude": orbital_data["highest_orbital_altitude_km"].values,
            "period": orbital_data["orbital_period_minutes"].values,
            "name": orbital_data["satellite_name"].astype(str).values
        })

        if len(plot_df) > 8000:
            plot_df = plot_df.sample(8000, random_state=1)

        native_card(
            "Orbital Altitude vs Orbital Period",
            lambda: vl_chart(plot_df, scatter_spec(430)),
            note=(
                f"Higher orbits take longer to complete one revolution: the rank "
                f"correlation is <b>{rho:.2f}</b> across "
                f"<b>{len(orbital_data):,}</b> satellites. Both axes use a log scale "
                "so the dense near-Earth cluster and the rare deep-space "
                "satellites can be seen together. Hover over a point to see the "
                "satellite name, and scroll to zoom. The chart shows a random "
                "sample of up to 8,000 points."
            )
        )

    left, right = st.columns(2)

    with left:

        period_s = orb_sat["orbital_period_minutes"]
        period_s = period_s[period_s > 0]

        period_bins = bin_counts(
            period_s,
            [0, 90, 100, 130, 700, 1500, float("inf")],
            ["Under 90 min", "90-100 min", "100-130 min",
             "130-700 min", "700-1,500 min (GEO zone)", "Over 1,500 min"]
        )

        if period_s.empty:
            period_note = None
        else:
            leo_share = pct((period_s <= 128).sum(), len(period_s))
            period_note = (
                f"The typical (median) satellite circles the Earth in "
                f"<b>{period_s.median():,.1f} minutes</b>, and <b>{leo_share:.0f}%</b> "
                "complete an orbit in under about 2 hours, which is the "
                "low-Earth-orbit range."
            )

        bar_card(
            "Distribution of Orbital Periods",
            period_bins.index,
            period_bins.values,
            note=period_note
        )

    with right:

        alt_s = orb_sat["highest_orbital_altitude_km"]
        alt_s = alt_s[alt_s > 0]

        alt_bins = bin_counts(
            alt_s,
            [0, 500, 1000, 2000, 10000, 36000, float("inf")],
            ["Under 500 km", "500-1,000 km", "1,000-2,000 km",
             "2,000-10,000 km", "10,000-36,000 km", "Over 36,000 km"]
        )

        if alt_s.empty:
            alt_note = None
        else:
            alt_note = (
                f"Half of the satellites have a highest altitude below "
                f"<b>{alt_s.median():,.0f} km</b>, and 95% are below "
                f"<b>{alt_s.quantile(0.95):,.0f} km</b>. The maximum reaches "
                f"<b>{alt_s.max():,.0f} km</b>; these extreme values are real "
                "high-altitude or deep-space missions, not errors."
            )

        bar_card(
            "Distribution of Orbital Altitudes",
            alt_bins.index,
            alt_bins.values,
            note=alt_note
        )

    left, right = st.columns(2)

    with left:

        inc_s = orb_sat["orbital_inclination_degrees"].dropna()

        inc_bins = bin_counts(
            inc_s,
            [0, 30, 60, 90, 100, 181],
            ["0-30 deg", "30-60 deg", "60-90 deg", "90-100 deg (polar)", "Over 100 deg"]
        )

        if inc_s.empty:
            inc_note = None
        else:
            mode_inc = inc_s.round(0).mode().iloc[0]
            mode_share = pct((inc_s.round(0) == mode_inc).sum(), len(inc_s))
            extra = ""
            if 96 <= mode_inc <= 99:
                extra = " This is typical of sun-synchronous (polar) orbits."
            elif 50 <= mode_inc <= 55:
                extra = " This is common for large low-orbit satellite constellations."
            inc_note = (
                f"The most common single inclination is about <b>{mode_inc:.0f} deg</b> "
                f"(<b>{mode_share:.0f}%</b> of satellites).{extra} "
                "Inclination describes how tilted the orbit is relative to the equator."
            )

        bar_card(
            "Distribution of Orbital Inclination",
            inc_bins.index,
            inc_bins.values,
            note=inc_note
        )

    with right:

        if orbital_data.empty:

            st.info("Not enough orbital data to compare orbit types.")

        else:

            type_med = (
                orbital_data.groupby("launch_orbit_category")["highest_orbital_altitude_km"]
                .agg(["median", "size"])
            )
            type_med = type_med[type_med["size"] >= 5].sort_values("median", ascending=False).head(8)

            if type_med.empty:

                st.info("Not enough orbital data to compare orbit types.")

            else:

                bar_card(
                    "Median Altitude by Orbit Type (km)",
                    [f"{o} ({int(n):,} sats)" for o, n in zip(type_med.index, type_med["size"])],
                    type_med["median"].values,
                    note=(
                        f"Orbit types separate clearly by altitude: "
                        f"<b>{esc(type_med.index[0])}</b> has the highest median altitude "
                        f"(<b>{type_med['median'].iloc[0]:,.0f} km</b>) and "
                        f"<b>{esc(type_med.index[-1])}</b> the lowest "
                        f"(<b>{type_med['median'].iloc[-1]:,.0f} km</b>)."
                    ),
                    value_fmt=lambda v: f"{v:,.0f}"
                )

    section(
        "Correlation Between Orbital Characteristics",
        "Linear relationship between the numeric orbital columns."
    )

    numeric_columns = [
        "orbital_period_minutes",
        "orbital_inclination_degrees",
        "highest_orbital_altitude_km",
        "lowest_orbital_altitude_km"
    ]

    corr = orb_sat[numeric_columns].corr()

    labels = ["Orbital Period", "Inclination", "Highest Altitude", "Lowest Altitude"]

    if corr.notna().any().any():

        head = "<tr><th></th>" + "".join(f"<th>{l}</th>" for l in labels) + "</tr>"
        body = ""

        for i, row_label in enumerate(labels):

            body += f'<tr><td class="rowlabel">{row_label}</td>'

            for j in range(len(labels)):

                v = corr.iloc[i, j]

                if pd.isna(v):
                    body += '<td style="background:rgba(255,255,255,0.05)">-</td>'
                    continue

                if v >= 0:
                    color = f"rgba(255, 133, 146, {0.12 + abs(v) * 0.78:.2f})"
                else:
                    color = f"rgba(122, 162, 255, {0.12 + abs(v) * 0.70:.2f})"

                body += f'<td style="background:{color}">{v:.2f}</td>'

            body += "</tr>"

        best_pair, best_val = None, 0.0
        for i in range(len(numeric_columns)):
            for j in range(i + 1, len(numeric_columns)):
                v = corr.iloc[i, j]
                if pd.notna(v) and abs(v) > abs(best_val):
                    best_pair, best_val = (labels[i], labels[j]), v

        if best_pair:
            direction = "positive" if best_val > 0 else "negative"
            heat_note = (
                f"The strongest relationship is between <b>{best_pair[0]}</b> and "
                f"<b>{best_pair[1]}</b> (<b>{best_val:.2f}</b>, {direction}). "
                "Values close to 1 or -1 mean a strong linear link, values near 0 "
                "mean almost none. Pink = positive, blue = negative. A few extreme "
                "satellites can inflate this number, so tick the outlier box above to compare."
            )
        else:
            heat_note = None

        with st.container(border=True):

            chart_title("Correlation Heatmap")

            st.markdown(
                f'<table class="heat">{head}{body}</table>',
                unsafe_allow_html=True
            )

            if heat_note:
                insight_box(heat_note)

    else:

        st.info("Not enough orbital data to calculate correlations.")


# ---------------- TAB 4: DATA EXPLORER ----------------

with tab4:

    section(
        "Data Explorer",
        "A plain-language profile of the data behind the dashboard."
    )

    dataset_choice = st.radio(
        "Select Dataset",
        ["Rocket Launches", "Satellites", "Merged Dataset"],
        horizontal=True
    )

    if dataset_choice == "Rocket Launches":
        selected_data = filtered_launches
    elif dataset_choice == "Satellites":
        selected_data = filtered_satellites
    else:
        selected_data = filtered_df

    # ---------- Data story ----------
    n_rows, n_cols = selected_data.shape

    if dataset_choice == "Rocket Launches":

        story = (
            f"This view contains <b>{n_rows:,} launches</b> between "
            f"<b>{selected_years[0]}</b> and <b>{selected_years[1]}</b>. "
            f"They were carried out by <b>{filtered_launches['launch_organization'].nunique():,}</b> "
            f"organizations from <b>{filtered_launches['launch_site'].nunique():,}</b> "
            f"launch sites in <b>{total_countries:,}</b> countries. "
            f"<b>{success_rate:.1f}%</b> of them were successful, and the most "
            f"common destination was <b>{esc(filtered_launches['launch_orbit_category'].mode().iloc[0])}</b>. "
            f"Each launch is one record described by <b>{n_cols}</b> fields."
        )

    elif dataset_choice == "Satellites":

        top_user = selected_data["satellite_user_type"].mode()
        top_user_txt = esc(top_user.iloc[0]) if not top_user.empty else "n/a"

        story = (
            f"This view contains <b>{n_rows:,} unique satellites</b> launched "
            f"between <b>{selected_years[0]}</b> and <b>{selected_years[1]}</b>, "
            f"operated by <b>{selected_data['satellite_operator'].nunique():,}</b> "
            f"different operators. The most common user type is <b>{top_user_txt}</b>. "
            f"Orbital measurements (period, inclination, altitude) are available "
            f"for <b>{pct(selected_data['orbital_period_minutes'].notna().sum(), n_rows):.0f}%</b> "
            f"of the satellites. Each satellite is one record described by <b>{n_cols}</b> fields."
        )

    else:

        story = (
            f"The merged dataset joins launch records with satellite records "
            f"using <b>launch_id</b>. It has <b>{n_rows:,} rows</b> and "
            f"<b>{n_cols}</b> columns, covering <b>{total_launches:,}</b> launches and "
            f"<b>{total_satellites:,}</b> satellites. One launch can carry many "
            "satellites, so a launch can appear in several rows; that is why the "
            "dashboard analyzes launches and satellites from their own de-duplicated "
            "versions instead of this merged table."
        )

    st.markdown(f'<div class="story">{story}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    c1.metric("Records", f"{n_rows:,}")
    c2.metric("Fields", f"{n_cols}")
    c3.metric(
        "Overall Completeness",
        f"{(1 - selected_data.isnull().sum().sum() / max(selected_data.size, 1)) * 100:.1f}%"
    )

    # ---------- Sample records as cards ----------
    section(
        "Sample Records",
        "A readable look at individual records instead of raw rows and columns."
    )

    sample_mode = st.radio(
        "Show",
        ["Most recent", "Earliest", "Random sample"],
        horizontal=True,
        key="sample_mode"
    )

    # always built from launches or satellites, never the duplicated merged table
    base_for_cards = filtered_satellites if dataset_choice == "Satellites" else filtered_launches
    ordered = base_for_cards.sort_values("rocket_launch_date_utc")

    if sample_mode == "Most recent":
        sample = ordered.tail(6).iloc[::-1]
    elif sample_mode == "Earliest":
        sample = ordered.head(6)
    else:
        sample = ordered.sample(n=min(6, len(ordered)), random_state=7)

    def badge(outcome):
        o = str(outcome).lower()
        if o == "success":
            return f'<span class="badge badge-success">{esc(outcome).upper()}</span>'
        if o == "failure":
            return f'<span class="badge badge-failure">{esc(outcome).upper()}</span>'
        if "partial" in o:
            return f'<span class="badge badge-partial">{esc(outcome).upper()}</span>'
        return f'<span class="badge badge-other">{esc(outcome).upper()}</span>'

    cards = []

    for _, r in sample.iterrows():

        date_txt = (
            r["rocket_launch_date_utc"].strftime("%d %b %Y, %H:%M UTC")
            if pd.notna(r["rocket_launch_date_utc"]) else "Unknown date"
        )

        if dataset_choice == "Satellites":

            title = esc(r.get("satellite_name", "Unnamed satellite"))
            period = r.get("orbital_period_minutes")
            alt = r.get("highest_orbital_altitude_km")
            body = (
                f"Operated by <b>{esc(r.get('satellite_operator', 'Unknown'))}</b> "
                f"({esc(r.get('satellite_user_type', 'n/a'))} use).<br>"
                f"Launched by <b>{esc(r['launch_organization'])}</b> from "
                f"<b>{esc(r['launch_country'])}</b>.<br>"
                f"Orbit: <b>{esc(r['launch_orbit_category'])}</b>, "
                f"period <b>{fmt(period)} min</b>, "
                f"highest altitude <b>{fmt(alt)} km</b>."
            )

        else:

            title = esc(r["mission_name"])
            body = (
                f"<b>{esc(r['launch_organization'])}</b> launched a "
                f"<b>{esc(r['satellite_record_rocket_name'])}</b> rocket from "
                f"<b>{esc(r['launch_site'])}</b>, {esc(r['launch_country'])}.<br>"
                f"Destination orbit: <b>{esc(r['launch_orbit_category'])}</b> · "
                f"Payloads catalogued: <b>{int(r['catalogued_payload_count'])}</b>."
            )

        cards.append(
            '<div class="record">'
            f'<div class="record-date">{date_txt.upper()}</div>'
            f'<div class="record-title">{title}</div>'
            f'<div class="record-line">{body}</div>'
            f'{badge(r["launch_outcome"])}'
            '</div>'
        )

    st.markdown(
        '<div class="record-grid">' + "".join(cards) + "</div>",
        unsafe_allow_html=True
    )

    with st.expander("Show the raw table (first 300 rows)"):
        show_table(selected_data, max_rows=300)

    with st.expander("Column guide: what each field means"):

        guide = {
            "Launch": [
                ("rocket_launch_date_utc", "Date and time of the launch (UTC)"),
                ("launch_organization", "Organization that ran the launch"),
                ("launch_country", "Country of the launch site"),
                ("launch_site / launch_pad", "Where the rocket lifted off"),
                ("launch_outcome", "Success, failure, or partial failure"),
                ("launch_orbit_category", "Target orbit of the mission (LEO, GEO, SSO, ...)"),
                ("catalogued_payload_count", "Number of payloads catalogued for the launch"),
            ],
            "Satellite": [
                ("satellite_name / satellite_norad_id", "Satellite name and its unique NORAD catalogue ID"),
                ("satellite_operator / operator_group", "Who operates the satellite"),
                ("satellite_user_type", "Civil, commercial, government or military use"),
                ("satellite_launch_date / decay_date", "When it was launched and when it re-entered"),
            ],
            "Orbit": [
                ("orbital_period_minutes", "Time to complete one orbit"),
                ("orbital_inclination_degrees", "Tilt of the orbit relative to the equator"),
                ("highest_orbital_altitude_km", "Highest point of the orbit (apogee)"),
                ("lowest_orbital_altitude_km", "Lowest point of the orbit (perigee)"),
            ],
        }

        for group, items in guide.items():
            st.markdown(f"**{group}**")
            for name, desc in items:
                st.markdown(f"- `{name}`: {desc}")

    # ---------- Completeness ----------
    section(
        "Data Completeness",
        "How much of each field is filled in."
    )

    missing_pct = selected_data.isnull().mean() * 100
    missing_pct = missing_pct[missing_pct > 0].sort_values()

    if missing_pct.empty:

        insight_box("Every field is <b>fully complete</b> in this dataset.")

    else:

        complete_cols = n_cols - len(missing_pct)
        worst = missing_pct.index[-1]

        bar_card(
            "Missing Values by Field (%)",
            list(missing_pct.index[::-1]),
            list(missing_pct.values[::-1]),
            note=(
                f"<b>{complete_cols}</b> of {n_cols} fields are fully complete. "
                f"The emptiest field is <b>{esc(worst)}</b> "
                f"(<b>{missing_pct.iloc[-1]:.1f}%</b> missing). "
                "Missing orbital values are mostly satellites with withheld or "
                "unavailable orbit data."
            ),
            value_fmt=lambda v: f"{v:.1f}%",
            max_value=100
        )

    # ---------- Summary statistics ----------
    section(
        "Summary Statistics",
        "Computed on the right level: launches for launch data, unique satellites for orbit data."
    )

    st.markdown("**Orbital characteristics** (one row per unique satellite)")

    orbit_spec = {
        "orbital_period_minutes": ("Orbital Period", "min"),
        "orbital_inclination_degrees": ("Inclination", "deg"),
        "highest_orbital_altitude_km": ("Highest Altitude", "km"),
        "lowest_orbital_altitude_km": ("Lowest Altitude", "km"),
    }

    def describe_table(frame, spec):

        rows = []

        for col, (label, unit) in spec.items():

            s = frame[col].dropna()

            if s.empty:
                continue

            rows.append({
                "Variable": f"{label} ({unit})" if unit else label,
                "Count": f"{len(s):,}",
                "Mean": fmt(s.mean()),
                "Median": fmt(s.median()),
                "Std Dev": fmt(s.std()),
                "Min": fmt(s.min()),
                "25%": fmt(s.quantile(0.25)),
                "75%": fmt(s.quantile(0.75)),
                "Max": fmt(s.max()),
            })

        return pd.DataFrame(rows)

    orbit_stats = describe_table(filtered_satellites, orbit_spec)

    if orbit_stats.empty:

        st.info("No orbital measurements are available for this selection.")

    else:

        show_table(orbit_stats)

        skew_lines = []

        for col, (label, unit) in orbit_spec.items():
            s = filtered_satellites[col].dropna()
            if len(s) > 1 and s.median() > 0 and s.mean() > 2 * s.median():
                skew_lines.append(
                    f"<b>{label}</b>: mean {fmt(s.mean())} {unit} is "
                    f"{s.mean() / s.median():.1f}x the median {fmt(s.median())} {unit}"
                )

        if skew_lines:
            insight_box(
                "For these variables the <b>median</b> describes a typical "
                "satellite better than the mean, because a few extreme values "
                "pull the mean upward (right-skewed data):<br>"
                + "<br>".join(skew_lines)
            )
        else:
            insight_box(
                "Mean and median are close for the orbital variables, so the "
                "distributions are fairly balanced in this selection."
            )

    st.markdown("**Launch characteristics** (one row per unique launch)")

    launch_spec = {
        "catalogued_payload_count": ("Payloads per Launch", ""),
        "launch_year": ("Launch Year", ""),
    }

    launch_stats = describe_table(filtered_launches, launch_spec)

    if not launch_stats.empty:

        # years should not have thousands separators
        for col in ["Mean", "Median", "Std Dev", "Min", "25%", "75%", "Max"]:
            launch_stats.loc[launch_stats["Variable"] == "Launch Year", col] = (
                launch_stats.loc[launch_stats["Variable"] == "Launch Year", col]
                .str.replace(",", "", regex=False)
            )

        show_table(launch_stats)

        payload = filtered_launches["catalogued_payload_count"]

        insight_box(
            f"A typical launch carries <b>{payload.median():,.0f}</b> catalogued "
            f"payloads (median), but the average is <b>{payload.mean():,.1f}</b> "
            f"and the largest launch carried <b>{payload.max():,.0f}</b>. "
            "Big constellation launches create this long tail."
        )

    st.markdown("**Categorical fields**")

    cat_rows = []

    cat_spec = [
        (filtered_launches, "launch_organization", "Launch Organization"),
        (filtered_launches, "launch_country", "Launch Country"),
        (filtered_launches, "launch_site", "Launch Site"),
        (filtered_launches, "launch_outcome", "Launch Outcome"),
        (filtered_launches, "launch_orbit_category", "Orbit Category"),
        (filtered_satellites, "satellite_user_type", "Satellite User Type"),
        (filtered_satellites, "satellite_operator", "Satellite Operator"),
    ]

    for frame, col, label in cat_spec:

        if col not in frame.columns:
            continue

        counts = frame[col].dropna().astype(str).value_counts()

        if counts.empty:
            continue

        cat_rows.append({
            "Field": label,
            "Unique Values": f"{len(counts):,}",
            "Most Frequent": counts.index[0],
            "Records": f"{counts.iloc[0]:,}",
            "Share": f"{pct(counts.iloc[0], counts.sum()):.1f}%",
        })

    if cat_rows:
        show_table(pd.DataFrame(cat_rows))

    st.download_button(
        label="Download Filtered Dataset",
        data=selected_data.to_csv(index=False).encode("utf-8-sig"),
        file_name="orbital_atlas_filtered.csv",
        mime="text/csv"
    )


# ==================================================
# 11. ANALYSIS HIGHLIGHTS
# ==================================================

st.divider()

section("Analysis Highlights", "Quick facts from the current selection.")

yearly_counts = filtered_launches.groupby("launch_year").size()
organization_counts = filtered_launches["launch_organization"].value_counts()

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("Peak Launch Year")

        if not yearly_counts.empty:

            st.metric("Recorded Launches", f"{int(yearly_counts.max()):,}")
            st.caption(f"Year: {int(yearly_counts.idxmax())}")

with col2:

    with st.container(border=True):

        st.subheader("Most Active Organization")

        if not organization_counts.empty:

            st.write(organization_counts.index[0])
            st.metric("Recorded Launches", f"{int(organization_counts.iloc[0]):,}")

with st.container(border=True):

    st.subheader("Orbital Science Insight")

    valid_orbits = filtered_satellites[
        ["highest_orbital_altitude_km", "orbital_period_minutes"]
    ].dropna()

    if len(valid_orbits) >= 2:

        correlation = valid_orbits["highest_orbital_altitude_km"].corr(
            valid_orbits["orbital_period_minutes"]
        )

        if pd.notna(correlation):

            st.metric("Altitude–Period Correlation", f"{correlation:.2f}")

            st.write(
                "This value describes the linear relationship between the "
                "highest orbital altitude and the orbital period in the "
                "filtered data. By Kepler's third law, a higher orbit always "
                "means a longer period."
            )

        else:
            st.info("Correlation is unavailable for this selection.")

    else:
        st.info("Not enough orbital data for this insight.")

with st.container(border=True):

    st.subheader("Key Findings")

    takeaways = [
        f"**{total_launches:,}** launches and **{total_satellites:,}** satellites "
        f"are recorded between {selected_years[0]} and {selected_years[1]}.",
        f"Launch reliability is high: **{success_rate:.1f}%** of launches succeeded.",
    ]

    if not organization_counts.empty:
        takeaways.append(
            f"**{organization_counts.index[0]}** is the most active organization "
            f"({pct(organization_counts.iloc[0], total_launches):.0f}% of launches)."
        )

    if not yearly_counts.empty:
        takeaways.append(
            f"Launch activity peaked in **{int(yearly_counts.idxmax())}** "
            f"with {int(yearly_counts.max()):,} launches."
        )

    if len(valid_orbits) >= 2:
        takeaways.append(
            f"Half of all satellites orbit below "
            f"**{valid_orbits['highest_orbital_altitude_km'].median():,.0f} km**, "
            "so most satellites live in low Earth orbit."
        )

    for item in takeaways:
        st.markdown(f"- {item}")


# ==================================================
# 12. FOOTER
# ==================================================

st.divider()

st.caption("ORBITAL ATLAS | SPACE ROCKETS & SATELLITE LAUNCHES")
