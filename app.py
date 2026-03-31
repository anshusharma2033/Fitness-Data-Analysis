import streamlit as st
import pandas as pd
import joblib
import database
import seaborn as sns
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="AI Fitness Intelligence System", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3 {
    color: #00ffcc;
}
div.stButton > button {
    background-color: #00ffcc;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------- HERO ----------
st.markdown("""
<div style='text-align:center'>
    <h1 style='color:#00ffcc;'>🤖 AI Fitness Intelligence System</h1>
    <p style='font-size:18px;'>Track • Analyze • Improve • Predict</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("---")
st.sidebar.success(random.choice([
    "Analyzing patterns...",
    "Running ML model...",
    "Generating insights..."
]))

# ---------- AUTH ----------
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Signup":
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        database.add_user(name, email, password)
        st.success("Account created!")

elif choice == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = database.login_user(email, password)
        if result:
            st.session_state["logged_in"] = True
            st.success(f"Welcome {result[0]} 🎉")
        else:
            st.error("Invalid credentials")

# ---------- MAIN ----------
if st.session_state["logged_in"]:

    st.markdown("### 📊 Explore Your Fitness Data")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🏋️ Exercise",
        "🥗 Diet",
        "🧠 AI Insights",
        "📋 Report"
    ])

    # ---------- DASHBOARD ----------
    with tab1:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔥 Calories", "350 kcal")

        with col2:
            st.metric("💧 Water", "8 glasses")

        with col3:
            st.metric("📊 BMI", "22.5")

        st.subheader("💡 AI Smart Tip")
        st.info(random.choice([
            "Consistency beats intensity",
            "Sleep improves recovery",
            "Hydration boosts metabolism"
        ]))

        # ---------- ML ----------
        st.subheader("🤖 Calories Prediction")
        model = joblib.load("calorie_model.pkl")

        duration = st.slider("Workout Duration", 10, 100)
        heart_rate = st.slider("Heart Rate", 80, 180)

        intensity = heart_rate / duration if duration != 0 else 0

        if st.button("Predict Calories"):
            pred = model.predict([[duration, heart_rate, intensity]])
            st.success(f"Predicted Calories: {pred[0]:.2f}")

            if pred[0] > 300:
                st.success("🔥 Great workout! Keep it up")
            else:
                st.warning("⚠️ Increase workout intensity")

        # ---------- REAL DATA ----------
        st.subheader("📊 Data Analysis")

        df = pd.read_csv("fitness_data.csv")
        df["Intensity"] = df["Heart_Rate"] / df["Duration"]

        st.write(df.describe())
        st.line_chart(df[["Duration", "Calories"]])

        # ---------- HEATMAP ----------
        st.subheader("🔥 Correlation Heatmap")

        corr = df.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(4,3))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # ---------- EXERCISE ----------
    with tab2:
        st.subheader("🏋️ Exercise Zone")

        weight = st.slider("Weight (kg)", 40, 120)
        time = st.slider("Workout Time", 5, 120)

        calories = weight * time * 0.12
        st.success(f"Calories Burned: {calories:.2f}")

        if calories > 300:
            st.success("🔥 Great workout!")
        else:
            st.warning("⚠️ Increase intensity")

    # ---------- DIET ----------
    with tab3:
        st.subheader("🥗 Diet & BMI")

        height = st.number_input("Height (cm)", 140, 210)
        weight_bmi = st.number_input("Weight (kg)", 40, 120)

        if height > 0:
            bmi = weight_bmi / ((height/100)**2)
            st.success(f"BMI: {bmi:.2f}")

            if bmi < 18.5:
                st.info("Underweight → High protein diet")
            elif bmi < 25:
                st.success("Normal → Maintain diet")
            else:
                st.warning("Overweight → Fat loss + cardio")

    # ---------- AI ----------
    with tab4:
        st.markdown("## 🧠 AI Lifestyle Analysis")

        sleep = st.slider("Sleep", 0, 10)
        water = st.slider("Water Intake", 0, 15)
        workout = st.slider("Workout Days", 0, 7)

        score = (sleep*10)+(water*3)+(workout*10)
        st.metric("🔥 Fitness Score", score)

        if score < 100:
            st.error("Poor Lifestyle")
        elif score < 180:
            st.warning("Average")
        else:
            st.success("Excellent")

    # ---------- REPORT ----------
    with tab5:
        st.subheader("📋 Report")

        st.write("Calories:", calories if 'calories' in locals() else 0)
        st.write("Water:", water if 'water' in locals() else 0)

else:
    st.warning("⚠️ Please login first")