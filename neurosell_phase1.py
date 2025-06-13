import streamlit as st
import openai

# -----------------------------
# Set your OpenAI API key securely
# -----------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="NeuroSell Industry Decoder™",
    layout="wide",
    initial_sidebar_state="auto"
)

# -----------------------------
# Styling: Branded Colors & Logo
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #081D34;
        color: white;
    }
    .title-text {
        color: white;
        font-size: 32px;
        font-weight: 700;
        padding-bottom: 10px;
    }
    .step-label {
        font-weight: 600;
        color: white;
        padding-top: 10px;
    }
    .yellow-button > div > button {
        background-color: #FFD700 !important;
        color: black !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("https://raw.githubusercontent.com/NeuroSell-56/neurosell-app/main/NeuroSell_AI_Official_Logo.png", width=180)
st.markdown('<div class="title-text">NeuroSell Industry Decoder™ – Industry Preferences + Pressure Grid</div>', unsafe_allow_html=True)

st.markdown("Use the dropdowns below to decode industry pressures and generate strategic narratives.")

# -----------------------------
# Step 1: Industry Dropdown
# -----------------------------
st.markdown("<div class='step-label'>Step 1: Select Industry</div>", unsafe_allow_html=True)
industries = [
    "Agriculture", "Education – K–12 & Higher Ed", "Financial Services",
    "Government – Federal", "Government – Local", "Government – State", "Grocery",
    "Healthcare", "Manufacturing", "Oil & Gas – Downstream", "Oil & Gas – Midstream",
    "Oil & Gas – Upstream", "Retail", "Technology", "Utilities", "Other (manual input)"
]
industry = st.selectbox("", industries)

# -----------------------------
# Step 2: AI-generated General Pressure Type (GPT)
# -----------------------------
st.markdown("<div class='step-label'>Step 2: Select General Pressure Type</div>", unsafe_allow_html=True)
gpt_options = []
if industry:
    with st.spinner("Analyzing industry..."):
        gpt_prompt = f"""
        List 6 concise General Pressure Types (1-2 words each, comma separated) facing the {industry} industry.
        """
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        gpt_text = gpt_response.choices[0].message.content.strip()
        gpt_options = [opt.strip() for opt in gpt_text.split(",")][:6]

gpt_selected = st.selectbox("", gpt_options) if gpt_options else None

# -----------------------------
# Step 3: AI-generated Specific Pressure Type (SPT)
# -----------------------------
st.markdown("<div class='step-label'>Step 3: Select Specific Pressure Type</div>", unsafe_allow_html=True)
spt_options = []
if gpt_selected:
    with st.spinner("Generating specific pressures..."):
        spt_prompt = f"""
        Based on the {industry} industry and the General Pressure Type '{gpt_selected}', return 4 concise Specific Pressure Types (1-3 words each).
        """
        spt_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": spt_prompt}]
        )
        spt_text = spt_response.choices[0].message.content.strip()
        spt_options = [opt.strip() for opt in spt_text.split("\n") if opt.strip()][:4]

spt_selected = st.selectbox("", spt_options) if spt_options else None

# -----------------------------
# Step 4: Generate Pressure Grid
# -----------------------------
st.markdown("<div class='step-label'>Step 4: Generate Pressure Grid</div>", unsafe_allow_html=True)
generate_grid = st.button("Generate Pressure Grid", key="generate_grid", help="Click to generate a 4-row Pressure Grid.", type="primary")

# -----------------------------
# Step 5: Show Grid with Buttons
# -----------------------------
if generate_grid and spt_selected:
    with st.spinner("Building Pressure Grid..."):
        grid_prompt = f"""
        Based on the {industry} industry and Specific Pressure Type '{spt_selected}', create a 4-row Pressure Grid with the following columns:
        - Industry Driver (short phrase)
        - KPI (1 per row)
        - Observed Effects (brief summary)
        - Industry Solution (what companies try)
        - Narrative Opportunity (strategic framing)
        - Emotional State (with 1-sentence explanation)

        Return this as a table with rows numbered 1 to 4.
        """
        grid_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": grid_prompt}]
        )
        st.markdown(grid_response.choices[0].message.content)

# -----------------------------
# Step 6: Navigation
# -----------------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("Refresh")
with col2:
    st.button("Back")
with col3:
    st.button("Forward")

