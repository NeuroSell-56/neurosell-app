
import streamlit as st
import openai

# Use OpenAI API key securely from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ----------------------------
# App Layout Configuration
# ----------------------------
st.set_page_config(page_title="NeuroSell Industry Decoder™", layout="wide")
st.markdown("## NeuroSell Industry Decoder™ – Industry Preferences + Pressure Grid")
st.markdown("Use the dropdowns below to decode industry pressures and generate strategic narratives.")

# ----------------------------
# Step 1: Industry Dropdown
# ----------------------------
industries = [
    "Agriculture", "Education – K-12 & Higher Ed", "Financial Services",
    "Government – Federal", "Government – Local", "Government – State", "Grocery",
    "Healthcare", "Manufacturing", "Oil & Gas – Downstream", "Oil & Gas – Midstream",
    "Oil & Gas – Upstream", "Retail", "Technology", "Utilities", "Other (manual input)"
]
industry = st.selectbox("Step 1: Select Industry", industries)

# ----------------------------
# Step 2: AI-Generated General Pressure Types
# ----------------------------
if industry:
    if "general_pressures" not in st.session_state:
        with st.spinner("Generating General Pressure Types..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert business analyst."},
                    {"role": "user", "content": f"List the 6 most current General Pressure Types facing the {industry} industry."}
                ]
            )
            st.session_state.general_pressures = response.choices[0].message.content.split("\n")

    general_pressure = st.selectbox("Step 2: Select General Pressure Type", st.session_state.general_pressures)

# ----------------------------
# Step 3: AI-Generated Specific Pressure Types
# ----------------------------
if industry and general_pressure:
    if "specific_pressures" not in st.session_state:
        with st.spinner("Generating Specific Pressure Types..."):
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert industry strategist."},
                    {"role": "user", "content": f"List 4 current Specific Pressure Types under the General Pressure '{general_pressure}' in the {industry} industry."}
                ]
            )
            st.session_state.specific_pressures = response.choices[0].message.content.split("\n")

    specific_pressure = st.selectbox("Step 3: Select Specific Pressure Type", st.session_state.specific_pressures)

# ----------------------------
# Step 4: Generate Pressure Grid
# ----------------------------
if industry and general_pressure and specific_pressure:
    if st.button("Step 4: Generate Pressure Grid"):
        with st.spinner("Creating AI-generated Pressure Grid..."):
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a sales enablement strategist building a pressure grid."},
                    {"role": "user", "content": f"Build a 4-row Pressure Grid for the {industry} industry under '{general_pressure}' > '{specific_pressure}'. Each row must include: Industry Driver, KPI(s), Observed Effects, Considered Solutions, Narrative Opportunity, Emotional State. Format it clearly."}
                ]
            )
            st.session_state.pressure_grid = response.choices[0].message.content

# ----------------------------
# Display Pressure Grid
# ----------------------------
if "pressure_grid" in st.session_state:
    st.markdown("### 🧠 AI-Populated Pressure Grid")
    st.text_area("Pressure Grid Output", value=st.session_state.pressure_grid, height=300)

# ----------------------------
# Global Controls
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Refresh"):
        st.session_state.clear()
with col2:
    st.button("⬅️ Back")
with col3:
    st.button("➡️ Forward")
