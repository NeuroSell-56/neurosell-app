
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="NeuroSell Industry Decoder™",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown(
    """
    <style>
    body {
        background-color: #0B1D34;
    }
    .block-container {
        padding: 2rem;
    }
    h1, h2, h3, label, p {
        color: white !important;
    }
    .stButton button {
        background-color: #FFD700;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("https://raw.githubusercontent.com/NeuroSell-56/neurosell-assets/main/NeuroSell_Logo_White_Text.png", width=250)

st.markdown("<h1 style='text-align: center;'>NeuroSell Industry Decoder™</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Use the dropdowns below to decode industry pressures and generate strategic narratives.</p>", unsafe_allow_html=True)

industries = [
    "Agriculture",
    "Education – K-12 & Higher Ed",
    "Financial Services",
    "Government – Federal",
    "Government – Local",
    "Government – State",
    "Grocery",
    "Healthcare",
    "Manufacturing",
    "Midstream Oil & Gas",
    "Downstream Oil & Gas",
    "Retail",
    "Technology",
    "Other"
]

industry = st.selectbox("", industries)

# Step 2: AI-generated General Pressure Type (GPT)
st.markdown("<div class='step-label'>Step 2: Select General Pressure Type</div>", unsafe_allow_html=True)
gpt_options = []
if industry:
    with st.spinner("Analyzing industry..."):
        gpt_prompt = f"""
        List 6 concise General Pressure Types (1–2 words each, comma separated) facing the {industry} industry.
        """
        gpt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        gpt_text = gpt_response.choices[0].message.content.strip()
        gpt_options = [opt.strip() for opt in gpt_text.split(",")][:6]

gpt_selected = st.selectbox("", gpt_options) if gpt_options else None
