import streamlit as st
from groq import Groq
import os

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="🔥 MemeScout AI",
    page_icon="🔥",
    layout="wide"
)

# ==================================================
# API CONFIG
# ==================================================

GROQ_API_KEY = os.getenv("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")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"

# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are MemeScout, an AI Meme Trend Analyst.

Responsibilities:
- Identify trending memes
- Explain cultural context
- Suggest marketing campaigns
- Highlight risks and brand safety concerns
- Recommend audience fit
- Suggest social platforms
- Generate engagement ideas

Always start with:

🔥 Hello! I am MemeScout, your AI Meme Trend Analyst.
"""

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp{
    background:#F8FAFC;
}

.hero{
    background:linear-gradient(135deg,#7C3AED,#EC4899);
    padding:2rem;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
}

.chat-user{
    background:#EDE9FE;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}

.chat-bot{
    background:#FCE7F3;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}

.stButton button{
    width:100%;
    border:none;
    border-radius:10px;
    color:white;
    font-weight:bold;
    background:linear-gradient(135deg,#7C3AED,#EC4899);
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🔥 MemeScout")

    st.markdown("---")

    st.write("### Features")

    st.write("""
✅ Trending Memes

✅ Meme Meaning

✅ Gen-Z Analysis

✅ Campaign Ideas

✅ Brand Safety

✅ Viral Growth Strategies
""")

    st.markdown("---")

    if st.button("🗑 Clear History"):
        st.session_state.history = []
        st.rerun()

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero">
<h1>🔥 MemeScout AI</h1>
<p>Your AI Meme Trend Analyst</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# EXAMPLES
# ==================================================

st.subheader("💡 Example Questions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Trending memes for fashion brands")

with col2:
    st.info("Most popular Gen-Z memes")

with col3:
    st.info("Food startup meme campaign ideas")

# ==================================================
# INPUT
# ==================================================

prompt = st.text_area(
    "Ask MemeScout",
    height=150,
    placeholder="Find trending memes for a sportswear brand..."
)

# ==================================================
# GENERATE
# ==================================================

if st.button("🚀 Analyze Trends"):

    if not prompt.strip():
        st.warning("Enter a question.")
    else:

        try:

            with st.spinner("Analyzing..."):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role":"system",
                            "content":SYSTEM_PROMPT
                        },
                        {
                            "role":"user",
                            "content":prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )

                result = response.choices[0].message.content

                st.session_state.history.append({
                    "user":prompt,
                    "assistant":result
                })

        except Exception as e:
            st.error(str(e))

# ==================================================
# CHAT HISTORY
# ==================================================

if st.session_state.history:

    st.markdown("## 📈 Insights")

    for item in reversed(st.session_state.history):

        st.markdown(
            f"""
            <div class="chat-user">
            <b>👤 You:</b><br>
            {item['user']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="chat-bot">
            <b>🔥 MemeScout:</b><br>
            {item['assistant']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.info(
    "🚀 MemeScout helps brands discover viral internet culture opportunities before competitors."
)
