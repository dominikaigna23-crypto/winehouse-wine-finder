import streamlit as st
import json
from google import genai


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="WineHouse Wine Finder",
    layout="wide"
)

UNKNOWN = "I don't remember"


# =========================================================
# GEMINI AI CONNECTION
# =========================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def interpret_with_ai(description):

    if not description.strip():
        return None

    prompt = f"""
You are the AI interpretation component of a wine search application.

The user is trying to identify a wine from a WineHouse tasting.

The user wrote:

"{description}"

Interpret the description into useful wine characteristics.

Return ONLY valid JSON in exactly this structure:

{{
    "colour": "",
    "country": "",
    "style": "",
    "flavours": [],
    "other_clues": []
}}

Rules:

- Do not guess a specific wine.
- Do not invent facts the user did not imply.
- Translate everyday language into useful wine characteristics
