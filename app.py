import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Password protection and intro page ---
PASSWORD = "osb2025"
st.set_page_config(page_title="Sleep Health Dashboard", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.title("Login")
    password = st.sidebar.text_input("Enter password to access the dashboard", type="password")

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
            st.image("cover_page.jpeg", width=280)
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

# --- Apply Streamlit theme overrides ---
st.markdown("""
    <style>
        section[data-testid="stSidebar"] > div:first-child {
            background-color: #f0f4f9;
        }
        .stSlider > div[data-testid="stSlider"] > div {
            color: #2a70c8;
        }
        .stMultiSelect > div[data-baseweb="select"] {
            background-color: #f0f4f9;
        }
    </style>
""", unsafe_allow_html=True)

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
    st.title("🛌 Sleep Health Dashboard")
    st.markdown("Analyze how lifestyle factors (alcohol, caffeine, smoking, exercise, age, gender) influence sleep quality.")

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Sleep Efficiency (%)", f"{filtered_df['Sleep efficiency'].mean():.2f}")
    col2.metric("Avg Sleep Duration (hrs)", f"{filtered_df['Sleep duration'].mean():.2f}")
    col3.metric("Avg Caffeine (mg)", f"{filtered_df['Caffeine consumption'].mean():.0f}")

    st.markdown("---")

    # --- Visuals in 3x2 layout with seaborn styling ---
    with plt.style.context('seaborn-colorblind'):
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            st.markdown("**Sleep Efficiency by Alcohol Consumption**")
            fig1, ax1 = plt.subplots()
            sns.barplot(x=filtered_df.groupby("Alcohol consumption")["Sleep efficiency"].mean().index,
                        y=filtered_df.groupby("Alcohol consumption")["Sleep efficiency"].mean().values,
                        ax=ax1)
            ax1.set_ylabel("Sleep Efficiency (%)")
            ax1.set_xlabel("Alcohol Consumption")
            st.pyplot(fig1)

        with row1_col2:
            st.markdown("**Sleep Efficiency by Smoking Status**")
            fig2, ax2 = plt.subplots()
            sns.barplot(x=filtered_df.groupby("Smoking status")["Sleep efficiency"].mean().index,
                        y=filtered_df.groupby("Smoking status")["Sleep efficiency"].mean().values,
                        ax=ax2)
            ax2.set_ylabel("Sleep Efficiency (%)")
            ax2.set_xlabel("Smoking Status")
            st.pyplot(fig2)

        with row1_col3:
            st.markdown("**Sleep Duration by Gender**")
            fig3, ax3 = plt.subplots()
            sns.boxplot(x="Gender", y="Sleep duration", data=filtered_df, ax=ax3)
            ax3.set_ylabel("Hours")
            ax3.set_title("Sleep Duration by Gender")
            st.pyplot(fig3)

        row2_col1, row2_col2, row2_col3 = st.columns(3)
        with row2_col1:
            st.markdown("**REM Sleep % vs Caffeine Consumption**")
            fig4, ax4 = plt.subplots()
            sns.scatterplot(x="Caffeine consumption", y="REM sleep percentage", data=filtered_df, ax=ax4)
            ax4.set_xlabel("Caffeine Consumption")
            ax4.set_ylabel("REM Sleep Percentage")
            st.pyplot(fig4)

        with row2_col2:
            st.markdown("**Exercise Frequency Distribution**")
            fig5, ax5 = plt.subplots()
            sns.countplot(x="Exercise frequency", data=filtered_df, ax=ax5)
            ax5.set_xlabel("Days per Week")
            ax5.set_ylabel("Number of People")
            ax5.set_title("Exercise Frequency")
            st.pyplot(fig5)

        with row2_col3:
            st.markdown("**Sleep Efficiency by Gender**")
            fig6, ax6 = plt.subplots()
            sns.barplot(x=filtered_df.groupby("Gender")["Sleep efficiency"].mean().index,
                        y=filtered_df.groupby("Gender")["Sleep efficiency"].mean().values,
                        ax=ax6)
            ax6.set_ylabel("Sleep Efficiency (%)")
            ax6.set_xlabel("Gender")
            st.pyplot(fig6)

# --- Filtered Dataset Page ---
elif page == "Filtered Dataset":
    st.title("📃 Filtered Dataset Preview")
    st.dataframe(filtered_df, use_container_width=True)

