"""
CoachBot AI - Smart Fitness Assistance Web App for Professional Tennis Players

This application uses Google's Gemini 1.5 Pro to provide personalized coaching
for young tennis players, bridging the gap in professional coaching accessibility.
"""

import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="CoachBot AI - Tennis Coach",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    color: #1E3A8A;
    text-align: center;
}
.sub-header {
    font-size: 1.2rem;
    color: #64748B;
    text-align: center;
    margin-bottom: 2rem;
}
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: white;
    border-radius: 10px;
    padding: 0.75rem;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:

    st.title("🎾 CoachBot AI")
    st.caption("Your AI Tennis Coach")

    st.markdown("---")

    # API Key
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter API key"
    )

    if api_key:
        st.success("API Connected")
    else:
        st.warning("Enter API Key")

    st.markdown("---")

    # Player Profile
    player_name = st.text_input("Name")
    age = st.slider("Age", 10, 25, 16)

    position = st.selectbox(
        "Playing Style",
        [
            "Baseline Player",
            "Serve & Volley",
            "All-Court Player",
            "Doubles Specialist"
        ]
    )

    surface = st.selectbox(
        "Court Surface",
        ["Hard", "Clay", "Grass", "Indoor"]
    )

    level = st.selectbox(
        "Skill Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
            "Competitive",
            "Professional"
        ]
    )

    serve_pct = st.slider("First Serve %", 30, 85, 65)

    injuries = st.multiselect(
        "Injury History",
        [
            "None - Healthy",
            "Shoulder",
            "Elbow",
            "Wrist",
            "Back",
            "Knee",
            "Ankle",
            "Hip"
        ],
        default=["None - Healthy"]
    )

    diet = st.selectbox(
        "Diet Type",
        ["Omnivore", "Vegetarian", "Vegan", "Pescatarian"]
    )

    goal = st.selectbox(
        "Training Goal",
        [
            "Stamina",
            "Power",
            "Agility",
            "Recovery",
            "Tournament Prep",
            "Skill Development",
            "Mental Toughness"
        ]
    )


# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="main-header">🎾 CoachBot AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Tennis Coaching System</div>', unsafe_allow_html=True)

if player_name:
    st.info(f"Welcome {player_name} | Level: {level} | Goal: {goal}")


# ============================================================================
# API CONFIG
# ============================================================================
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        st.success("Gemini Model Ready")
    except Exception as e:
        st.error(str(e))
else:
    st.warning("Please enter API Key")


# ============================================================================
# AI FUNCTION
# ============================================================================
def generate_response(prompt, temp=0.3):

    if not api_key:
        return "Enter API Key First"

    try:

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temp,
                max_output_tokens=2048,
                top_p=0.95,
                top_k=40
            )
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# USER PROFILE
# ============================================================================
user_data = {
    "name": player_name or "Player",
    "age": age,
    "position": position,
    "surface": surface,
    "level": level,
    "serve": serve_pct,
    "injuries": ", ".join(injuries),
    "diet": diet,
    "goal": goal
}


# ============================================================================
# TRAINING SCHEDULE
# ============================================================================
def weekly_schedule(injuries):

    data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Morning": [
            "Groundstrokes",
            "Agility",
            "Match Play",
            "Strength",
            "Technique",
            "Tournament Sim",
            "Recovery"
        ],
        "Evening": [
            "Serve",
            "Tactics",
            "Video",
            "Yoga",
            "Hitting",
            "Competition",
            "Stretching"
        ],
        "Hours": [2.5, 2.5, 3, 2, 2.5, 3.5, 1.5],
        "Intensity": ["High", "Medium", "High", "High", "Medium", "High", "Low"]
    }

    df = pd.DataFrame(data)

    if "None - Healthy" not in injuries:
        df["Notes"] = [
            "Low impact",
            "Light cardio",
            "Reduced load",
            "Safe strength",
            "Technique only",
            "Monitor pain",
            "Extra rest"
        ]

    return df


# ============================================================================
# PROMPTS
# ============================================================================
PROMPTS = {

    "Workout": {
        "temp": 0.3,
        "text": """
You are a professional tennis coach.

Player: {name}
Age: {age}
Style: {position}
Surface: {surface}
Level: {level}
Goal: {goal}

Create a full weekly workout plan with warmup, drills, strength, and recovery.
"""
    },

    "Injury Recovery": {
        "temp": 0.3,
        "text": """
You are a sports physiotherapist.

Player: {name}
Injuries: {injuries}
Goal: {goal}

Create a safe injury recovery program.
"""
    },

    "Tactics": {
        "temp": 0.7,
        "text": """
You are a professional match strategist.

Player: {name}
Style: {position}
Surface: {surface}
Level: {level}

Create tactical match strategy.
"""
    },

    "Nutrition": {
        "temp": 0.3,
        "text": """
You are a sports nutritionist.

Player: {name}
Age: {age}
Diet: {diet}
Goal: {goal}

Create daily nutrition plan.
"""
    },

    "Mental Training": {
        "temp": 0.7,
        "text": """
You are a sports psychologist.

Player: {name}
Age: {age}
Level: {level}
Goal: {goal}

Create mental toughness routine.
"""
    },

    "Serve Training": {
        "temp": 0.3,
        "text": """
You are a serve biomechanics expert.

Player: {name}
Serve %: {serve}
Injuries: {injuries}

Create serve improvement program.
"""
    }
}


# ============================================================================
# SESSION STATE
# ============================================================================
if "result" not in st.session_state:
    st.session_state.result = ""

if "feature" not in st.session_state:
    st.session_state.feature = ""


# ============================================================================
# FEATURE BUTTONS
# ============================================================================
st.markdown("---")
st.subheader("🚀 Coaching Modules")

cols = st.columns(3)

features = list(PROMPTS.keys())

for i, feature in enumerate(features):

    with cols[i % 3]:

        if st.button(feature):

            p = PROMPTS[feature]

            prompt = p["text"].format(**user_data)

            st.session_state.feature = feature

            st.session_state.result = generate_response(
                prompt,
                p["temp"]
            )


# ============================================================================
# OUTPUT
# ============================================================================
if st.session_state.result:

    st.markdown("---")

    st.subheader(st.session_state.feature)

    time = datetime.now().strftime("%d %B %Y | %I:%M %p")

    st.caption(f"Generated on {time}")

    st.markdown(st.session_state.result)

    st.markdown("---")

    st.subheader("📅 Weekly Training Plan")

    df = weekly_schedule(injuries)

    st.dataframe(df, use_container_width=True, hide_index=True)


# ============================================================================
# INFO SECTION (NO ASSIGNMENT INFO)
# ============================================================================
st.markdown("---")

with st.expander("ℹ️ About CoachBot AI"):

    st.markdown("""
CoachBot AI is an AI-powered tennis coaching assistant that provides personalized
training, nutrition, tactical, and recovery guidance.

It adapts recommendations based on player profile, injuries, and goals.
""")


with st.expander("⚠️ Disclaimer"):

    st.markdown("""
This application provides general training guidance.

It does NOT replace professional medical or coaching advice.

Always consult certified professionals for injuries and health issues.
""")


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

st.markdown("""
<div style="text-align:center;color:gray;">
<p><b>CoachBot AI</b> – Tennis Performance System</p>
<p>Powered by Gemini 1.5 Pro | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

