import streamlit as st
import openai

# Set your OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="NeuroSell Industry Decoder™",
    layout="wide",
    initial_sidebar_state="auto"
)

# -------------------------
# Styling: Branded Colors & Logo
# -------------------------
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
    .stSelectbox label {
        font-weight: bold;
        font-size: 1.1rem;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Logo + Title
# -------------------------
st.image("https://raw.githubusercontent.com/NeuroSell-56/neurosell-assets/main/NeuroSell_AI_Official_Logo.png", width=300)
st.markdown("## NeuroSell Industry Decoder™ – Industry Preferences + Pressure Grid")
st.markdown("Use the dropdowns below to decode industry pressures and generate strategic narratives.")

# -------------------------
# Step 1: Select Industry
# -------------------------
st.markdown("### Step 1: Select Industry")
industries = [
    "Agriculture", "Education – K-12 & Higher Ed", "Financial Services", "Government – Federal",
    "Government – Local", "Government – State", "Grocery", "Healthcare", "Manufacturing",
    "Oil & Gas – Downstream", "Oil & Gas – Midstream", "Oil & Gas – Upstream",
    "Retail", "Technology", "Utilities", "Other (manual input)"
]
industry = st.selectbox("Select an Industry", [""] + industries)

# Placeholder session state
if "gpt_options" not in st.session_state:
    st.session_state["gpt_options"] = []
if "spt_options" not in st.session_state:
    st.session_state["spt_options"] = []

# -------------------------
# Step 2: Generate GPT Options from AI
# -------------------------
if industry:
    st.markdown("### Step 2: Select General Pressure Type")
    if not st.session_state["gpt_options"]:
        with st.spinner("Generating General Pressure Types..."):
            gpt_response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert business strategist."},
                    {"role": "user", "content": f"List six high-level general pressure types (1–2 words each) currently affecting the {industry} industry. Only return the list."}
                ]
            )
            st.session_state["gpt_options"] = [item.strip() for item in gpt_response['choices'][0]['message']['content'].split('\n') if item.strip()]
    gpt = st.selectbox("Select General Pressure Type", [""] + st.session_state["gpt_options"])
else:
    gpt = ""

# -------------------------
# Step 3: Generate SPT Options from AI
# -------------------------
if industry and gpt:
    st.markdown("### Step 3: Select Specific Pressure Type")
    if not st.session_state["spt_options"]:
        with st.spinner("Generating Specific Pressure Types..."):
            spt_response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a strategic industry analyst."},
                    {"role": "user", "content": f"Based on the {gpt} pressure in the {industry} industry, list four specific pressure types (1–3 words each). Only return the list."}
                ]
            )
            st.session_state["spt_options"] = [item.strip() for item in spt_response['choices'][0]['message']['content'].split('\n') if item.strip()]
    spt = st.selectbox("Select Specific Pressure Type", [""] + st.session_state["spt_options"])
else:
    spt = ""

# -------------------------
# Step 4: Generate Pressure Grid (Trigger Button)
# -------------------------
if industry and gpt and spt:
    st.markdown("### Step 4: Generate Pressure Grid")
    if st.button("Generate Pressure Grid", type="primary"):
        st.session_state["generate_grid"] = True

# -------------------------
# Step 5: AI-Populate Pressure Grid
# -------------------------
if st.session_state.get("generate_grid"):
    st.markdown("### Step 5: Industry Pressure Grid")
    with st.spinner("Generating Pressure Grid..."):
        grid_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a strategic sales advisor."},
                {"role": "user", "content": f"Create a 4-row Pressure Grid for the {industry} industry facing {gpt} → {spt}. Each row should contain:\n\n- Industry Driver\n- KPI(s)\n- Observed Effects\n- Industry Solution\n- Narrative Opportunity\n- Emotional State (and short explanation).\n\nReturn in a structured markdown table."}
            ]
        )
        st.markdown(grid_response['choices'][0]['message']['content'])

# -------------------------
# Step 6: Continue to Reframe Tone
# -------------------------
if st.session_state.get("generate_grid"):
    st.markdown("### Step 6: Generate Reframe Tone")
    if st.button("Next: Generate Reframed Narrative"):
        st.success("Proceeding to Screen 2 (Reframe Tone)... [not yet implemented]")
