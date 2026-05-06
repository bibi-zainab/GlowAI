import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import google.generativeai as genai
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GlowAI",
    page_icon="✨",
    layout="wide"
)

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- GEMINI SETUP ----------------
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.stMetric {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- PDF FUNCTION ----------------
def generate_pdf(name, score, ai_text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "GlowAI Skin Report",
            styles['Title']
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"User: {name}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Skin Score: {score}/100",
            styles['BodyText']
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            ai_text,
            styles['BodyText']
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("✨ GlowAI")

    selected = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Skin Quiz",
            "Results",
            "AI Chat",
            "About"
        ],
        icons=[
            "house",
            "clipboard-heart",
            "bar-chart",
            "chat-dots",
            "info-circle"
        ],
        default_index=0,
    )

# ---------------- HOME ----------------
if selected == "Home":

    st.title("✨ GlowAI")

    st.subheader("AI Powered Skin Health Assistant")

    st.write("""
    Understand your skin, analyze habits,
    and receive personalized skincare guidance using AI.
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info("🧠 AI Analysis")

        st.write("""
        • Skin Pattern Insights

        • Personalized Recommendations

        • AI Generated Guidance
        """)

    with col2:

        st.success("📊 Analytics Dashboard")

        st.write("""
        • AI Skin Score

        • Wellness Tracking

        • Lifestyle Analytics
        """)

    with col3:

        st.warning("💖 Personalized Routine")

        st.write("""
        • Morning Routine

        • Night Routine

        • Ingredient Suggestions
        """)

    st.divider()

    st.subheader("🚀 Why GlowAI?")

    st.write("""
    GlowAI combines AI with skincare education
    to help users better understand their skin health,
    habits, and routines.
    """)

# ---------------- SKIN QUIZ ----------------
elif selected == "Skin Quiz":

    st.title("🧴 AI Skin Health Quiz")

    st.write("Fill this quiz for personalized AI skincare insights.")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Your Name")

        skin_type = st.selectbox(
            "Select Skin Type",
            ["Oily", "Dry", "Combination", "Sensitive"]
        )

        acne = st.slider(
            "Acne Frequency",
            0,
            10
        )

    with col2:

        water = st.slider(
            "Daily Water Intake",
            1,
            10
        )

        sleep = st.slider(
            "Sleep Hours",
            1,
            12
        )

        sunscreen = st.radio(
            "Do you use sunscreen?",
            ["Yes", "No"]
        )

    concern = st.multiselect(
        "Skin Concerns",
        [
            "Pigmentation",
            "Dark Spots",
            "Dryness",
            "Acne",
            "Redness",
            "Tan"
        ]
    )

    st.progress(90)

    if st.button("Generate AI Report"):

        with st.spinner("Analyzing your skin profile..."):

            st.session_state["name"] = name
            st.session_state["skin_type"] = skin_type
            st.session_state["acne"] = acne
            st.session_state["water"] = water
            st.session_state["sleep"] = sleep
            st.session_state["sunscreen"] = sunscreen
            st.session_state["concern"] = concern

        st.success("AI Skin Report Generated Successfully ✨")

# ---------------- RESULTS ----------------
elif selected == "Results":

    st.title("📊 AI Skin Analysis Report")

    if "skin_type" in st.session_state:

        # ---------------- AI SCORE ----------------

        skin_score = 50

        skin_score += st.session_state["water"] * 2
        skin_score += st.session_state["sleep"] * 2

        if st.session_state["sunscreen"] == "Yes":
            skin_score += 10

        skin_score = min(skin_score, 100)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=skin_score,
            title={'text': "AI Skin Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#ff4b91"}
            }
        ))

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # ---------------- METRICS ----------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💧 Water Intake",
                f"{st.session_state['water']}/10"
            )

        with col2:
            st.metric(
                "😴 Sleep",
                f"{st.session_state['sleep']} hrs"
            )

        with col3:
            st.metric(
                "☀ Sunscreen",
                st.session_state["sunscreen"]
            )

        st.divider()

        # ---------------- AI ANALYSIS ----------------

        st.subheader("🤖 AI Skin Expert Analysis")

        prompt = f"""
        Analyze this skincare profile.

        Skin Type: {st.session_state['skin_type']}
        Concerns: {st.session_state['concern']}
        Water Intake: {st.session_state['water']}
        Sleep Hours: {st.session_state['sleep']}
        Sunscreen Usage: {st.session_state['sunscreen']}
        Acne Frequency: {st.session_state['acne']}

        Generate:
        1. Skin Summary
        2. Causes
        3. Morning Routine
        4. Night Routine
        5. Ingredients to Use
        6. Ingredients to Avoid
        7. Lifestyle Improvements

        Keep response beginner friendly.
        """

        with st.spinner("Generating AI analysis..."):

            response = model.generate_content(prompt)

            ai_answer = response.text

        st.success("AI Analysis Generated")

        st.write(ai_answer)

        # ---------------- DASHBOARD ----------------

        st.subheader("📈 Wellness Dashboard")

        data = pd.DataFrame({
            "Category": [
                "Water",
                "Sleep",
                "Skin Care"
            ],
            "Score": [
                st.session_state["water"],
                st.session_state["sleep"],
                8 if st.session_state["sunscreen"] == "Yes" else 3
            ]
        })

        chart = px.bar(
            data,
            x="Category",
            y="Score",
            title="Skin Wellness Metrics"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        # ---------------- PDF DOWNLOAD ----------------

        pdf = generate_pdf(
            st.session_state["name"],
            skin_score,
            ai_answer
        )

        st.download_button(
            label="📄 Download Skin Report",
            data=pdf,
            file_name="GlowAI_Report.pdf",
            mime="application/pdf"
        )

    else:

        st.warning("Please complete the Skin Quiz first.")

# ---------------- AI CHAT ----------------
elif selected == "AI Chat":

    st.title("💬 GlowAI AI Chat")

    st.write("Ask skincare questions using AI.")

    user_input = st.chat_input(
        "Ask your skincare question..."
    )

    if user_input:

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = model.generate_content(
                    f"""
                    You are a skincare assistant.

                    Answer this question:

                    {user_input}
                    """
                )

                st.write(response.text)

# ---------------- ABOUT ----------------
elif selected == "About":

    st.title("💖 About GlowAI")

    st.write("""
    GlowAI is an AI-powered skincare assistant
    designed to help users understand skin health,
    skincare routines, and lifestyle habits.
    """)

    st.subheader("🚀 Features")

    st.write("""
    • AI Skin Analysis

    • AI Chat Assistant

    • Personalized Skincare Routines

    • AI Skin Score

    • Wellness Dashboard

    • PDF Report Export
    """)

    st.subheader("🛠 Tech Stack")

    st.write("""
    • Python

    • Streamlit

    • Gemini API

    • Plotly

    • ReportLab
    """)