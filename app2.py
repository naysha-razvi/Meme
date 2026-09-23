import streamlit as st
from openai import OpenAI

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="DeepSeek AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# NVIDIA CLIENT
# ---------------------------
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=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"
)

# ---------------------------
# SESSION STATE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#0B1220;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#111827;
}

/* Hero Section */
.hero{
    background:#111827;
    border:1px solid #334155;
    border-radius:24px;
    padding:2rem;
    text-align:center;
    margin-bottom:20px;
}

.hero h1{
    color:#F8FAFC;
    font-size:42px;
    margin-bottom:8px;
}

.hero p{
    color:#94A3B8;
    font-size:16px;
}

/* Cards */
.insight-card{
    background:#111827;
    border:1px solid #334155;
    border-radius:18px;
    padding:15px;
}

/* Buttons */
.stButton button{
    width:100%;
    border-radius:12px;
    background:#2563EB;
    color:white;
    border:none;
    font-weight:600;
}

.stButton button:hover{
    background:#1D4ED8;
}

/* Chat Message Styling */
[data-testid="stChatMessage"]{
    border-radius:16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HERO
# ---------------------------
st.markdown("""
<div class="hero">
    <h1>🤖 DeepSeek AI Assistant</h1>
    <p>Powered by NVIDIA NIM</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("### About")
    st.info(
        "AI Assistant powered by DeepSeek and NVIDIA APIs"
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### Suggested Topics")

    st.markdown("""
    ✅ Business Analysis

    ✅ Prompt Engineering

    ✅ Marketing Ideas

    ✅ AI Learning

    ✅ Startup Planning
    """)

# ---------------------------
# DISPLAY OLD CHAT
# ---------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.chat_input(
    "Ask me anything..."
)

# ---------------------------
# AI RESPONSE
# ---------------------------
if user_input:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        try:

            messages = [
                {
                    "role":"system",
                    "content":"""
You are an intelligent AI assistant.

Rules:
1. Give accurate answers.
2. Avoid repeating responses.
3. Be concise and practical.
4. Use bullet points when helpful.
5. Ask one relevant follow-up question.
"""
                }
            ]

            messages.extend(st.session_state.messages)

            response = client.chat.completions.create(

                model="deepseek-ai/deepseek-r1",

                messages=messages,

                temperature=0.7,

                top_p=0.9,

                max_tokens=1200
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )

        except Exception as e:

            st.error(f"Error: {e}")
