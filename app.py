import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Password protection ---
PASSWORD = "osb2025"
st.set_page_config(page_title="Sleep Health Dashboard", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password to access the dashboard", type="password")
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
alcohol_filter = st.sidebar.multiselect("Alcohol consumption", df["Alcohol consumption"].unique(), default=df["Alcohol consumption"].unique())
exercise_range = st.sidebar.slider("Exercise Frequency", int(df["Exercise frequency"].min()), int(df["Exercise frequency"].max()), (0, 7))

# --- Apply filters ---
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(*age_range)) &
    (df["Alcohol consumption"].isin(alcohol_filter)) &
    (df["Exercise frequency"].between(*exercise_range))
]

# --- Page Title ---
st.title("🛏️ Sleep Health Dashboard")
st.markdown("Analyze how lifestyle factors (alcohol, caffeine, exercise, age, gender) influence sleep quality.")

# --- KPIs ---
col1, col2 = st.columns(2)
col1.metric("Average Sleep Efficiency (%)", f"{filtered_df['Sleep efficiency'].mean():.2f}")
col2.metric("Average Sleep Duration (hrs)", f"{filtered_df['Sleep duration'].mean():.2f}")

st.markdown("---")
st.subheader("📊 Sleep Visualizations")

# First row
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Sleep Efficiency by Alcohol Consumption**")
    fig1, ax1 = plt.subplots()
    filtered_df.groupby("Alcohol consumption")["Sleep efficiency"].mean().plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Sleep Efficiency (%)")
    ax1.set_xlabel("Alcohol Consumption Level")
    st.pyplot(fig1)

with col2:
    st.markdown("**REM Sleep % vs Caffeine Consumption**")
    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df["Caffeine consumption"], filtered_df["REM sleep percentage"], alpha=0.6)
    ax2.set_xlabel("Caffeine Consumption")
    ax2.set_ylabel("REM Sleep Percentage")
    st.pyplot(fig2)

# Second row
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Sleep Duration by Gender**")
    fig3, ax3 = plt.subplots()
    filtered_df.boxplot(column="Sleep duration", by="Gender", ax=ax3)
    ax3.set_title("Sleep Duration by Gender")
    ax3.set_ylabel("Hours")
    st.pyplot(fig3)

with col4:
    st.markdown("**Exercise Frequency Distribution**")
    fig4, ax4 = plt.subplots()
    filtered_df["Exercise frequency"].value_counts().sort_index().plot(kind="bar", ax=ax4)
    ax4.set_xlabel("Days per Week")
    ax4.set_ylabel("Number of People")
    ax4.set_title("Exercise Frequency")
    st.pyplot(fig4)

# Third row
col5, col6 = st.columns(2)

with col5:
    st.markdown("**Sleep Efficiency by Smoking Status**")
    fig5, ax5 = plt.subplots()
    filtered_df.groupby("Smoking status")["Sleep efficiency"].mean().plot(kind="bar", ax=ax5)
    ax5.set_ylabel("Sleep Efficiency (%)")
    ax5.set_xlabel("Smoking Status")
    st.pyplot(fig5)

with col6:
    st.markdown("**Filtered Dataset Preview**")
    st.dataframe(filtered_df)


