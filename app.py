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
    h1, h2, h3 {
        color: #1a73e8;
        font-family: 'Helvetica Neue', sans-serif;
    }
    section[data-testid="stSidebar"] div.stSlider > div,
    section[data-testid="stSidebar"] .stMultiSelect > div,
    section[data-testid="stSidebar"] .stSelectbox > div,
    section[data-testid="stSidebar"] .stTextInput > div {
        background-color: #ccece6;
        border-radius: 5px;
        padding: 6px;
        border: 2px solid #fc8d62;
    }
    section[data-testid="stSidebar"] .stMultiSelect span,
    section[data-testid="stSidebar"] .stSelectbox span {
        background-color: #66c2a5 !important;
        color: white !important;
    }
    .stSlider > div > div > div:nth-child(1) > div {
        background: #fc8d62 !important;
    }
    .stSlider [role="slider"] {
        background-color: #fc8d62 !important;
        border: 1px solid #fc8d62 !important;
    }
    input[type="range"]::-webkit-slider-runnable-track {
        background: #fc8d62 !important;
    }
    input[type="range"]::-moz-range-track {
        background: #fc8d62 !important;
    }
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
            <div style='padding-top: 30px;'>
                <h1 style='font-size: 42px;'>Sleep Health & Lifestyle Factors</h1>
                <h3 style='font-size: 24px;'>MSBA 382 — Healthcare Analytics Project</h3>
                <p style='font-size: 17px; max-width: 600px; color: black;'>
                    Welcome to this interactive dashboard exploring how lifestyle habits such as
                    alcohol consumption, caffeine intake, smoking, and physical activity influence
                    sleep efficiency and duration.
                </p>
            </div>
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
gender_filter = st.sidebar.multiselect("👤 Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
age_range = st.sidebar.slider("🎂 Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))
alcohol_filter = st.sidebar.multiselect("🍷 Alcohol Consumption", df["Alcohol consumption"].unique(), default=df["Alcohol consumption"].unique())
exercise_range = st.sidebar.slider("🏃 Exercise Frequency", int(df["Exercise frequency"].min()), int(df["Exercise frequency"].max()), (0, 7))
smoking_filter = st.sidebar.multiselect("🚬 Smoking Status", df["Smoking status"].unique(), default=df["Smoking status"].unique())
caffeine_range = st.sidebar.slider("☕ Caffeine Consumption", float(df["Caffeine consumption"].min()), float(df["Caffeine consumption"].max()), (0.0, 300.0))

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



