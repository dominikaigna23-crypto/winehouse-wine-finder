import streamlit as st
import json
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "10 July 2026",
        "name": "Valpolicella",
        "type": "Red",
        "country": "Italy",
        "style": "Light",
        "notes": "sour cherry red berries light soft",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "10 July 2026",
        "name": "Italian Rosato",
        "type": "Rosé",
        "country": "Italy",
        "style": "Dry",
        "notes": "strawberry peach fresh summer",
        "status": "Proposed",
        "image": None
    },

    # AUTUMN REDS

    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "9 October 2026",
        "name": "Primitivo",
        "type": "Red",
        "country": "Italy",
        "style": "Full-bodied",
        "notes": "plum blackberry jam spice rich",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "9 October 2026",
        "name": "Italian Pinot Noir",
        "type": "Red",
        "country": "Italy",
        "style": "Light",
        "notes": "cherry raspberry earthy light",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "9 October 2026",
        "name": "French Pinot Noir",
        "type": "Red",
        "country": "France",
        "style": "Light",
        "notes": "red berries cherry mushroom earthy",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "9 October 2026",
        "name": "Rioja Reserva",
        "type": "Red",
        "country": "Spain",
        "style": "Full-bodied",
        "notes": "dark cherry vanilla oak spice",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "9 October 2026",
        "name": "Malbec",
        "type": "Red",
        "country": "Argentina",
        "style": "Full-bodied",
        "notes": "blackberry plum chocolate rich",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "9 October 2026",
        "name": "Côtes du Rhône",
        "type": "Red",
        "country": "France",
        "style": "Medium-bodied",
        "notes": "black fruit pepper herbs spice",
        "status": "Proposed",
        "image": None
    }
]


def interpret_with_ai(description):
    if not description.strip():
        return None

    prompt = f"""
You are helping a wine search system interpret a user's memory of a wine.

The user wrote:
"{description}"

Extract useful wine characteristics from the description.

Return ONLY valid JSON in exactly this format:
{{
    "colour": "",
    "country": "",
    "style": "",
    "flavours": [],
    "other_clues": []
}}

Rules:
- Do not identify or invent a specific wine.
- Only extract or reasonably interpret characteristics from the user's description.
- If something is unknown, use an empty string or empty list.
- Keep flavour words short and useful for matching wine records.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception:
        return None


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------

def normalise(value):
    return str(value).lower().strip()


def calculate_match(
    wine,
    selected_type,
    selected_country,
    selected_style,
    description
):
    score = 0
    reasons = []

    # Wine type
    if selected_type != UNKNOWN:
        if normalise(wine["type"]) == normalise(selected_type):
            score += 4
            reasons.append(wine["type"])
        else:
            score -= 2

    # Country
    if selected_country != UNKNOWN:
        if normalise(wine["country"]) == normalise(selected_country):
            score += 4
            reasons.append(wine["country"])
        else:
            score -= 2

    # Style
    if selected_style != UNKNOWN:
        if normalise(selected_style) in normalise(wine["style"]):
            score += 3
            reasons.append(wine["style"])

    # Free-text description
    if description.strip():

        searchable_text = normalise(
            wine["name"]
            + " "
            + wine["type"]
            + " "
            + wine["country"]
            + " "
            + wine["style"]
            + " "
            + wine["notes"]
        )

        words = [
            word.strip(".,!?;:")
            for word in normalise(description).split()
            if len(word.strip(".,!?;:")) >= 3
        ]

        matched_words = []

        for word in words:
            if word in searchable_text:
                score += 2
                matched_words.append(word)

        if matched_words:
            reasons.append(
                "matching notes: "
                + ", ".join(matched_words[:5])
            )

    return score, reasons


def show_wine(wine, number=None, reasons=None, confidence=None):

    image_column, text_column = st.columns([1, 3])

    with image_column:

        if wine.get("image"):
            st.image(
                wine["image"],
                use_container_width=True
            )
        else:
            st.markdown(
                """
                <div style="
                    height:190px;
                    border:1px solid #e2e2e2;
                    border-radius:8px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:#999999;
                    background:#fafafa;
                    text-align:center;
                    padding:15px;
                ">
                    Wine image<br>coming soon
                </div>
                """,
                unsafe_allow_html=True
            )

    with text_column:

        if number:
            st.caption(f"Match {number}")

        st.markdown(f"### {wine['name']}")

        st.write(
            f"{wine['type']} | "
            f"{wine['country']} | "
            f"{wine['style']}"
        )

        st.write(
            f"**Tasting:** {wine['event']}"
        )

        st.write(
            f"**Tasting notes:** {wine['notes']}"
        )

        if reasons:
            st.write(
                "**Why this may match:** "
                + "; ".join(reasons)
            )

        if confidence:
            st.write(
                f"**Match confidence:** {confidence}"
            )

        st.caption(
            f"Event-wine record status: {wine['status']}"
        )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("WineHouse Wine Finder")

st.write(
    "Trying to find a wine from a WineHouse tasting? "
    "Choose the details you remember and the Wine Finder "
    "will search the available tasting records for possible matches."
)

st.caption(
    "You do not need to remember every detail. "
    "Choose 'I don't remember' whenever you are unsure."
)

st.divider()


# ---------------------------------------------------------
# STEP 1 - TASTING
# ---------------------------------------------------------

st.subheader("1. Do you remember the tasting?")

event_names = sorted(
    set(wine["event"] for wine in wines)
)

selected_event = st.selectbox(
    "Tasting date and theme",
    [UNKNOWN] + event_names
)


if selected_event != UNKNOWN:

    candidate_wines = [
        wine
        for wine in wines
        if wine["event"] == selected_event
    ]

    st.write(
        f"**{len(candidate_wines)} wines are linked "
        "to this tasting record.**"
    )

    with st.expander(
        "View wines from this tasting",
        expanded=True
    ):

        for wine in candidate_wines:
            show_wine(wine)
            st.divider()

else:

    candidate_wines = wines

    st.info(
        "No problem. The Wine Finder will search across "
        "all available tasting-wine records."
    )


st.divider()


# ---------------------------------------------------------
# STEP 2 - DETAILS
# ---------------------------------------------------------

st.subheader("2. What do you remember about the wine?")

column1, column2 = st.columns(2)


with column1:

    wine_types = sorted(
        set(wine["type"] for wine in wines)
    )

    selected_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + wine_types
    )


    countries = sorted(
        set(wine["country"] for wine in wines)
    )

    selected_country = st.selectbox(
        "Country of origin",
        [UNKNOWN] + countries
    )


with column2:

    styles = sorted(
        set(wine["style"] for wine in wines)
    )

    selected_style = st.selectbox(
        "Style",
        [UNKNOWN] + styles
    )


    description = st.text_input(
        "Taste, smell or anything else you remember",
        placeholder=(
            "For example: cherry, citrus, mineral, "
            "light, sweet, spicy..."
        )
    )


st.divider()


# ---------------------------------------------------------
# STEP 3 - SEARCH
# ---------------------------------------------------------

st.subheader("3. Find the wine")


if st.button(
    "Find likely matches",
    type="primary",
    use_container_width=True
):

    remembered_details = 0

    if selected_event != UNKNOWN:
        remembered_details += 1

    if selected_type != UNKNOWN:
        remembered_details += 1

    if selected_country != UNKNOWN:
        remembered_details += 1

    if selected_style != UNKNOWN:
        remembered_details += 1

    if description.strip():
        remembered_details += 1


    # Nothing remembered
    if remembered_details == 0:

        st.warning(
            "There isn't enough information to identify "
            "a likely wine yet. Add at least one detail "
            "you remember."
        )


    else:

        results = []

        for wine in candidate_wines:

            score, reasons = calculate_match(
                wine,
                selected_type,
                selected_country,
                selected_style,
                description
            )

            results.append(
                {
                    "wine": wine,
                    "score": score,
                    "reasons": reasons
                }
            )


        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )


        positive_results = [
            result
            for result in results
            if result["score"] > 0
        ]


        if not positive_results:

            st.warning(
                "No confident match was found with those details. "
                "Try removing one detail or entering another "
                "taste, smell or style you remember."
            )


        else:

            st.markdown("## Likely matches")

            st.write(
                "These results are ranked using the details "
                "you entered and the available tasting records."
            )


            top_results = positive_results[:3]


            for position, result in enumerate(
                top_results,
                start=1
            ):

                score = result["score"]

                if score >= 9:
                    confidence = "Strong possible match"

                elif score >= 5:
                    confidence = "Possible match"

                else:
                    confidence = "Weak possible match"


                with st.container(border=True):

                    show_wine(
                        result["wine"],
                        number=position,
                        reasons=result["reasons"],
                        confidence=confidence
                    )


            st.info(
                "The Wine Finder provides possible matches, "
                "not a guaranteed identification. "
                "Tasting records may include proposed or synthetic "
                "event-wine selections. Current bottle availability "
                "should be checked separately."
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "WineHouse Wine Finder | Data and AI project prototype"
)
