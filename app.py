import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Sleep Health Dashboard", layout="wide")

# --- Apply seaborn theme and color palette globally ---
sns.set_theme(style="whitegrid")
sns.set_palette(["#66c2a5", "#fc8d62"])  # Two-tone aesthetic colors

# --- Custom CSS styling for consistent visual theme across filters, sliders, KPIs, login ---
st.markdown("""
<style>
html, body, .main, .block-container, .stApp, section.main {
    background-color: #1f2937 !important;
    color: #ffffff !important;
}

/* Global font and text color */
body, p, h1, h2, h3, h4, h5, h6, label, span, div {
    color: #ffffff !important;
    font-family: 'Helvetica Neue', sans-serif;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #1f2937 !important;
    color: #ffffff !important;
}

/* Sidebar widgets */
section[data-testid="stSidebar"] div.stSlider > div,
section[data-testid="stSidebar"] .stMultiSelect > div,
section[data-testid="stSidebar"] .stSelectbox > div,
section[data-testid="stSidebar"] .stTextInput > div {
    background-color: #ccece6;
    border-radius: 5px;
    padding: 6px;
    border: 2px solid #fc8d62;
}

/* Pills/tags */
section[data-testid="stSidebar"] .stMultiSelect span,
section[data-testid="stSidebar"] .stSelectbox span {
    background-color: #66c2a5 !important;
    color: white !important;
}

/* Slider styling */
.stSlider > div > div > div:nth-child(1) > div {
    background: #fc8d62 !important;
}
.stSlider [role="slider"] {
    background-color: #fc8d62 !important;
    border: 1px solid #fc8d62 !important;
}
input[type="range"]::-webkit-slider-runnable-track,
input[type="range"]::-moz-range-track {
    background: #fc8d62 !important;
}
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stSlider span,
section[data-testid="stSidebar"] .stSlider div {
    color: #ffffff !important;
}

/* KPI cards */
.metric-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding-bottom: 20px;
}
.metric-box {
    background: linear-gradient(90deg, #66c2a5, #fc8d62);
    border-radius: 8px;
    padding: 20px;
    width: 100%;
    color: white;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.metric-box .value {
    font-size: 26px;
    margin-top: 5px;
}

/* Input focus styling */
input:focus, textarea:focus, select:focus {
    outline: none !important;
    box-shadow: none !important;
}
button[title="Show password"]:focus,
button[title="Hide password"]:focus {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Login page override */
section.main > div:has(.stTextInput) {
    background-color: #1f2937 !important;
    color: white !important;
}
section.main > div:has(.stTextInput) * {
    color: white !important;
}

/* Header and footer dark */
header,
header[data-testid="stHeader"],
footer,
.css-164nlkn, .css-1lcbmhc,
.css-18ni7ap.e8zbici2 {
    background-color: #1f2937 !important;
    color: white !important;
    border: none !important;
    box-shadow: none !important;
}

/* Dataframe background and icon buttons */
.stDataFrame {
    background-color: #1f2937 !important;
    color: white !important;
}
[data-testid="stElementToolbar"],
[data-testid="stElementToolbar"] *,
[data-testid="stToolbar"] svg,
[data-testid="stDownloadButton"] svg,
section.main button[title="Download"] svg,
section.main button[title="Search"] svg,
section.main button[title="Expand"] svg,
button[kind="icon"] svg {
    background-color: transparent !important;
    color: #ffffff !important;
    fill: #ffffff !important;
}
[data-testid="stElementToolbar"] button:hover,
button[kind="icon"]:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px;
}

/* Fix expand (ellipsis "...") hover popup icon and background */
button[kind="icon"] {
    background-color: transparent !important;
    color: #ffffff !important;
    fill: #ffffff !important;
    border-radius: 6px !important;
    border: none !important;
    box-shadow: none !important;
}

/* Fix the hover popup container background */
div[data-testid="stElementToolbar"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Ensure expand/search/download icons inside toolbar stay white */
div[data-testid="stElementToolbar"] svg,
div[data-testid="stElementToolbar"] * {
    fill: #ffffff !important;
    color: #ffffff !important;
}

/* Optional: on hover, show subtle dark tint */
div[data-testid="stElementToolbar"] button:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
}

/* 🔧 FINAL FIX (Streamlit expand button white square + hover icon) */

/* Strong override for the toolbar wrapper */
div[data-testid="stElementToolbar"] {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* Override pseudo-elements (responsible for white box) */
div[data-testid="stElementToolbar"]::before,
div[data-testid="stElementToolbar"]::after {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    content: none !important;
}

/* Fix the actual expand button */
div[data-testid="stElementToolbar"] button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Icon inside button */
div[data-testid="stElementToolbar"] button svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}

/* On hover: no white flash */
div[data-testid="stElementToolbar"] button:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border: none !important;
    box-shadow: none !important;
}

/* Handle internal elements */
div[data-testid="stElementToolbar"] * {
    background: transparent !important;
    color: #ffffff !important;
    fill: #ffffff !important;
    border: none !important;
}

/* 🔥 Target the exact expand button and kill white hover/box */
button.st-emotion-cache-d0v1h0,
button.st-emotion-cache-d0v1h0:hover {
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    outline: none !important;
}

/* Kill any hover effect square */
button.st-emotion-cache-d0v1h0::before,
button.st-emotion-cache-d0v1h0::after {
    background: none !important;
    content: none !important;
    border: none !important;
    box-shadow: none !important;
    display: none !important;
}

/* Make the icon itself white */
button.st-emotion-cache-d0v1h0 svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

.stTooltipHoverTarget {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* 💀 Remove the white hover ghost box for expand icon */
.stTooltipHoverTarget::before,
.stTooltipHoverTarget::after {
    background: transparent !important;
    content: none !important;
    display: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Remove background on tooltip popup itself */
div[data-testid="stTooltipContent"] {
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    color: white !important;
}

/* Hide that floating white square next to expand button */
div[data-testid="stElementToolbar"] > div > div {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* ✅ Fix Streamlit DataFrame toolbar icon buttons (Search, Expand, Download) */
[data-testid="stElementToolbar"] svg,
[data-testid="stElementToolbarButtonIcon"] {
    fill: white !important;
    stroke: white !important;
    color: white !important;
}

/* 🧽 Clean up white box hover or tooltip on these icons */
button[aria-label="Download"],
button[aria-label="Expand"],
button[aria-label="Search"] {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
    outline: none !important;
}

button[aria-label="Download"]:hover,
button[aria-label="Expand"]:hover,
button[aria-label="Search"]:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px !important;
}

/* Kill white box around icons on hover */
button[aria-label="Download"]::before,
button[aria-label="Expand"]::before,
button[aria-label="Search"]::before {
    content: none !important;
    background: none !important;
    display: none !important;
    box-shadow: none !important;
}

<style>
/* Force white color on all Streamlit toolbar icons */
button[kind="icon"] svg,
button[data-testid="stBaseButton-elementToolbar"] svg,
div[data-testid="stElementToolbar"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* Remove white background square */
button[kind="icon"],
button[data-testid="stBaseButton-elementToolbar"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Kill pseudo elements that might cause white box */
button[kind="icon"]::before,
button[kind="icon"]::after,
button[data-testid="stBaseButton-elementToolbar"]::before,
button[data-testid="stBaseButton-elementToolbar"]::after {
    content: none !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    display: none !important;
}

/* Fix on hover */
button[kind="icon"]:hover,
button[data-testid="stBaseButton-elementToolbar"]:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
}

<style>
/* 🔧 Fix remaining white square on expand icon in chart toolbar */
button[title="View fullscreen"],
button[title="Download image"],
button[title="Zoom"],
button[title="Pan"],
button[title="Reset axes"],
button[title="Autoscale"],
button[title="Save as..."],
button[title="Download as CSV"],
div[data-testid="stElementToolbar"] button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Remove any white box from pseudo-elements */
button[title="View fullscreen"]::before,
button[title="View fullscreen"]::after,
div[data-testid="stElementToolbar"] button::before,
div[data-testid="stElementToolbar"] button::after {
    content: none !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Force the expand icon to be white */
button[title="View fullscreen"] svg,
div[data-testid="stElementToolbar"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}
</style>


</style>
""", unsafe_allow_html=True)



# --- Password protection and intro page ---
PASSWORD = "osb2025"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.title("Login")
    password = st.sidebar.text_input("Enter password to access the dashboard", type="password")

    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.markdown("""
            <h1 style='font-size: 42px; color: white;'>Sleep Health & Lifestyle Factors</h1>
            <h3 style='font-size: 24px; color: white;'>MSBA 382 — Healthcare Analytics Project</h3>
            <p style='font-size: 17px; max-width: 600px; color: white;'>
                Welcome to this interactive dashboard exploring how lifestyle habits such as
                alcohol consumption, caffeine intake, smoking, and physical activity influence
                sleep efficiency and duration.
            </p>
        """, unsafe_allow_html=True)

    
    with col2:
        try:
            st.image("cover_page.jpeg", width=400)
        except:
            st.warning("Image not found. Please ensure 'cover_page.jpeg' is in the same folder.")

    if password == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# --- Load data ---
@st.cache_data
def load_data():
    return pd.read_excel("Sleep Efficiency.xlsx")

df = load_data()

# --- Sidebar filters ---
st.sidebar.title("Filters")
gender_filter = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))
alcohol_filter = st.sidebar.multiselect("Alcohol Consumption", df["Alcohol consumption"].unique(), default=df["Alcohol consumption"].unique())
exercise_range = st.sidebar.slider("Exercise Frequency", int(df["Exercise frequency"].min()), int(df["Exercise frequency"].max()), (0, 7))
smoking_filter = st.sidebar.multiselect("Smoking Status", df["Smoking status"].unique(), default=df["Smoking status"].unique())
caffeine_range = st.sidebar.slider("Caffeine Consumption", float(df["Caffeine consumption"].min()), float(df["Caffeine consumption"].max()), (0.0, 300.0))

# --- Page navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Filtered Dataset"])

# --- Apply filters ---
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(*age_range)) &
    (df["Alcohol consumption"].isin(alcohol_filter)) &
    (df["Exercise frequency"].between(*exercise_range)) &
    (df["Smoking status"].isin(smoking_filter)) &
    (df["Caffeine consumption"].between(*caffeine_range))
]

# --- Dashboard Page ---
if page == "Dashboard":
    st.title("Sleep Health Dashboard")
    st.markdown("Analyze how lifestyle factors (alcohol, caffeine, smoking, exercise, age, gender) influence sleep quality.")

    # KPI Section
    st.markdown("""
        <div class="metric-container">
            <div class="metric-box">
                🌙 Avg Sleep Efficiency (%)<div class="value">{:.2f}</div>
            </div>
            <div class="metric-box">
                ⏱ Avg Sleep Duration (hrs)<div class="value">{:.2f}</div>
            </div>
            <div class="metric-box">
                ☕ Avg Caffeine (mg)<div class="value">{:.0f}</div>
            </div>
        </div>
    """.format(
        filtered_df['Sleep efficiency'].mean(),
        filtered_df['Sleep duration'].mean(),
        filtered_df['Caffeine consumption'].mean()
    ), unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        st.markdown("**Sleep Efficiency by Alcohol Consumption**")
        fig, ax = plt.subplots()
        sns.barplot(x="Alcohol consumption", y="Sleep efficiency", hue="Gender", data=filtered_df, ax=ax)
        st.pyplot(fig)

    with cols[1]:
        st.markdown("**Sleep Efficiency by Smoking Status**")
        fig, ax = plt.subplots()
        sns.barplot(x="Smoking status", y="Sleep efficiency", hue="Gender", data=filtered_df, ax=ax)
        st.pyplot(fig)

    with cols[2]:
        st.markdown("**Sleep Efficiency by Gender**")
        fig, ax = plt.subplots()
        sns.barplot(x="Gender", y="Sleep efficiency", hue="Gender", data=filtered_df, ax=ax, dodge=False)
        st.pyplot(fig)

    cols = st.columns(3)
    with cols[0]:
        st.markdown("**REM Sleep % vs Caffeine Consumption**")
        fig, ax = plt.subplots()
        sns.scatterplot(x="Caffeine consumption", y="REM sleep percentage", hue="Gender", data=filtered_df, ax=ax)
        st.pyplot(fig)

    with cols[1]:
        st.markdown("**Sleep Duration**")
        fig, ax = plt.subplots()
        sns.boxplot(x="Gender", y="Sleep duration", data=filtered_df, ax=ax, hue="Gender")
        st.pyplot(fig)

    with cols[2]:
        st.markdown("**Exercise Frequency Distribution**")
        fig, ax = plt.subplots()
        sns.countplot(x="Exercise frequency", hue="Gender", data=filtered_df, ax=ax)
        st.pyplot(fig)

# --- Filtered Dataset Page ---
elif page == "Filtered Dataset":
    st.title("Filtered Dataset Preview")
    st.dataframe(filtered_df, use_container_width=True)




