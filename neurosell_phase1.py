import streamlit as st
import openai
from openai import OpenAI
from openai import AzureOpenAI
from openai import AsyncOpenAI
from openai import AsyncAzureOpenAI

# Set your OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="NeuroSell Industry Decoder™",
    layout="wide",
    initial_sidebar_state="auto"
)

# ----------------------------
# Styling: Branded Colors & Logo
# ----------------------------
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

# ----------------------------
# NeuroSell Logo
# ----------------------------
st.image("https://raw.githubusercontent.com/NeuroSell-56/assets/main/NeuroSell_AI_Official_Logo.png", width=250)

# ----------------------------
# Header
# ----------------------------
st.title("NeuroSell Industry Decoder™ – Industry Preferences + Pressure Grid")
st.write("Use the dropdowns below to decode industry pressures and generate strategic narratives.")

# ----------------------------
# Step 1: Select Industry
# ----------------------------
st.subheader("Step 1: Select Industry")
industries = [
    "Agriculture", "Education – K-12 & Higher Ed", "Financial Services",
    "Government – Federal", "Government – Local", "Government – State", "Grocery",
    "Healthcare", "Manufacturing", "Oil & Gas – Downstream", "Oil & Gas – Midstream",
    "Oil & Gas – Upstream", "Retail", "Technology", "Utilities", "Other (manual input)"
]
industry = st.selectbox("Select your Industry", [""] + industries)

# Initialize placeholders
gpt_options = []
spt_options = []
pressure_grid = []

# ----------------------------
# Step 2: GPT Dropdown
# ----------------------------
st.subheader("Step 2: Select General Pressure Type")
gpt = ""
if industry:
    gpt_prompt = f"""
    Based on the {industry} industry, list 6 General Pressure Types (GPTs) that typically impact this sector.
    Return them as a Python list of short 1-2 word categories only, no explanations.
    Example: ["Regulatory", "Financial", "Geopolitical", "Technological", "Labor", "Environmental"]
    """
    client = OpenAI()
    gpt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": gpt_prompt}],
        temperature=0.7,
    )
    try:
        gpt_options = eval(gpt_response.choices[0].message.content.strip())
    except Exception:
        gpt_options = []

gpt = st.selectbox("Select a General Pressure Type", [""] + gpt_options) if gpt_options else ""

# ----------------------------
# Step 3: SPT Dropdown
# ----------------------------
st.subheader("Step 3: Select Specific Pressure Type")
spt = ""
if industry and gpt:
    spt_prompt = f"""
    Based on the {industry} industry and the selected general pressure type '{gpt}',
    list 4 Specific Pressure Types (SPTs) that fall under this category.
    Return them as a Python list of short 1-3 word phrases only, no explanations.
    """
    spt_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": spt_prompt}],
        temperature=0.7,
    )
    try:
        spt_options = eval(spt_response.choices[0].message.content.strip())
    except Exception:
        spt_options = []

spt = st.selectbox("Select a Specific Pressure Type", [""] + spt_options) if spt_options else ""

# ----------------------------
# Step 4: Generate Pressure Grid
# ----------------------------
st.subheader("Step 4: Generate Pressure Grid")
grid_data = []
if st.button("Generate Pressure Grid") and industry and gpt and spt:
    grid_prompt = f"""
    Using the {industry} industry, General Pressure Type '{gpt}', and Specific Pressure Type '{spt}',
    generate a Pressure Grid with 4 rows. Each row should contain the following columns:
    1. Industry Driver
    2. Related KPI
    3. Observed Effects
    4. Industry Solution
    5. Narrative Opportunity
    6. Emotional State (with short explanation)

    Return the result as a list of 4 dictionaries in this format:
    [
        {{"Industry Driver": "...", "KPI": "...", "Observed Effects": "...", "Industry Solution": "...", "Narrative Opportunity": "...", "Emotional State": "..."}},
        ... 3 more like above ...
    ]
    """
    grid_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": grid_prompt}],
        temperature=0.7,
    )
    try:
        grid_data = eval(grid_response.choices[0].message.content.strip())
    except Exception:
        st.error("Failed to generate Pressure Grid. Please try again.")

    if grid_data:
        st.write("### Pressure Grid")
        st.dataframe(grid_data)
