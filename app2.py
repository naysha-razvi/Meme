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
    GROQ_API_KEY =["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"]
except Exception:
    st.error("❌ GROQ_API_KEY not found in Streamlit Secrets")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"

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

Always provide practical and actionable insights.

Always begin your answer with:

🔥 Hello! I am MemeScout, your AI Meme Trend Analyst.
"""

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp{
    background-color:#F8FAFC;
}

.hero{
    background:linear-gradient(135deg,#7C3AED,#EC4899);
    padding:2rem;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

.user-box{
    background:#EDE9FE;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}

.bot-box{
    background:#FCE7F3;
    padding:15px;
    border-radius:12px;
    margin-bottom:15px;
}

.stButton button{
    width:100%;
    background:linear-gradient(135deg,#7C3AED,#EC4899);
    color:white;
    border:none;
    border-radius:10px;
    font-weight:bold;
}

textarea {
    border-radius:12px !important;
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

    st.subheader("Features")

    st.markdown("""
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
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">
    <h1>🔥 MemeScout AI</h1>
    <p>Your AI Meme Trend Analyst</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SAMPLE QUESTIONS
# ==================================================

st.subheader("💡 Example Questions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Trending memes for fashion brands")

with col2:
    st.info("Most popular Gen-Z memes in India")

with col3:
    st.info("Food startup meme campaign ideas")

# ==================================================
# USER INPUT
# ==================================================

prompt = st.text_area(
    "Ask MemeScout",
    height=150,
    placeholder="Find trending memes for a sportswear brand..."
)

# ==================================================
# GENERATE RESPONSE
# ==================================================

if st.button("🚀 Analyze Trends"):

    if not prompt.strip():

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
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )

                answer = response.choices[0].message.content

                st.session_state.history.append({
                    "user": prompt,
                    "assistant": answer
                })

                st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ==================================================
# CHAT HISTORY
# ==================================================

if st.session_state.history:

    st.markdown("## 📈 Insights")

    for chat in reversed(st.session_state.history):

        st.markdown(
            f"""
            <div class="user-box">
            <b>👤 You:</b><br><br>
            {chat['user']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="bot-box">
            <b>🔥 MemeScout:</b><br><br>
            {chat['assistant']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# FOLLOW-UP QUESTIONS
# ==================================================

if st.session_state.history:

    st.markdown("### 🤔 Suggested Follow-up Questions")

    suggestions = [
        "What brands can use this meme?",
        "What are the risks of using this meme?",
        "Give me 5 campaign ideas.",
        "Which platforms should I target?",
        "How long will this trend last?"
    ]

    cols = st.columns(len(suggestions))

    for i, question in enumerate(suggestions):
        with cols[i]:
            if st.key=f"followup_{i}":

                try:
                    with st.spinner("Generating follow-up analysis..."):

                        response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=[
                                {
                                    "role": "system",
                                    "content": SYSTEM_PROMPT
                                },
                                {
                                    "role": "user",
                                    "content": question
                                }
                            ],
                            temperature=0.7,
                            max_tokens=1000
                        )

                        answer = response.choices[0].message.content

                        st.session_state.history.append({
                            "user": question,
                            "assistant": answer
                        })

                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.info(
    "🚀 MemeScout helps brands discover viral internet culture opportunities before competitors."
)
