import streamlit as st
import os
from google import genai
from google.genai import types

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="MemeScout AI",
    page_icon="🔥",
    layout="wide"
)

# ----------------------------------
# CUSTOM CSS
# ----------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

.hero {
    background: linear-gradient(135deg, #7C3AED, #EC4899);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 48px;
}

.hero p {
    font-size: 18px;
}

.user-box {
    background-color: #EDE9FE;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.bot-box {
    background-color: #FCE7F3;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.insight-card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(135deg, #7C3AED, #EC4899);
    color: white;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")
# ----------------------------------
# SIDEBAR
# ----------------------------------
with st.sidebar:
    st.title("⚙ Configuration")

    st.markdown("---")

    st.subheader("🎯 What MemeScout Does")

    st.markdown("""
    - Discover trending memes
    - Explain meme meaning
    - Analyze Gen Z culture
    - Suggest campaign ideas
    - Evaluate brand safety
    - Recommend social platforms
    - Generate viral content strategies
    """)

# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("""
<div class="hero">
    <h1>🔥 MemeScout AI</h1>
    <p>Your AI Meme Trend Analyst for Brands & Marketers</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# SYSTEM PROMPT
# ----------------------------------
system_instruction = """
You are a Meme Trend Analyst AI.

Your name is MemeScout.

Your Role:
- Help brands identify trending memes.
- Explain meme meaning and cultural context.
- Suggest how brands can use memes in marketing campaigns.
- Highlight risks of using a meme.
- Evaluate whether a meme aligns with a brand's target audience.
- Recommend suitable social media platforms.
- Suggest engagement strategies based on trends.

Rules:
- Never provide offensive content.
- Warn users when a meme may be controversial.
- Explain internet slang in simple language.
- Focus on marketing insights rather than entertainment only.

Always greet users with:

"🔥 Hello! I am MemeScout, your AI Meme Trend Analyst. I help brands discover and leverage internet trends before they go mainstream."
"""

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# SUGGESTED PROMPTS
# ----------------------------------
st.markdown("### 💡 Try These Questions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Find trending memes for a fashion brand")

with col2:
    st.info("What memes are popular among Gen Z this week?")

with col3:
    st.info("Suggest meme marketing ideas for a food startup")

# ----------------------------------
# USER INPUT
# ----------------------------------
user_prompt = st.text_area(
    "Ask MemeScout",
    placeholder="Example: Find trending memes that a sportswear brand can use this week..."
)

# ----------------------------------
# BUTTON
# ----------------------------------
if st.button("🚀 Analyze Trends"):

    if not api_key:
        st.error("Please enter your Gemini API Key.")
    elif not user_prompt.strip():
        st.warning("Enter a question to continue.")
    else:

        try:
            client = genai.Client(api_key=api_key)

            with st.spinner("Analyzing internet culture and trends..."):

                response = client.models.generate_content(
                    model="gemini-flash-lite-latest",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        max_output_tokens=800
                    )
                )

                result = response.text

                st.session_state.messages.append(
                    {
                        "user": user_prompt,
                        "assistant": result
                    }
                )

        except Exception as e:
            st.error(f"Error: {e}")

# ----------------------------------
# CONVERSATION
# ----------------------------------
if st.session_state.messages:

    st.markdown("## 📈 Meme Trend Insights")

    for msg in reversed(st.session_state.messages):

        st.markdown(
            f"""
            <div class="user-box">
            <b>👤 You:</b><br>
            {msg['user']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="bot-box">
            <b>🔥 MemeScout:</b><br>
            {msg['assistant']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")

st.markdown("""
<div class="insight-card">
<b>📌 Business Use Cases</b>

<ul>
<li>Social Media Teams</li>
<li>Marketing Agencies</li>
<li>D2C Brands</li>
<li>Fashion Brands</li>
<li>Food & Beverage Companies</li>
<li>Personal Branding Consultants</li>
<li>Influencer Marketing Teams</li>
</ul>

<b>Goal:</b> Help brands identify viral internet culture opportunities before competitors.
</div>
""", unsafe_allow_html=True)
