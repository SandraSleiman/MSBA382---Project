import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --- Password protection and intro page ---
PASSWORD = "osb2025"
st.set_page_config(page_title="Sleep Health Dashboard", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # --- Sidebar password input ---
    st.sidebar.title("Login")
    password = st.sidebar.text_input("Enter password to access the dashboard", type="password")

    # --- Text and image side-by-side ---
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
            <div style='padding-top: 30px;'>
                <h1 style='font-size: 40px;'>💤 Sleep Health & Lifestyle Factors</h1>
                <h3 style='font-size: 24px; color: #777;'>MSBA 382 — Healthcare Analytics Project</h3>
                <p style='font-size: 17px; max-width: 600px; color: #aaa;'>
                    Welcome to this interactive dashboard exploring how lifestyle habits such as
                    alcohol consumption, caffeine intake, smoking, and physical activity influence
                    sleep efficiency and duration.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        try:
            st.image("cover_page.jpeg", width=200)
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
alcohol_filter = st.sidebar.multiselect("Alcohol consumption", df["Alcohol consumption"].unique(), default=df["Alcohol consumption"].unique())
exercise_range = st.sidebar.slider("Exercise Frequency", int(df["Exercise frequency"].min()), int(df["Exercise frequency"].max()), (0, 7))
smoking_filter = st.sidebar.multiselect("Smoking Status", df["Smoking status"].unique(), default=df["Smoking status"].unique())
caffeine_range = st.sidebar.slider("Caffeine Consumption", float(df["Caffeine consumption"].min()), float(df["Caffeine consumption"].max()), (0.0, 300.0))

# --- Page navigation ---
st.sidebar.title("Go to")
page = st.sidebar.radio("", ["Dashboard", "Filtered Dataset"])

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

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Sleep Efficiency (%)", f"{filtered_df['Sleep efficiency'].mean():.2f}")
    col2.metric("Avg Sleep Duration (hrs)", f"{filtered_df['Sleep duration'].mean():.2f}")
    col3.metric("Avg Caffeine (mg)", f"{filtered_df['Caffeine consumption'].mean():.0f}")

    st.markdown("---")
    st.subheader("Lifestyle Impact Visuals")

    # --- Visuals Layout: 3 per row ---
    vis_cols1 = st.columns(3)
    with vis_cols1[0]:
        st.markdown("**Sleep Efficiency by Alcohol**")
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x="Alcohol consumption", y="Sleep efficiency", estimator='mean', ax=ax, palette="Blues")
        ax.set_ylabel("Sleep Efficiency (%)")
        st.pyplot(fig)

    with vis_cols1[1]:
        st.markdown("**Sleep Efficiency by Smoking**")
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x="Smoking status", y="Sleep efficiency", estimator='mean', ax=ax, palette="Oranges")
        ax.set_ylabel("Sleep Efficiency (%)")
        st.pyplot(fig)

    with vis_cols1[2]:
        st.markdown("**Sleep Efficiency by Gender**")
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x="Gender", y="Sleep efficiency", estimator='mean', ax=ax, palette="Purples")
        ax.set_ylabel("Sleep Efficiency (%)")
        st.pyplot(fig)

    vis_cols2 = st.columns(3)
    with vis_cols2[0]:
        st.markdown("**REM Sleep % vs Caffeine**")
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x="Caffeine consumption", y="REM sleep percentage", hue="Gender", ax=ax, palette="Set2")
        ax.set_xlabel("Caffeine Consumption")
        ax.set_ylabel("REM Sleep %")
        st.pyplot(fig)

    with vis_cols2[1]:
        st.markdown("**Sleep Duration by Gender**")
        fig, ax = plt.subplots()
        sns.boxplot(data=filtered_df, x="Gender", y="Sleep duration", ax=ax, palette="coolwarm")
        ax.set_ylabel("Hours")
        st.pyplot(fig)

    with vis_cols2[2]:
        st.markdown("**Exercise Frequency**")
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x="Exercise frequency", color="#3fb1c0", ax=ax)
        ax.set_xlabel("Days per Week")
        ax.set_ylabel("Individuals")
        st.pyplot(fig)

# --- Filtered Dataset Page ---
elif page == "Filtered Dataset":
    st.title("Filtered Dataset Preview")
    st.dataframe(filtered_df, use_container_width=True)

