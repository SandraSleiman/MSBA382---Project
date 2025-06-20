import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Sleep Health Dashboard", layout="wide")

# --- Apply seaborn theme and color palette globally ---
sns.set_theme(style="whitegrid")
sns.set_palette(["#66c2a5", "#fc8d62"])  # Two-tone aesthetic colors

# --- Custom CSS for icons only (no dark mode overrides) ---
st.markdown("""
<style>
/* --- Icon Toolbar Fixes Only --- */

[data-testid="stElementToolbar"] svg,
[data-testid="stElementToolbarButtonIcon"] {
    fill: white !important;
    stroke: white !important;
    color: white !important;
}

[data-testid="stElementToolbar"] button,
button[aria-label="Download"],
button[aria-label="Expand"],
button[aria-label="Search"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stElementToolbar"] button:hover,
button[aria-label="Download"]:hover,
button[aria-label="Expand"]:hover,
button[aria-label="Search"]:hover {
    background-color: rgba(255,255,255,0.1) !important;
    border-radius: 6px;
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

/* Fix the hover popup container background */
div[data-testid="stElementToolbar"] {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Hide that floating white square next to expand button */
div[data-testid="stElementToolbar"] > div > div {
    background: transparent !important;
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



