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
MODEL_NAME = "gemini-4-hydrogen"


# =========================================================
# GEMINI CONNECTION
# =========================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================================================
# VISUAL STYLE
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

    .wine-image-placeholder {
        height: 190px;
        border: 1px solid #dddddd;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #888888;
        background: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TEMPORARY DEMONSTRATION DATA
#
# These records will later be replaced with exported Azure
# Events + EventProducts + Products data.
#
# Each event currently has six demonstration wines.
# =========================================================

wines = [

    # GREEK WINES & MEZE

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

    # ITALIAN SUMMER WINES

    {
        "event": "10 July 2026 | Italian Summer Wines",
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

    # AUTUMN REDS

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
# HELPER FUNCTIONS
# =========================================================

def normalise(value):
    return str(value).strip().lower()


def filter_candidates(
    selected_event,
    selected_type,
    selected_country,
    selected_style
):
    candidates = wines.copy()

    if selected_event != UNKNOWN:
        candidates = [
            wine for wine in candidates
            if wine["event"] == selected_event
        ]

    if selected_type != UNKNOWN:
        candidates = [
            wine for wine in candidates
            if normalise(wine["type"]) == normalise(selected_type)
        ]

    if selected_country != UNKNOWN:
        candidates = [
            wine for wine in candidates
            if normalise(wine["country"]) == normalise(selected_country)
        ]

    if selected_style != UNKNOWN:
        candidates = [
            wine for wine in candidates
            if normalise(wine["style"]) == normalise(selected_style)
        ]

    return candidates


def rank_wines_with_ai(description, candidates):

    candidate_data = []

    for wine in candidates:
        candidate_data.append(
            {
                "name": wine["name"],
                "event": wine["event"],
                "type": wine["type"],
                "country": wine["country"],
                "style": wine["style"],
                "notes": wine["notes"],
                "record_status": wine["status"]
            }
        )

    candidate_json = json.dumps(
        candidate_data,
        ensure_ascii=False,
        indent=2
    )

    prompt = (
        "You are the matching engine for the WineHouse Wine Finder. "
        "A person is trying to identify a wine using an imperfect memory. "
        "You must rank only the candidate wines supplied below. "
        "Do not invent wine names. Do not use outside knowledge to add "
        "products that are not in the supplied records. "
        "Use semantic reasoning, not just exact word matching. "
        "Consider similar concepts, for example: "
        "not heavy can mean light-bodied; zesty can relate to citrus; "
        "salty can relate to mineral; dark fruit can relate to plum or "
        "blackberry. However, do not claim details absent from the records. "
        "\n\n"
        "Person's description:\n"
        + description
        + "\n\n"
        "Candidate wine records:\n"
        + candidate_json
        + "\n\n"
        "Return ONLY valid JSON in the following structure:\n"
        "{"
        '"enough_information": true,'
        '"clarifying_question": "",'
        '"matches": ['
        "{"
        '"name": "exact candidate name",'
        '"confidence": "Strong possible match",'
        '"reason": "brief explanation based only on stored record details"'
        "}"
        "]"
        "}"
        "\n\n"
        "Rules:\n"
        "1. Return no more than three matches.\n"
        "2. Use the exact candidate wine names supplied.\n"
        "3. Valid confidence values are: Strong possible match, "
        "Possible match, Weak possible match.\n"
        "4. Rank the strongest match first.\n"
        "5. Explanations must mention stored characteristics that support "
        "or weaken the match.\n"
        "6. If the description is too vague to rank responsibly, set "
        "enough_information to false, return an empty matches list, and "
        "ask one simple clarifying question.\n"
        "7. Do not claim that a wine is currently in stock.\n"
        "8. Return JSON only."
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            raise ValueError("The AI returned an empty response.")

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        result = json.loads(text)

        if not isinstance(result, dict):
            raise ValueError("The AI response was not a JSON object.")

        return result

    except Exception as error:
        st.error(f"AI matching error: {error}")
        return None


def validate_ai_matches(ai_result, candidates):

    if not ai_result:
        return []

    allowed_wines = {
        normalise(wine["name"]): wine
        for wine in candidates
    }

    validated = []
    seen_names = set()

    for result in ai_result.get("matches", []):

        result_name = normalise(
            result.get("name", "")
        )

        if result_name not in allowed_wines:
            continue

        if result_name in seen_names:
            continue

        confidence = result.get(
            "confidence",
            "Possible match"
        )

        valid_confidences = [
            "Strong possible match",
            "Possible match",
            "Weak possible match"
        ]

        if confidence not in valid_confidences:
            confidence = "Possible match"

        reason = result.get(
            "reason",
            "The candidate matches some of the remembered details."
        )

        validated.append(
            {
                "wine": allowed_wines[result_name],
                "confidence": confidence,
                "reason": reason
            }
        )

        seen_names.add(result_name)

        if len(validated) == 3:
            break

    return validated


def show_wine(
    wine,
    number=None,
    confidence=None,
    reason=None
):

    picture_column, details_column = st.columns(
        [1, 3]
    )

    with picture_column:

        if wine.get("image"):
            st.image(
                wine["image"],
                use_container_width=True
            )
        else:
            st.markdown(
                """
                <div class="wine-image-placeholder">
                    Wine image<br>coming soon
                </div>
                """,
                unsafe_allow_html=True
            )

    with details_column:

        if number is not None:
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
            f"**Stored characteristics:** {wine['notes']}"
        )

        if reason:
            st.write(
                f"**Why this may match:** {reason}"
            )

        if confidence:
            st.write(
                f"**Match confidence:** {confidence}"
            )

        st.caption(
            f"Event-wine record status: {wine['status']}"
        )


# =========================================================
# HEADER
# =========================================================

st.title("WineHouse Wine Finder")

st.write(
    "Find a wine from a WineHouse tasting using "
    "the details you remember."
)

st.caption(
    "Choose 'I don't remember' whenever you are unsure. "
    "The AI ranks only wines contained in the available "
    "WineHouse tasting records."
)

st.divider()


# =========================================================
# STEP 1: TASTING
# =========================================================

st.subheader("1. Do you remember the tasting?")

event_names = sorted(
    set(wine["event"] for wine in wines)
)

selected_event = st.selectbox(
    "Tasting date and theme",
    [UNKNOWN] + event_names
)

if selected_event != UNKNOWN:

    event_wines = [
        wine for wine in wines
        if wine["event"] == selected_event
    ]

    st.success(
        f"{len(event_wines)} wines are linked "
        "to this tasting record."
    )

    with st.expander(
        "View wines from this tasting"
    ):
        for wine in event_wines:
            show_wine(wine)
            st.divider()

else:
    st.info(
        "The tasting is unknown, so the finder can search "
        "across all available tasting-wine records."
    )

st.divider()


# =========================================================
# STEP 2: REMEMBERED DETAILS
# =========================================================

st.subheader(
    "2. What do you remember about the wine?"
)

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

    description = st.text_area(
        "Describe what you remember",
        placeholder=(
            "For example: it was not very heavy, "
            "with cherry and earthy flavours. "
            "It seemed smooth and possibly Italian."
        ),
        height=125
    )

st.caption(
    "The filters identify eligible database records. "
    "The AI then compares and ranks those actual wines "
    "using the description."
)

st.divider()


# =========================================================
# STEP 3: AI MATCHING
# =========================================================

st.subheader("3. Find the wine")

if st.button(
    "Find likely matches",
    type="primary",
    use_container_width=True
):

    supplied_details = 0

    if selected_event != UNKNOWN:
        supplied_details += 1

    if selected_type != UNKNOWN:
        supplied_details += 1

    if selected_country != UNKNOWN:
        supplied_details += 1

    if selected_style != UNKNOWN:
        supplied_details += 1

    if description.strip():
        supplied_details += 1

    if supplied_details == 0:

        st.warning(
            "There is not enough information to search yet. "
            "Add at least one detail."
        )

    else:

        candidates = filter_candidates(
            selected_event,
            selected_type,
            selected_country,
            selected_style
        )

        if not candidates:

            st.warning(
                "No WineHouse records match all the selected "
                "filters. Try changing one answer to "
                "'I don't remember'."
            )

        elif not description.strip():

            st.write(
                f"The selected filters leave "
                f"{len(candidates)} possible wine records."
            )

            st.warning(
                "Please describe at least one taste, smell, "
                "texture or other detail so the AI can rank them."
            )

            with st.expander(
                "View remaining candidate wines"
            ):
                for wine in candidates:
                    show_wine(wine)
                    st.divider()

        else:

            st.write(
                f"AI is comparing your description with "
                f"{len(candidates)} eligible wine records."
            )

            with st.spinner(
                "Comparing the description with WineHouse records..."
            ):

                ai_result = rank_wines_with_ai(
                    description,
                    candidates
                )

            if ai_result:

                enough_information = ai_result.get(
                    "enough_information",
                    True
                )

                if not enough_information:

                    st.warning(
                        "There is not enough detail for a "
                        "responsible match."
                    )

                    clarifying_question = ai_result.get(
                        "clarifying_question",
                        ""
                    )

                    if clarifying_question:
                        st.write(
                            f"**One helpful question:** "
                            f"{clarifying_question}"
                        )

                else:

                    matches = validate_ai_matches(
                        ai_result,
                        candidates
                    )

                    if not matches:

                        st.warning(
                            "The AI did not return a valid match "
                            "from the supplied WineHouse records. "
                            "Try adding one more detail."
                        )

                    else:

                        st.markdown("## Likely matches")

                        st.write(
                            "These wines were ranked by AI, but "
                            "every result comes from the eligible "
                            "WineHouse records supplied to the model."
                        )

                        for position, match in enumerate(
                            matches,
                            start=1
                        ):

                            with st.container(border=True):

                                show_wine(
                                    match["wine"],
                                    number=position,
                                    confidence=match["confidence"],
                                    reason=match["reason"]
                                )

                        clarifying_question = ai_result.get(
                            "clarifying_question",
                            ""
                        )

                        if clarifying_question:
                            st.write(
                                f"**A detail that could improve "
                                f"the result:** "
                                f"{clarifying_question}"
                            )

                        st.info(
                            "These are possible matches, not "
                            "guaranteed identifications. Some event "
                            "wine lists are synthetic or proposed. "
                            "Current availability must be checked "
                            "separately."
                        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "WineHouse Wine Finder | Data and AI prototype"
)
