
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

# --- Load cleaned data ---
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Efficiency.xlsx")
    return df

df = load_data()

st.write("COLUMN NAMES:", df.columns.tolist())


# --- Sidebar filters ---
st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))
alcohol_filter = st.sidebar.multiselect("Alcohol Level", df["Alcohol consumption"].unique(), default=df["Alcohol consumption"].unique())
exercise_range = st.sidebar.slider("Exercise Frequency", int(df["Exercise frequency"].min()), int(df["Exercise frequency"].max()), (0, 7))

# Apply filters
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(*age_range)) &
    (df["Alcohol consumption"].isin(alcohol_filter)) &
    (df["Exercise frequency"].between(*exercise_range))
]

# --- KPIs ---
st.title("Sleep Health Dashboard")
st.markdown("Analyze how lifestyle factors affect sleep quality.")

col1, col2 = st.columns(2)
col1.metric("Average Sleep Efficiency (%)", f"{filtered_df['Sleep efficiency'].mean():.2f}")
col2.metric("Average Sleep Duration (hrs)", f"{filtered_df['Sleep duration'].mean():.2f}")

# --- Sleep Efficiency by Alcohol Level ---
st.subheader("Sleep Efficiency by Alcohol Level")
fig1, ax1 = plt.subplots()
filtered_df.groupby("Alcohol consumption")["Sleep efficiency"].mean().plot(kind="bar", ax=ax1)
ax1.set_ylabel("Sleep Efficiency (%)")
ax1.set_xlabel("Alcohol Consumption Level")
st.pyplot(fig1)

# --- REM Sleep vs Caffeine ---
st.subheader("REM Sleep % vs Caffeine Consumption")
fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df["Caffeine consumption"], filtered_df["REM sleep percentage"], alpha=0.6)
ax2.set_xlabel("Caffeine Consumption")
ax2.set_ylabel("REM Sleep Percentage")
st.pyplot(fig2)

# --- Sleep Duration by Gender ---
st.subheader("Sleep Duration by Gender")
fig3, ax3 = plt.subplots()
filtered_df.boxplot(column="Sleep duration", by="Gender", ax=ax3)
ax3.set_title("Sleep Duration by Gender")
ax3.set_ylabel("Hours")
st.pyplot(fig3)

# --- Data Table ---
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)
