import html
import json

import pandas as pd
import streamlit as st
from google import genai


# =========================================================
# SETTINGS
# =========================================================

st.set_page_config(
    page_title="WineHouse Wine Finder",
    layout="wide",
    initial_sidebar_state="collapsed"
)

UNKNOWN = "I don't remember"
MODEL_NAME = "gemini-4-hydrogen"


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --wine: #6b1f38;
        --dark-wine: #3d101f;
        --soft-wine: #8c3b55;
        --cream: #f7f1e8;
        --paper: #fffdf9;
        --gold: #b79555;
        --light-gold: #d9c69c;
        --text: #2a2022;
        --muted: #766c6e;
        --border: #e5d9cd;
    }

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(183, 149, 85, 0.12),
                transparent 28rem
            ),
            linear-gradient(
                180deg,
                #fffdf9 0%,
                #f7f1e8 100%
            );
        color: var(--text);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2.3rem;
        padding-bottom: 5rem;
    }

    h1, h2, h3 {
        font-family: Georgia, "Times New Roman", serif;
        color: var(--dark-wine);
        letter-spacing: -0.02em;
    }

    p, label, div, button, input, textarea {
        font-family: Arial, Helvetica, sans-serif;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 50px 54px;
        border-radius: 25px;
        background:
            linear-gradient(
                115deg,
                rgba(55, 10, 27, 0.99),
                rgba(112, 30, 56, 0.94)
            );
        color: white;
        box-shadow: 0 24px 65px rgba(64, 16, 31, 0.22);
        margin-bottom: 30px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 290px;
        height: 290px;
        right: -70px;
        top: -115px;
        border: 1px solid rgba(217, 198, 156, 0.35);
        border-radius: 50%;
        box-shadow:
            0 0 0 35px rgba(217, 198, 156, 0.06),
            0 0 0 70px rgba(217, 198, 156, 0.035);
    }

    .hero-label,
    .section-label {
        color: var(--gold);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero-label {
        color: var(--light-gold);
        margin-bottom: 13px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(2.5rem, 6vw, 4.3rem);
        line-height: 1.02;
        margin: 0 0 17px 0;
        max-width: 720px;
    }

    .hero p {
        color: rgba(255, 255, 255, 0.82);
        font-size: 1.05rem;
        line-height: 1.72;
        max-width: 700px;
        margin: 0;
    }

    .age-card {
        max-width: 700px;
        margin: 70px auto 24px auto;
        padding: 54px 46px;
        border-radius: 27px;
        background:
            linear-gradient(
                145deg,
                rgba(55, 10, 27, 0.99),
                rgba(110, 29, 55, 0.97)
            );
        color: white;
        text-align: center;
        box-shadow: 0 30px 85px rgba(64, 16, 31, 0.30);
    }

    .age-card h1 {
        color: white;
        font-size: 3.1rem;
        margin: 12px 0 17px 0;
    }

    .age-card p {
        color: rgba(255, 255, 255, 0.82);
        line-height: 1.7;
    }

    .age-label {
        color: var(--light-gold);
        font-size: 0.78rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .section-label {
        margin-top: 26px;
        margin-bottom: 3px;
    }

    .information-box {
        padding: 16px 18px;
        border-radius: 13px;
        background: #f7f0df;
        border-left: 4px solid var(--gold);
        color: #5c4d31;
        line-height: 1.58;
        font-size: 0.91rem;
        margin: 18px 0;
    }

    .wine-card {
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 19px;
        padding: 21px;
        margin: 14px 0;
        box-shadow: 0 10px 27px rgba(64, 16, 31, 0.06);
    }

    .wine-visual {
        min-height: 185px;
        border-radius: 15px;
        background:
            radial-gradient(
                circle at 50% 28%,
                rgba(217, 198, 156, 0.38),
                transparent 30%
            ),
            linear-gradient(145deg, #eee1d2, #fbf7f0);
        border: 1px solid #e1d4c3;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: var(--wine);
        text-align: center;
        padding: 18px;
    }

    .bottle {
        width: 47px;
        height: 76px;
        border-radius: 7px 7px 15px 15px;
        background: linear-gradient(180deg, #7e2b46, #3e101f);
        margin: 18px 0 13px 0;
        position: relative;
        box-shadow: 0 13px 22px rgba(64, 16, 31, 0.22);
    }

    .bottle::before {
        content: "";
        position: absolute;
        width: 15px;
        height: 28px;
        left: 16px;
        top: -24px;
        border-radius: 4px 4px 0 0;
        background: #3e101f;
    }

    .bottle-label {
        position: absolute;
        width: 32px;
        height: 25px;
        left: 8px;
        top: 30px;
        border-radius: 3px;
        background: #eee2ca;
        border: 1px solid #c7ac75;
    }

    .wine-visual-name {
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1.35;
    }

    .tag {
        display: inline-block;
        padding: 5px 10px;
        margin: 3px 5px 5px 0;
        border-radius: 999px;
        background: #f1e5df;
        color: var(--wine);
        font-size: 0.77rem;
        font-weight: 700;
    }

    div.stButton > button {
        min-height: 51px;
        border-radius: 11px;
        border: 1px solid var(--wine);
        background: var(--wine);
        color: white;
        font-weight: 700;
        transition: all 0.18s ease;
    }

    div.stButton > button:hover {
        background: var(--dark-wine);
        border-color: var(--dark-wine);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 10px 23px rgba(64, 16, 31, 0.18);
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.7;
        margin-top: 48px;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 35px 27px;
        }

        .age-card {
            padding: 38px 25px;
            margin-top: 30px;
        }

        .age-card h1 {
            font-size: 2.4rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# AGE GATE
# =========================================================

if "age_confirmed" not in st.session_state:
    st.session_state.age_confirmed = False

if "age_declined" not in st.session_state:
    st.session_state.age_declined = False


if not st.session_state.age_confirmed:

    st.markdown(
        """
        <div class="age-card">
            <div class="age-label">WineHouse</div>
            <h1>Are you 18 or older?</h1>
            <p>
                This website contains information about alcoholic beverages.
                Please confirm that you are at least 18 years old before
                entering the WineHouse Wine Finder.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    yes_column, no_column = st.columns(2)

    with yes_column:
        if st.button(
            "Yes, I am 18 or older",
            type="primary",
            use_container_width=True
        ):
            st.session_state.age_confirmed = True
            st.session_state.age_declined = False
            st.rerun()

    with no_column:
        if st.button(
            "No, I am under 18",
            use_container_width=True
        ):
            st.session_state.age_declined = True

    if st.session_state.age_declined:
        st.warning(
            "You must be 18 or older to enter the WineHouse Wine Finder."
        )

    st.stop()


# =========================================================
# GEMINI CONNECTION
# =========================================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception as error:
    st.error(
        "The AI service could not be initialized. "
        f"Technical detail: {error}"
    )
    st.stop()


# =========================================================
# LOAD ALL EVENT-PRODUCT RECORDS
# =========================================================

@st.cache_data
def load_wine_data():

    dataframe = pd.read_csv(
        "winehouse_data.csv"
    )

    # Notes is optional because Azure may omit a completely
    # empty Notes column when exporting the query result.
    required_columns = [
        "EventID",
        "EventDateKey",
        "Theme",
        "CalendarStatus",
        "ProductID",
        "ProductName",
        "BeverageType",
        "CountryOrOrigin",
        "Style",
        "ProductStatus",
        "SequenceNo",
        "SelectionStatus"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing CSV columns: "
            + ", ".join(missing_columns)
        )

    if "Notes" not in dataframe.columns:
        dataframe["Notes"] = ""

    for column in dataframe.columns:
        dataframe[column] = (
            dataframe[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    dataframe["EventDate"] = pd.to_datetime(
        dataframe["EventDateKey"],
        format="%Y%m%d",
        errors="coerce"
    )

    dataframe["FormattedDate"] = (
        dataframe["EventDate"]
        .dt.strftime("%d %B %Y")
        .fillna(dataframe["EventDateKey"])
    )

    dataframe["EventLabel"] = (
        dataframe["FormattedDate"]
        + " | "
        + dataframe["Theme"]
    )

    # IMPORTANT:
    # Do not filter by BeverageType here.
    # Every event-product relationship from the CSV is retained.
    dataframe["DisplayType"] = (
        dataframe["BeverageType"]
        .replace("", "Wine")
    )

    return dataframe.sort_values(
        [
            "EventDate",
            "SequenceNo",
            "ProductName"
        ]
    )


try:
    wine_data = load_wine_data()
except Exception as error:
    st.error(
        "The WineHouse data file could not be loaded. "
        "Make sure winehouse_data.csv is in the same GitHub "
        "repository as app.py. "
        f"Technical detail: {error}"
    )
    st.stop()


# =========================================================
# HELPERS
# =========================================================

def safe_text(value):
    return html.escape(str(value))


def dataframe_to_candidates(dataframe):

    candidates = []

    for _, row in dataframe.iterrows():

        event_id = str(row["EventID"])
        product_id = str(row["ProductID"])

        candidates.append(
            {
                "record_id": event_id + "|" + product_id,
                "event_id": event_id,
                "event": row["EventLabel"],
                "event_status": row["CalendarStatus"],
                "product_id": product_id,
                "name": row["ProductName"],
                "type": row["DisplayType"],
                "country": row["CountryOrOrigin"],
                "style": row["Style"],
                "product_status": row["ProductStatus"],
                "selection_status": row["SelectionStatus"],
                "notes": row["Notes"]
            }
        )

    return candidates


def filter_candidate_data(
    dataframe,
    selected_event,
    selected_type,
    selected_country
):

    filtered = dataframe.copy()

    if selected_event != UNKNOWN:
        filtered = filtered[
            filtered["EventLabel"] == selected_event
        ]

    if selected_type != UNKNOWN:
        filtered = filtered[
            filtered["DisplayType"].str.lower()
            == selected_type.lower()
        ]

    if selected_country != UNKNOWN:
        filtered = filtered[
            filtered["CountryOrOrigin"].str.lower()
            == selected_country.lower()
        ]

    return filtered


def clean_json_response(text):

    cleaned = str(text).strip()

    if cleaned.startswith("```"):
        cleaned = (
            cleaned
            .replace("```json", "")
            .replace("```JSON", "")
            .replace("```", "")
            .strip()
        )

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if (
        first_brace != -1
        and last_brace > first_brace
    ):
        cleaned = cleaned[
            first_brace:last_brace + 1
        ]

    return cleaned


# =========================================================
# AI RANKING
# =========================================================

def rank_wines_with_ai(
    description,
    candidates
):

    compact_candidates = []

    for candidate in candidates:
        compact_candidates.append(
            {
                "record_id": candidate["record_id"],
                "name": candidate["name"],
                "event": candidate["event"],
                "beverage_type": candidate["type"],
                "country": candidate["country"],
                "style": candidate["style"],
                "product_status": candidate["product_status"],
                "selection_status": candidate["selection_status"],
                "notes": candidate["notes"]
            }
        )

    candidate_json = json.dumps(
        compact_candidates,
        ensure_ascii=False
    )

    prompt = f"""
You are the matching engine for the WineHouse Wine Finder.

A person is trying to identify a wine using an imperfect memory.
Compare the description with ONLY the supplied WineHouse records.

DESCRIPTION:
{description}

ELIGIBLE WINEHOUSE RECORDS:
{candidate_json}

Return ONLY valid JSON in this structure:

{{
  "enough_information": true,
  "clarifying_question": "",
  "matches": [
    {{
      "record_id": "exact supplied record_id",
      "confidence": "Strong possible match",
      "reason": "Short explanation based only on supplied record details"
    }}
  ]
}}

Rules:

1. Return no more than three matches.
2. Use only exact record_id values supplied above.
3. Do not invent a product, event, origin, style, note or stock claim.
4. Rank by semantic similarity, not only exact word matching.
5. Valid confidence values:
   Strong possible match
   Possible match
   Weak possible match
6. Explain which stored details support the match.
7. Mention an important mismatch when relevant.
8. If the description is too vague, set enough_information to false,
   return an empty matches list, and ask one short question.
9. Product presence does not prove current stock.
10. Proposed status does not prove historical service.
11. Return JSON only.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            raise ValueError(
                "The AI returned an empty response."
            )

        result = json.loads(
            clean_json_response(
                response.text
            )
        )

        if not isinstance(result, dict):
            raise ValueError(
                "The AI response was not a JSON object."
            )

        return result

    except Exception as error:
        st.error(
            "AI matching could not be completed. "
            f"Technical detail: {error}"
        )
        return None


def validate_matches(
    ai_result,
    candidates
):

    allowed_records = {
        candidate["record_id"]: candidate
        for candidate in candidates
    }

    valid_confidences = [
        "Strong possible match",
        "Possible match",
        "Weak possible match"
    ]

    validated = []
    used_ids = set()

    for result in ai_result.get("matches", []):

        record_id = str(
            result.get("record_id", "")
        ).strip()

        if record_id not in allowed_records:
            continue

        if record_id in used_ids:
            continue

        confidence = str(
            result.get(
                "confidence",
                "Possible match"
            )
        ).strip()

        if confidence not in valid_confidences:
            confidence = "Possible match"

        reason = str(
            result.get(
                "reason",
                "This record matches some of the remembered details."
            )
        ).strip()

        validated.append(
            {
                "wine": allowed_records[record_id],
                "confidence": confidence,
                "reason": reason
            }
        )

        used_ids.add(record_id)

        if len(validated) == 3:
            break

    return validated


# =========================================================
# DISPLAY
# =========================================================

def wine_visual(name):

    st.markdown(
        f"""
        <div class="wine-visual">
            <div class="bottle">
                <div class="bottle-label"></div>
            </div>
            <div class="wine-visual-name">
                {safe_text(name)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_wine(
    wine,
    match_number=None,
    confidence=None,
    reason=None
):

    st.markdown(
        '<div class="wine-card">',
        unsafe_allow_html=True
    )

    visual_column, details_column = st.columns(
        [1, 3]
    )

    with visual_column:
        wine_visual(wine["name"])

    with details_column:

        if match_number is not None:
            st.caption(f"MATCH {match_number}")

        st.markdown(f"### {wine['name']}")

        tags = [
            wine["type"],
            wine["country"],
            wine["style"]
        ]

        tag_html = ""

        for item in tags:
            if str(item).strip():
                tag_html += (
                    '<span class="tag">'
                    + safe_text(item)
                    + "</span>"
                )

        st.markdown(
            tag_html,
            unsafe_allow_html=True
        )

        st.write(
            f"**Tasting:** {wine['event']}"
        )

        if wine["notes"]:
            st.write(
                f"**Stored notes:** {wine['notes']}"
            )

        if reason:
            st.write(
                f"**Why this may match:** {reason}"
            )

        if confidence:
            st.write(
                f"**Confidence:** {confidence}"
            )

        if wine["product_status"]:
            st.caption(
                "Product status: "
                + wine["product_status"]
            )

        if wine["selection_status"]:
            st.caption(
                "Event-product status: "
                + wine["selection_status"]
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <section class="hero">
        <div class="hero-label">
            WineHouse discovery
        </div>
        <h1>Find the wine you remember.</h1>
        <p>
            Select any details you know, describe the wine in your own
            words, and let AI compare your memory with the available
            WineHouse tasting and product records.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="information-box">
        This prototype uses synthetic and proposed project records.
        Results are possible matches rather than guaranteed
        identifications. Current availability must be checked separately.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STEP 1
# =========================================================

st.markdown(
    '<div class="section-label">Step one</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Choose the tasting, if remembered"
)

event_options = (
    wine_data[
        ["EventLabel", "EventDate"]
    ]
    .drop_duplicates()
    .sort_values("EventDate")["EventLabel"]
    .tolist()
)

selected_event = st.selectbox(
    "Tasting date and theme",
    [UNKNOWN] + event_options
)

if selected_event != UNKNOWN:

    event_data = wine_data[
        wine_data["EventLabel"]
        == selected_event
    ]

    st.success(
        f"{len(event_data)} product records are linked "
        "to this tasting."
    )

    with st.expander(
        "View products linked to this tasting"
    ):

        event_candidates = dataframe_to_candidates(
            event_data
        )

        for candidate in event_candidates:
            show_wine(candidate)

else:

    st.info(
        "The tasting is optional. If it is unknown, "
        "the finder searches across all available "
        "WineHouse event-product records."
    )


# =========================================================
# STEP 2
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">Step two</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Add the details you remember"
)

left_column, right_column = st.columns(2)

with left_column:

    product_types = sorted(
        value
        for value in wine_data[
            "DisplayType"
        ].unique().tolist()
        if str(value).strip()
    )

    selected_type = st.selectbox(
        "Wine or beverage type",
        [UNKNOWN] + product_types
    )

    countries = sorted(
        value
        for value in wine_data[
            "CountryOrOrigin"
        ].unique().tolist()
        if str(value).strip()
    )

    selected_country = st.selectbox(
        "Country or origin",
        [UNKNOWN] + countries
    )

with right_column:

    description = st.text_area(
        "Describe the wine in your own words",
        placeholder=(
            "For example: it was a light red, smooth rather "
            "than heavy, with cherries and something earthy."
        ),
        height=175
    )

    st.caption(
        "Useful clues include colour, sweetness, body, fruit, "
        "spices, flowers, minerals, bubbles, food pairing or date."
    )


# =========================================================
# STEP 3
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">Step three</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Ask AI to compare the records"
)

if st.button(
    "Find likely matches",
    type="primary",
    use_container_width=True
):

    details_supplied = sum(
        [
            selected_event != UNKNOWN,
            selected_type != UNKNOWN,
            selected_country != UNKNOWN,
            bool(description.strip())
        ]
    )

    if details_supplied == 0:

        st.warning(
            "Please provide at least one detail before searching."
        )

    else:

        filtered_data = filter_candidate_data(
            wine_data,
            selected_event,
            selected_type,
            selected_country
        )

        if filtered_data.empty:

            st.warning(
                "No WineHouse records match every selected filter. "
                "Change one answer to 'I don't remember' and try again."
            )

        elif not description.strip():

            st.warning(
                "The filters found possible records, but the AI needs "
                "at least one taste, smell, texture or other clue."
            )

            st.write(
                f"**Remaining eligible records:** "
                f"{len(filtered_data)}"
            )

        else:

            candidates = dataframe_to_candidates(
                filtered_data
            )

            st.write(
                f"AI is comparing your description with "
                f"**{len(candidates)} eligible WineHouse records**."
            )

            with st.spinner(
                "Comparing your description with the records..."
            ):

                ai_result = rank_wines_with_ai(
                    description,
                    candidates
                )

            if ai_result:

                if not ai_result.get(
                    "enough_information",
                    True
                ):

                    st.warning(
                        "There is not enough information "
                        "for a responsible match."
                    )

                    question = str(
                        ai_result.get(
                            "clarifying_question",
                            ""
                        )
                    ).strip()

                    if question:
                        st.write(
                            f"**One useful question:** {question}"
                        )

                else:

                    matches = validate_matches(
                        ai_result,
                        candidates
                    )

                    if not matches:

                        st.warning(
                            "The AI did not return a valid match "
                            "from the eligible records. "
                            "Try adding another detail."
                        )

                    else:

                        st.markdown(
                            "## Your likely matches"
                        )

                        st.write(
                            "Every result below comes from the "
                            "records loaded from winehouse_data.csv."
                        )

                        for position, match in enumerate(
                            matches,
                            start=1
                        ):

                            show_wine(
                                match["wine"],
                                match_number=position,
                                confidence=match["confidence"],
                                reason=match["reason"]
                            )

                        question = str(
                            ai_result.get(
                                "clarifying_question",
                                ""
                            )
                        ).strip()

                        if question:
                            st.info(
                                "A detail that could improve the result: "
                                + question
                            )

                        st.markdown(
                            """
                            <div class="information-box">
                                Please verify the event record before relying
                                on a match. Project records may contain
                                proposed selections, and catalogue presence
                                does not confirm current availability.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        WineHouse Wine Finder<br>
        Data and AI project prototype · Synthetic project records
    </div>
    """,
    unsafe_allow_html=True
)
