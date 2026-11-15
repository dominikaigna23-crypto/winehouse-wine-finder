import streamlit as st
import json
from google import genai


# =========================================================
# SETTINGS
# =========================================================

st.set_page_config(
    page_title="WineHouse Wine Finder",
    layout="wide"
)

UNKNOWN = "I don't remember"


# =========================================================
# GEMINI AI
# =========================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def interpret_with_ai(description):

    if not description.strip():
        return None

    prompt = f"""
You are the AI interpretation component of a wine search application.

A user is trying to identify a wine from a tasting.

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

Instructions:

- Do not guess a specific wine.
- Do not invent information that the user did not imply.
- You may translate everyday language into useful wine characteristics.
- Example: "not heavy" may mean "light".
- Example: "cherries" may become "cherry".
- Example: "fresh and lemony" may become ["fresh", "lemon", "citrus"].
- Example: "kind of salty" may become ["salty", "mineral"].
- If colour, country or style cannot reasonably be inferred, return an empty string.
- Keep flavour terms short.
- Return JSON only.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return json.loads(text)

    except Exception:
        return None


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #6d1835;
    }

    div.stButton > button {
        background-color: #751d3b;
        color: white;
        border: none;
        border-radius: 6px;
        min-height: 48px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #57142c;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TEMPORARY DEMONSTRATION DATA
#
# We will replace this with the real Azure records later.
#
# Add a picture later like:
# "image": "images/chianti.jpg"
# =========================================================

wines = [

    # -----------------------------------------------------
    # GREEK WINES & MEZE
    # -----------------------------------------------------

    {
        "event": "13 March 2026 | Greek Wines & Meze",
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
        "name": "Xinomavro",
        "type": "Red",
        "country": "Greece",
        "style": "Full-bodied",
        "notes": "dark fruit herbs earthy tannins",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "13 March 2026 | Greek Wines & Meze",
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
        "name": "Mavrodaphne",
        "type": "Dessert",
        "country": "Greece",
        "style": "Sweet",
        "notes": "raisins dried fruit caramel sweet",
        "status": "Proposed",
        "image": None
    },


    # -----------------------------------------------------
    # ITALIAN SUMMER WINES
    # -----------------------------------------------------

    {
        "event": "10 July 2026 | Italian Summer Wines",
        "name": "Pinot Grigio",
        "type": "White",
        "country": "Italy",
        "style": "Light",
        "notes": "pear citrus crisp refreshing",
        "status": "Proposed",
        "image": None
    },

    {
        "event": "10 July 2026 | Italian Summer Wines",
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
        "name": "Italian Rosato",
        "type": "Rosé",
        "country": "Italy",
        "style": "Dry",
        "notes": "strawberry peach fresh summer",
        "status": "Proposed",
        "image": None
    },


    # -----------------------------------------------------
    # AUTUMN REDS
    # -----------------------------------------------------

    {
        "event": "9 October 2026 | Autumn Reds",
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
        "name": "Côtes du Rhône",
        "type": "Red",
        "country": "France",
        "style": "Medium-bodied",
        "notes": "black fruit pepper herbs spice",
        "status": "Proposed",
        "image": None
    }

]


# =========================================================
# MATCHING FUNCTIONS
# =========================================================

def normalise(value):
    return str(value).lower().strip()


def calculate_match(
    wine,
    selected_type,
    selected_country,
    selected_style,
    ai_description
):

    score = 0
    reasons = []


    # -----------------------------------------------------
    # TYPE
    # -----------------------------------------------------

    if selected_type != UNKNOWN:

        if normalise(wine["type"]) == normalise(selected_type):

            score += 5

            reasons.append(
                f"matches the selected {wine['type']} type"
            )

        else:
            score -= 3


    # -----------------------------------------------------
    # COUNTRY
    # -----------------------------------------------------

    if selected_country != UNKNOWN:

        if normalise(wine["country"]) == normalise(
            selected_country
        ):

            score += 5

            reasons.append(
                f"matches {wine['country']}"
            )

        else:
            score -= 3


    # -----------------------------------------------------
    # STYLE
    # -----------------------------------------------------

    if selected_style != UNKNOWN:

        if normalise(selected_style) in normalise(
            wine["style"]
        ):

            score += 4

            reasons.append(
                f"matches the {wine['style']} style"
            )

        else:
            score -= 1


    # -----------------------------------------------------
    # AI-INTERPRETED DESCRIPTION
    # -----------------------------------------------------

    if ai_description.strip():

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
            for word in normalise(
                ai_description
            ).split()
            if len(
                word.strip(".,!?;:")
            ) >= 3
        ]

        matched_words = []

        for word in words:

            if word in searchable_text:

                score += 2

                matched_words.append(word)


        if matched_words:

            unique_words = list(
                dict.fromkeys(matched_words)
            )

            reasons.append(
                "matching characteristics: "
                + ", ".join(unique_words[:5])
            )


    return score, reasons


# =========================================================
# DISPLAY WINE
# =========================================================

def show_wine(
    wine,
    number=None,
    reasons=None,
    confidence=None
):

    picture, details = st.columns(
        [1, 3]
    )


    with picture:

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
                    border:1px solid #dddddd;
                    border-radius:8px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    text-align:center;
                    color:#888888;
                    background:#fafafa;
                ">
                    Wine image<br>coming soon
                </div>
                """,
                unsafe_allow_html=True
            )


    with details:

        if number:
            st.caption(
                f"Match {number}"
            )

        st.markdown(
            f"### {wine['name']}"
        )

        st.write(
            f"{wine['type']} | "
            f"{wine['country']} | "
            f"{wine['style']}"
        )

        st.write(
            f"**Tasting:** "
            f"{wine['event']}"
        )

        st.write(
            f"**Tasting characteristics:** "
            f"{wine['notes']}"
        )


        if reasons:

            st.write(
                "**Why this may match:** "
                + "; ".join(reasons)
            )


        if confidence:

            st.write(
                f"**Match confidence:** "
                f"{confidence}"
            )


        st.caption(
            "Event-wine record status: "
            + wine["status"]
        )


# =========================================================
# HEADER
# =========================================================

st.title(
    "WineHouse Wine Finder"
)

st.write(
    "Find a wine from a WineHouse tasting using "
    "whatever details you remember."
)

st.caption(
    "You do not need to remember everything. "
    "Choose 'I don't remember' whenever you are unsure."
)

st.divider()


# =========================================================
# STEP 1 - TASTING
# =========================================================

st.subheader(
    "1. Do you remember the tasting?"
)


event_names = sorted(
    set(
        wine["event"]
        for wine in wines
    )
)


selected_event = st.selectbox(
    "Tasting date and theme",
    [UNKNOWN] + event_names
)


if selected_event != UNKNOWN:

    candidate_wines = [
        wine
        for wine in wines
        if wine["event"]
        == selected_event
    ]


    st.success(
        f"{len(candidate_wines)} wines "
        "are linked to this tasting."
    )


    with st.expander(
        "View wines from this tasting"
    ):

        for wine in candidate_wines:

            show_wine(wine)

            st.divider()


else:

    candidate_wines = wines

    st.info(
        "That's fine. The search will use "
        "all available tasting-wine records."
    )


st.divider()


# =========================================================
# STEP 2 - REMEMBERED DETAILS
# =========================================================

st.subheader(
    "2. What do you remember about the wine?"
)


column1, column2 = st.columns(2)


with column1:

    wine_types = sorted(
        set(
            wine["type"]
            for wine in wines
        )
    )


    selected_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + wine_types
    )


    countries = sorted(
        set(
            wine["country"]
            for wine in wines
        )
    )


    selected_country = st.selectbox(
        "Country of origin",
        [UNKNOWN] + countries
    )


with column2:

    styles = sorted(
        set(
            wine["style"]
            for wine in wines
        )
    )


    selected_style = st.selectbox(
        "Style",
        [UNKNOWN] + styles
    )


    description = st.text_area(
        "Describe anything else you remember",
        placeholder=(
            "For example: it was light and fruity, "
            "tasted like cherries, and I think "
            "it was Italian."
        ),
        height=110
    )


st.caption(
    "The description box uses AI to interpret "
    "everyday language into wine characteristics."
)


st.divider()


# =========================================================
# STEP 3 - FIND MATCH
# =========================================================

st.subheader(
    "3. Find the wine"
)


if st.button(
    "Find likely matches",
    type="primary",
    use_container_width=True
):


    # -----------------------------------------------------
    # CHECK HOW MUCH INFORMATION WE HAVE
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # NO INFORMATION
    # -----------------------------------------------------

    if remembered_details == 0:

        st.warning(
            "There is not enough information "
            "to identify a likely wine yet. "
            "Add at least one detail you remember."
        )


    else:

        # =================================================
        # AI INTERPRETATION
        # =================================================

        ai_clues = interpret_with_ai(
            description
        )


        ai_words = []


        if ai_clues:

            if ai_clues.get("colour"):

                ai_words.append(
                    ai_clues["colour"]
                )


            if ai_clues.get("country"):

                ai_words.append(
                    ai_clues["country"]
                )


            if ai_clues.get("style"):

                ai_words.append(
                    ai_clues["style"]
                )


            ai_words.extend(
                ai_clues.get(
                    "flavours",
                    []
                )
            )


            ai_words.extend(
                ai_clues.get(
                    "other_clues",
                    []
                )
            )


            ai_description = " ".join(
                ai_words
            )


        else:

            ai_description = description


        # =================================================
        # OPTIONAL: SHOW WHAT AI UNDERSTOOD
        # =================================================

        if description.strip():

            with st.expander(
                "What the AI understood"
            ):

                if ai_clues:

                    colour = (
                        ai_clues.get(
                            "colour"
                        )
                        or "Not identified"
                    )

                    country = (
                        ai_clues.get(
                            "country"
                        )
                        or "Not identified"
                    )

                    style = (
                        ai_clues.get(
                            "style"
                        )
                        or "Not identified"
                    )

                    flavours = (
                        ai_clues.get(
                            "flavours"
                        )
                        or []
                    )


                    st.write(
                        f"**Colour/type:** "
                        f"{colour}"
                    )

                    st.write(
                        f"**Country:** "
                        f"{country}"
                    )

                    st.write(
                        f"**Style:** "
                        f"{style}"
                    )

                    st.write(
                        "**Flavour clues:** "
                        + (
                            ", ".join(flavours)
                            if flavours
                            else "Not identified"
                        )
                    )


                else:

                    st.write(
                        "AI interpretation was not "
                        "available, so the original "
                        "description was used."
                    )


        # =================================================
        # SEARCH THE WINE RECORDS
        # =================================================

        results = []


        for wine in candidate_wines:

            score, reasons = calculate_match(
                wine,
                selected_type,
                selected_country,
                selected_style,
                ai_description
            )


            results.append(
                {
                    "wine": wine,
                    "score": score,
                    "reasons": reasons
                }
            )


        results.sort(
            key=lambda item:
            item["score"],
            reverse=True
        )


        positive_results = [
            result
            for result in results
            if result["score"] > 0
        ]


        # =================================================
        # NO MATCH
        # =================================================

        if not positive_results:

            st.warning(
                "No confident match was found "
                "with those details. Try removing "
                "one detail or describing another "
                "taste, smell or characteristic."
            )


        # =================================================
        # RESULTS
        # =================================================

        else:

            st.markdown(
                "## Likely matches"
            )


            st.write(
                "The results below combine the information "
                "you selected with the characteristics "
                "interpreted from your description."
            )


            top_results = (
                positive_results[:3]
            )


            for position, result in enumerate(
                top_results,
                start=1
            ):

                score = result["score"]


                if score >= 11:

                    confidence = (
                        "Strong possible match"
                    )


                elif score >= 6:

                    confidence = (
                        "Possible match"
                    )


                else:

                    confidence = (
                        "Weak possible match"
                    )


                with st.container(
                    border=True
                ):

                    show_wine(
                        result["wine"],
                        number=position,
                        reasons=result["reasons"],
                        confidence=confidence
                    )


            st.info(
                "These are possible matches rather "
                "than guaranteed identifications. "
                "The tasting records may contain "
                "synthetic or proposed wine selections. "
                "Current bottle availability should "
                "be checked separately."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "WineHouse Wine Finder | "
    "Data and AI prototype"
)
