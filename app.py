import streamlit as st

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="WineHouse Wine Finder",
    layout="wide"
)

# ---------------------------------------------------------
# SIMPLE WINEHOUSE STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #6f1734;
    }

    div.stButton > button {
        background-color: #7a1f3d;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        min-height: 46px;
    }

    div.stButton > button:hover {
        background-color: #5e142f;
        color: white;
    }

    .wine-card {
        padding: 18px;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        margin-bottom: 12px;
        background-color: #ffffff;
    }

    .wine-label {
        color: #737373;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .wine-name {
        color: #6f1734;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .wine-details {
        color: #333333;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# DATA
#
# IMPORTANT:
# This is temporary synthetic demonstration data.
# Later we will replace this with your real Azure data.
#
# Pictures:
# If image is None, the app simply shows no picture.
#
# Later we can add:
# "image": "images/wine-name.jpg"
# ---------------------------------------------------------

wines = [

    # GREEK WINES & MEZE

    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "13 March 2026",
        "name": "Santorini Assyrtiko",
        "type": "White",
        "country": "Greece",
        "style": "Dry",
        "notes": "crisp citrus lemon mineral salty fresh",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "13 March 2026",
        "name": "Moschofilero",
        "type": "White",
        "country": "Greece",
        "style": "Aromatic",
        "notes": "floral rose citrus light fresh",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "13 March 2026",
        "name": "Agiorgitiko",
        "type": "Red",
        "country": "Greece",
        "style": "Medium-bodied",
        "notes": "red berries cherry soft spice",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "13 March 2026",
        "name": "Xinomavro",
        "type": "Red",
        "country": "Greece",
        "style": "Full-bodied",
        "notes": "dark fruit tomato herbs earthy tannins",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "13 March 2026",
        "name": "Greek Rosé",
        "type": "Rosé",
        "country": "Greece",
        "style": "Dry",
        "notes": "strawberry watermelon fresh light",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "13 March 2026",
        "name": "Mavrodaphne",
        "type": "Dessert",
        "country": "Greece",
        "style": "Sweet",
        "notes": "raisins dried fruit caramel sweet",
        "status": "Proposed",
        "image": None
    },

    # ITALIAN SUMMER WINES

    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "10 July 2026",
        "name": "Pinot Grigio",
        "type": "White",
        "country": "Italy",
        "style": "Light",
        "notes": "pear citrus crisp light refreshing",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "10 July 2026",
        "name": "Vermentino",
        "type": "White",
        "country": "Italy",
        "style": "Dry",
        "notes": "lemon herbs mineral salty fresh",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "10 July 2026",
        "name": "Prosecco",
        "type": "Sparkling",
        "country": "Italy",
        "style": "Fresh",
        "notes": "apple pear floral light bubbles",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "10 July 2026",
        "name": "Chianti Classico",
        "type": "Red",
        "country": "Italy",
        "style": "Medium-bodied",
        "notes": "cherry herbs red fruit earthy",
        "status": "Proposed",
        "image": None
    },

    {

