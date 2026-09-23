import streamlit as st
from groq import Groq

# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="🔥 MemeScout AI",
    page_icon="🔥",
    layout="wide"
)

MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are MemeScout, an AI Meme Trend Analyst.

Your Responsibilities:
- Identify trending memes.
- Explain meme meaning and cultural context.
- Suggest marketing use cases.
- Highlight risks and brand safety concerns.
- Recommend audience fit.
- Suggest social platforms.
- Generate engagement strategies.

Rules:
- Never provide offensive content.
- Warn about controversial trends.
- Explain internet slang simply.
- Focus on marketing insights.

Always begin with:

🔥 Hello! I am MemeScout, your AI Meme Trend Analyst.

I help brands discover and leverage internet trends before they go mainstream.
"""

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

.hero {
    background: linear-gradient(135deg,#7C3AED,#EC4899);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
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
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(135deg,#7C3AED,#EC4899);
    color: white;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# GROQ CLIENT
# ==========================================================

try:
    GROQ_API_KEY = st.secrets["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"]
    client = Groq(api_key=GROQ_API_KEY)

except Exception:
    client = None

# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("⚙️ MemeScout")

    st.markdown("---")

    st.subheader("🎯 Features")

    st.markdown("""
✅ Discover Trending Memes

✅ Explain Meme Meaning

✅ Analyze Gen Z Culture

✅ Generate Campaign Ideas

✅ Evaluate Brand Safety

✅ Platform Recommendations

✅ Viral Content Strategies
""")

    st.markdown("---")

    if st.button("🗑 Clear History"):
        st.session_state.messages = []
        st.rerun()

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="hero">
<h1>🔥 MemeScout AI</h1>
<p>Your AI Meme Trend Analyst for Brands & Marketers</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# EXAMPLE PROMPTS
# ==========================================================

st.markdown("### 💡 Example Questions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Find trending memes for a fashion brand")

with col2:
    st.info("What memes are popular among Gen Z this week?")

with col3:
    st.info("Suggest meme marketing ideas for a food startup")

# ==========================================================
# USER INPUT
# ==========================================================

user_prompt = st.text_area(
    "Ask MemeScout",
    height=150,
    placeholder="Example: Find trending memes that a sportswear brand can use this week..."
)

# ==========================================================
# GENERATE RESPONSE
# ==========================================================

if st.button("🚀 Analyze Trends"):

    if not client:
        st.error("Missing GROQ_API_KEY in Streamlit Secrets.")

    elif not user_prompt.strip():
        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("🔍 Analyzing meme trends..."):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )

                result = response.choices[0].message.content

                st.session_state.messages.append({
                    "user": user_prompt,
                    "assistant": result
                })

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ==========================================================
# CHAT HISTORY
# ==========================================================

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

# ==========================================================
# FOOTER
# ==========================================================

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

<b>Goal:</b>

Help brands identify viral internet culture opportunities before competitors.

</div>
""", unsafe_allow_html=True)
