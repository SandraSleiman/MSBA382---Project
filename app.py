import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page config and password ---
st.set_page_config(page_title="Sleep Health Dashboard", layout="wide")
PASSWORD = "osb2025"

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
smoking_filter = st.sidebar.multiselect("Smoking Status", df["Smoking status"].unique(), default=df["Smoking status"].unique())
caffeine_range = st.sidebar.slider("Caffeine Consumption Range", int(df["Caffeine consumption"].min()), int(df["Caffeine consumption"].max()), (0, 500))

# --- Apply filters ---
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(*age_range)) &
    (df["Alcohol consumption"].isin(alcohol_filter)) &
    (df["Exercise frequency"].between(*exercise_range)) &
    (df["Smoking status"].isin(smoking_filter)) &
    (df["Caffeine consumption"].between(*caffeine_range))
]

# --- Page selection ---
page = st.sidebar.radio("Navigate", ["Overview", "Lifestyle Impact", "Data Explorer"])

if page == "Overview":
    st.title("🛏️ Sleep Health Dashboard")
    st.markdown("Understand how lifestyle factors impact sleep quality.")

    col1, col2 = st.columns(2)
    col1.metric("Average Sleep Efficiency (%)", f"{filtered_df['Sleep efficiency'].mean():.2f}")
    col2.metric("Average Sleep Duration (hrs)", f"{filtered_df['Sleep duration'].mean():.2f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sleep Efficiency by Alcohol Consumption**")
        fig1, ax1 = plt.subplots()
        filtered_df.groupby("Alcohol consumption")["Sleep efficiency"].mean().plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Sleep Efficiency (%)")
        ax1.set_xlabel("Alcohol Consumption")
        st.pyplot(fig1)

    with col2:
        st.markdown("**REM Sleep % vs Caffeine Consumption**")
        fig2, ax2 = plt.subplots()
        ax2.scatter(filtered_df["Caffeine consumption"], filtered_df["REM sleep percentage"], alpha=0.6)
        ax2.set_xlabel("Caffeine Consumption")
        ax2.set_ylabel("REM Sleep %")
        st.pyplot(fig2)

elif page == "Lifestyle Impact":
    st.title("💡 Lifestyle Factor Insights")
    st.markdown("Explore how smoking, exercise, and gender influence sleep health.")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Sleep Efficiency by Smoking Status**")
        fig3, ax3 = plt.subplots()
        filtered_df.groupby("Smoking status")["Sleep efficiency"].mean().plot(kind="bar", ax=ax3)
        ax3.set_ylabel("Sleep Efficiency (%)")
        ax3.set_xlabel("Smoking Status")
        st.pyplot(fig3)

    with col4:
        st.markdown("**Exercise Frequency Distribution**")
        fig4, ax4 = plt.subplots()
        filtered_df["Exercise frequency"].value_counts().sort_index().plot(kind="bar", ax=ax4)
        ax4.set_xlabel("Days per Week")
        ax4.set_ylabel("Number of Individuals")
        st.pyplot(fig4)

    st.markdown("---")
    st.markdown("**Sleep Duration by Gender**")
    fig5, ax5 = plt.subplots()
    filtered_df.boxplot(column="Sleep duration", by="Gender", ax=ax5)
    ax5.set_title("Sleep Duration by Gender")
    ax5.set_ylabel("Hours")
    st.pyplot(fig5)

elif page == "Data Explorer":
    st.title("🔍 Data Explorer & Correlations")
    st.markdown("Analyze the full dataset and explore correlations between variables.")

    st.markdown("**Correlation Heatmap**")
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    numeric_cols = filtered_df.select_dtypes(include=['number'])
    sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", ax=ax6)
    st.pyplot(fig6)

    st.markdown("---")
    st.markdown("**Filtered Dataset Preview**")
    st.dataframe(filtered_df)



