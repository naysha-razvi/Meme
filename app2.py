import streamlit as st
from groq import Groq

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="🔥 MemeScout AI",
    page_icon="🔥",
    layout="wide"
)

# ==================================================
# API KEY
# ==================================================

try:
    GROQ_API_KEY = st.secrets["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"]
except Exception:
    st.error("❌ GROQ_API_KEY not found in Streamlit Secrets")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-20b"

# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are MemeScout, an expert Meme Trend Analyst AI.

Your responsibilities:

• Identify trending memes
• Explain meme meaning and cultural context
• Recommend audiences
• Suggest marketing campaigns
• Highlight brand safety risks
• Suggest content ideas
• Recommend social media platforms
• Generate engagement strategies
• Suggest viral marketing tactics

Always provide practical, actionable, and brand-safe insights.

Always begin your answer with:

🔥 Hello! I am MemeScout, your AI Meme Trend Analyst.
"""

# ==================================================
# CUSTOM CSS
# ==================================================

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

[data-testid="stChatMessage"]{
    border-radius:16px;
    padding:10px;
}

.stButton button{
    width:100%;
    border-radius:12px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🔥 MemeScout")

    st.markdown("---")

    st.subheader("Features")

    st.markdown("""
✅ Trending Meme Discovery

✅ Meme Explanations

✅ Gen-Z Culture Insights

✅ Campaign Recommendations

✅ Brand Safety Analysis

✅ Audience Fit

✅ Viral Growth Strategies

✅ Content Ideas
""")

    st.markdown("---")

    if st.button("🗑 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">
<h1>🔥 MemeScout AI</h1>
<p>Your AI Meme Trend Analyst</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# QUICK START IDEAS
# ==================================================

st.subheader("💡 Popular Searches")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Trending memes for fashion brands")

with col2:
    st.info("Most popular Gen-Z memes in India")

with col3:
    st.info("Food startup meme campaign ideas")

# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==================================================
# CHAT INPUT (ALWAYS VISIBLE)
# ==================================================

prompt = st.chat_input(
    "Ask MemeScout about memes, trends, campaigns, Gen-Z culture..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        with st.spinner("🔍 Analyzing meme trends..."):

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    *[
                        {
                            "role": msg["role"],
                            "content": msg["content"]
                        }
                        for msg in st.session_state.messages
                    ]
                ],
                temperature=0.7,
                max_tokens=1500
            )

            answer = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.info(
    "🚀 MemeScout helps brands identify viral internet culture opportunities before competitors."
)
