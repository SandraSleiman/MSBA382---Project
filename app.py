
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Password Protection ---
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

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Efficiency.xlsx")
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filters")
gender_filter = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))
alcohol_filter = st.sidebar.multiselect("Alcohol consumption", df["Alcohol consumption"].unique(), default=df["Alcohol consumption"].unique())
exercise_range = st.sidebar.slider("Exercise Frequency", int(df["Exercise frequency"].min()), int(df["Exercise frequency"].max()), (0, 7))

# --- Apply Filters ---
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(*age_range)) &
    (df["Alcohol consumption"].isin(alcohol_filter)) &
    (df["Exercise frequency"].between(*exercise_range))
]

# --- Navigation ---
page = st.sidebar.radio("Navigate", ["Sleep Overview", "Alcohol & Sleep", "Caffeine Impact", "Dataset"])

# --- Sleep Overview Page ---
if page == "Sleep Overview":
    st.title("🛏️ Sleep Health Dashboard")
    st.markdown("Analyze how lifestyle factors affect sleep quality.")

    col1, col2 = st.columns(2)
    col1.metric("Average Sleep Efficiency (%)", f"{filtered_df['Sleep efficiency'].mean():.2f}")
    col2.metric("Average Sleep Duration (hrs)", f"{filtered_df['Sleep duration'].mean():.2f}")

    st.subheader("Sleep Duration by Gender")
    fig, ax = plt.subplots()
    filtered_df.boxplot(column="Sleep duration", by="Gender", ax=ax)
    ax.set_title("Sleep Duration by Gender")
    ax.set_ylabel("Hours")
    st.pyplot(fig)

# --- Alcohol & Sleep Page ---
elif page == "Alcohol & Sleep":
    st.title("🍷 Alcohol & Sleep Efficiency")
    st.markdown("How does alcohol intake impact sleep efficiency?")

    fig, ax = plt.subplots()
    filtered_df.groupby("Alcohol consumption")["Sleep efficiency"].mean().plot(kind="bar", ax=ax)
    ax.set_ylabel("Sleep Efficiency (%)")
    ax.set_xlabel("Alcohol Consumption Level")
    st.pyplot(fig)

# --- Caffeine & REM Sleep ---
elif page == "Caffeine Impact":
    st.title("☕ Caffeine & REM Sleep")
    st.markdown("Scatter plot between caffeine and REM sleep.")

    fig, ax = plt.subplots()
    ax.scatter(filtered_df["Caffeine consumption"], filtered_df["REM sleep percentage"], alpha=0.6)
    ax.set_xlabel("Caffeine Consumption")
    ax.set_ylabel("REM Sleep %")
    st.pyplot(fig)

# --- Data Table Page ---
elif page == "Dataset":
    st.title("📄 Filtered Dataset")
    st.dataframe(filtered_df)
