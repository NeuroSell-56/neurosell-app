import streamlit as st
from openai import OpenAI

# Set your OpenAI API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(
    page_title="NeuroSell Industry Decoder™",
    layout="wide",
    initial_sidebar_state="auto"
)

# --------------------------
# Styling: Branded Colors & Logo
# --------------------------
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
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Step 1: Select Industry
# --------------------------
st.markdown("<div class='step-label'>Step 1: Select Industry</div>", unsafe_allow_html=True)
industries = [
    "Agriculture", "Education – K-12 & Higher Ed", "Financial Services",
    "Government – Federal", "Government – Local", "Government – State",
    "Grocery", "Healthcare", "Hospitality", "Manufacturing",
    "Midstream Oil & Gas", "Downstream Oil & Gas", "Retail",
    "Technology", "Transportation", "Utilities", "Other"
]
industry = st.selectbox("", industries)

# --------------------------
# Step 2: AI-generated General Pressure Type (GPT)
# --------------------------
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

# --------------------------
# Step 3: AI-generated Specific Pressure Type (SPT)
# --------------------------
st.markdown("<div class='step-label'>Step 3: Select Specific Pressure Type</div>", unsafe_allow_html=True)
spt_options = []
if gpt_selected:
    with st.spinner("Generating specific pressures..."):
        spt_prompt = f"""
        Based on the {industry} industry and the General Pressure Type '{gpt_selected}', return 4 concise Specific Pressure Types (2–3 words each, comma separated).
        """
        spt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": spt_prompt}]
        )
        spt_text = spt_response.choices[0].message.content.strip()
        spt_options = [opt.strip() for opt in spt_text.split(",")][:4]

spt_selected = st.selectbox("", spt_options) if spt_options else None

# --------------------------
# Step 4: AI-generated Strategic Narrative
# --------------------------
st.markdown("<div class='step-label'>Step 4: View Strategic Narrative</div>", unsafe_allow_html=True)
if spt_selected:
    with st.spinner("Crafting narrative..."):
        final_prompt = f"""
        Based on the {industry} industry, the General Pressure Type '{gpt_selected}', and the Specific Pressure Type '{spt_selected}', write a short strategic narrative (3-4 sentences) a sales professional could use to show deep understanding of the client's business challenge.
        """
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": final_prompt}]
        )
        final_text = final_response.choices[0].message.content.strip()
        st.markdown(f"<div class='narrative'>{final_text}</div>", unsafe_allow_html=True)
