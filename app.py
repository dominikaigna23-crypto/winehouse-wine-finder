import html
import json

import pandas as pd
import streamlit as st
from google import genai


# =========================================================
# APPLICATION SETTINGS
# =========================================================

st.set_page_config(
    page_title="WineHouse Wine Finder",
    layout="wide",
    initial_sidebar_state="collapsed"
)

UNKNOWN = "I don't remember"

# This is the model available through the Google AI Studio
# account used for this project.
MODEL_NAME = "gemini-4-hydrogen"


# =========================================================
# WEBSITE DESIGN
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --wine: #6b1f38;
        --wine-dark: #38101e;
        --wine-soft: #8b3d56;
        --cream: #f7f1e8;
        --paper: #fffdf9;
        --gold: #b79555;
        --gold-light: #dbc99f;
        --text: #292022;
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
        max-width: 1080px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    h1, h2, h3 {
        font-family: Georgia, "Times New Roman", serif;
        color: var(--wine-dark);
        letter-spacing: -0.02em;
    }

    p, label, input, textarea, button, div {
        font-family: Arial, Helvetica, sans-serif;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 52px 55px;
        border-radius: 26px;
        background:
            linear-gradient(
                115deg,
                rgba(53, 9, 25, 0.99),
                rgba(113, 30, 57, 0.94)
            );
        color: white;
        box-shadow: 0 24px 65px rgba(64, 16, 31, 0.22);
        margin-bottom: 30px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        right: -75px;
        top: -120px;
        border: 1px solid rgba(219, 201, 159, 0.35);
        border-radius: 50%;
        box-shadow:
            0 0 0 38px rgba(219, 201, 159, 0.055),
            0 0 0 76px rgba(219, 201, 159, 0.03);
    }

    .hero-label {
        color: var(--gold-light);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 13px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(2.5rem, 6vw, 4.3rem);
        line-height: 1.03;
        max-width: 720px;
        margin: 0 0 17px 0;
    }

    .hero p {
        color: rgba(255, 255, 255, 0.82);
        font-size: 1.06rem;
        line-height: 1.72;
        max-width: 700px;
        margin: 0;
    }

    .age-card {
        max-width: 700px;
        margin: 70px auto 24px auto;
        padding: 55px 48px;
        border-radius: 27px;
        background:
            linear-gradient(
                145deg,
                rgba(53, 9, 25, 0.99),
                rgba(110, 29, 55, 0.97)
            );
        color: white;
        text-align: center;
        box-shadow: 0 30px 85px rgba(64, 16, 31, 0.30);
    }

    .age-card h1 {
        color: white;
        font-size: 3.1rem;
        margin: 12px 0 18px 0;
    }

    .age-card p {
        color: rgba(255, 255, 255, 0.82);
        line-height: 1.72;
    }

    .age-label {
        color: var(--gold-light);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }

    .section-label {
        color: var(--gold);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-top: 27px;
        margin-bottom: 3px;
    }

    .notice {
        padding: 16px 18px;
        border-radius: 13px;
        background: #f7f0df;
        border-left: 4px solid var(--gold);
        color: #5c4d31;
        line-height: 1.6;
        margin: 18px 0;
        font-size: 0.91rem;
    }

    .wine-card {
        background: rgba(255, 253, 249, 0.96);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 23px 25px;
        margin: 14px 0;
        box-shadow: 0 10px 27px rgba(64, 16, 31, 0.06);
    }

    .wine-number {
        color: var(--gold);
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .wine-name {
        font-family: Georgia, "Times New Roman", serif;
        color: var(--wine-dark);
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.22;
        margin-bottom: 10px;
    }

    .tag {
        display: inline-block;
        padding: 6px 11px;
        margin: 3px 5px 10px 0;
        border-radius: 999px;
        background: #f1e5df;
        color: var(--wine);
        font-size: 0.77rem;
        font-weight: 700;
    }

    .wine-detail {
        color: var(--text);
        line-height: 1.62;
        margin-top: 8px;
    }

    .confidence-strong {
        color: #386c4c;
        font-weight: 700;
    }

    .confidence-possible {
        color: #88631e;
        font-weight: 700;
    }

    .confidence-weak {
        color: #8b493d;
        font-weight: 700;
    }

    .record-summary {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 13px;
        margin: 18px 0;
    }

    .summary-card {
        background: rgba(255, 253, 249, 0.92);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 16px;
    }

    .summary-number {
        font-family: Georgia, "Times New Roman", serif;
        color: var(--wine);
        font-size: 1.55rem;
        font-weight: 700;
    }

    .summary-label {
        color: var(--muted);
        font-size: 0.78rem;
        margin-top: 4px;
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
        background: var(--wine-dark);
        border-color: var(--wine-dark);
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
        margin-top: 50px;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 36px 27px;
        }

        .age-card {
            padding: 39px 25px;
            margin-top: 30px;
        }

        .age-card h1 {
            font-size: 2.4rem;
        }

        .record-summary {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# AGE CONFIRMATION
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
# GOOGLE GEMINI
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
# LOAD THE CLEAN CSV
# =========================================================

@st.cache_data
def load_wine_data():

    dataframe = pd.read_csv(
        "winehouse_data.csv"
    )

    required_columns = [
        "EventID",
        "EventDateKey",
        "Theme",
        "ProductID",
        "ProductName",
        "BeverageType",
        "CountryOrOrigin",
        "Style"
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

    for column in required_columns:

        dataframe[column] = (
            dataframe[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Convert the date key, for example 20260313,
    # to an actual date displayed as 13 March 2026.
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

    # The dropdown is built only from real event fields:
    # EventID, date and theme.
    dataframe["EventLabel"] = (
        dataframe["FormattedDate"]
        + " | "
        + dataframe["Theme"]
    )

    # This application identifies wine.
    # Spirit products and their spirit-only events are excluded.
    dataframe = dataframe[
        dataframe["BeverageType"]
        .str.lower()
        .eq("wine")
    ].copy()

    if dataframe.empty:

        raise ValueError(
            "The CSV does not contain any rows where "
            "BeverageType is Wine."
        )

    # Extract the first part of Style as the general type.
    # Example: "Red, dry, rich" becomes "Red".
    dataframe["WineType"] = (
        dataframe["Style"]
        .str.split(",")
        .str[0]
        .str.strip()
    )

    dataframe.loc[
        dataframe["WineType"] == "",
        "WineType"
    ] = "Wine"

    # Remove accidental duplicate event-product rows.
    dataframe = dataframe.drop_duplicates(
        subset=[
            "EventID",
            "ProductID"
        ]
    )

    return dataframe.sort_values(
        [
            "EventDate",
            "EventID",
            "ProductName"
        ]
    )


try:

    wine_data = load_wine_data()

except Exception as error:

    st.error(
        "The WineHouse data file could not be loaded. "
        "Make sure the new clean file is named "
        "winehouse_data.csv and is in the same GitHub "
        "repository as app.py. "
        f"Technical detail: {error}"
    )

    st.stop()


# =========================================================
# BASIC HELPERS
# =========================================================

def safe_text(value):

    return html.escape(
        str(value)
    )


def normalise(value):

    return str(value).strip().lower()


def event_table_from_data(dataframe):

    # One row per event.
    # Products are not treated as events.
    return (
        dataframe[
            [
                "EventID",
                "EventDate",
                "FormattedDate",
                "Theme",
                "EventLabel"
            ]
        ]
        .drop_duplicates(
            subset=["EventID"]
        )
        .sort_values(
            [
                "EventDate",
                "EventID"
            ]
        )
        .reset_index(drop=True)
    )


events = event_table_from_data(
    wine_data
)


def products_for_event(
    dataframe,
    event_id
):

    # Correct relationship:
    # take EventID from the events list,
    # then find product rows with that EventID.
    return dataframe[
        dataframe["EventID"]
        == event_id
    ].copy()


def dataframe_to_candidates(
    dataframe
):

    candidates = []

    for _, row in dataframe.iterrows():

        event_id = str(
            row["EventID"]
        )

        product_id = str(
            row["ProductID"]
        )

        candidates.append(
            {
                "record_id": (
                    event_id
                    + "|"
                    + product_id
                ),
                "event_id": event_id,
                "event_date": row["FormattedDate"],
                "event_theme": row["Theme"],
                "event_label": row["EventLabel"],
                "product_id": product_id,
                "name": row["ProductName"],
                "beverage_type": row["BeverageType"],
                "country": row["CountryOrOrigin"],
                "style": row["Style"],
                "wine_type": row["WineType"]
            }
        )

    return candidates


def filter_candidate_data(
    dataframe,
    selected_event_id,
    selected_type,
    selected_country
):

    filtered = dataframe.copy()

    # If an event is known, get only products connected
    # to that exact EventID.
    if selected_event_id:

        filtered = filtered[
            filtered["EventID"]
            == selected_event_id
        ]

    if selected_type != UNKNOWN:

        filtered = filtered[
            filtered["WineType"]
            .str.lower()
            == selected_type.lower()
        ]

    if selected_country != UNKNOWN:

        filtered = filtered[
            filtered["CountryOrOrigin"]
            .str.lower()
            == selected_country.lower()
        ]

    return filtered


def clean_json_response(
    response_text
):

    cleaned = str(
        response_text
    ).strip()

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
# AI MATCHING
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
                "event_id": candidate["event_id"],
                "event_date": candidate["event_date"],
                "event_theme": candidate["event_theme"],
                "product_id": candidate["product_id"],
                "product_name": candidate["name"],
                "country": candidate["country"],
                "style": candidate["style"]
            }
        )

    candidate_json = json.dumps(
        compact_candidates,
        ensure_ascii=False
    )

    prompt = f"""
You are the matching engine for the WineHouse Wine Finder.

A person is trying to identify a wine using an imperfect memory.

The application has already selected eligible records from the
WineHouse event-product dataset.

Compare the person's description only with those eligible records.

PERSON'S DESCRIPTION:
{description}

ELIGIBLE EVENT-PRODUCT RECORDS:
{candidate_json}

Return ONLY valid JSON with this exact structure:

{{
  "enough_information": true,
  "clarifying_question": "",
  "matches": [
    {{
      "record_id": "exact supplied record_id",
      "confidence": "Strong possible match",
      "reason": "Short explanation based only on supplied record fields"
    }}
  ]
}}

Rules:

1. Return no more than three matches.
2. Use only exact record_id values supplied above.
3. Never invent a product, event, origin, style or tasting note.
4. Never add a wine that is not in the eligible records.
5. Rank using semantic similarity, not only exact word matching.
6. Treat everyday descriptions reasonably:
   not heavy may mean light;
   powerful may mean rich or full-bodied;
   sweet may relate to sweet or semi-sweet;
   bubbles may relate to sparkling or Champagne.
7. Valid confidence values are:
   Strong possible match
   Possible match
   Weak possible match
8. Explain which supplied fields support the match.
9. Mention a meaningful mismatch when relevant.
10. If the description is too vague:
    set enough_information to false,
    return an empty matches list,
    and ask one short clarifying question.
11. Do not claim current stock availability.
12. Return JSON only.
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

        if not isinstance(
            result,
            dict
        ):

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

    accepted_confidence = [
        "Strong possible match",
        "Possible match",
        "Weak possible match"
    ]

    validated_matches = []
    used_ids = set()

    for item in ai_result.get(
        "matches",
        []
    ):

        record_id = str(
            item.get(
                "record_id",
                ""
            )
        ).strip()

        # The result is rejected unless that exact record
        # was supplied from the CSV.
        if record_id not in allowed_records:
             continue

        if record_id in used_ids:
            continue

        confidence = str(
            item.get(
                "confidence",
                "Possible match"
            )
        ).strip()

        if confidencenot in accepted_confidence:
            confidence = "Possible match"

        reason = str(
            item.get(
                "reason",
                "This product matches some of the remembered details."
            )
        ).strip()

        validated_matches.append(
            {
                "wine": allowed_records[
                    record_id
                ],
                "confidence": confidence,
                "reason": reason
            }
        )

        used_ids.add(
            record_id
        )

        if len(validated_matches) == 3:
            break

    return validated_matches


# =========================================================
# WINE RESULT DISPLAY
# =========================================================

def confidence_css(
    confidence
):

    if confidence == "Strong possible match":
        return "confidence-strong"

    if confidence == "Weak possible match":
        return "confidence-weak"

    return "confidence-possible"


def show_wine(
    wine,
    match_number=None,
    confidence=None,
    reason=None
):

    if match_number is not None:

        number_html = (
            '<div class="wine-number">'
            + "Match "
            + safe_text(match_number)
            + "</div>"
        )

    else:

        number_html = ""

    tags = [
        wine["wine_type"],
        wine["country"],
        wine["style"]
    ]

    tag_html = ""

    for tag in tags:

        if str(tag).strip():

            tag_html += (
                '<span class="tag">'
                + safe_text(tag)
                + "</span>"
            )

    reason_html = ""

    if reason:

        reason_html = (
            '<div class="wine-detail">'
            "<strong>Why this may match:</strong> "
            + safe_text(reason)
            + "</div>"
        )

    confidence_html = ""

    if confidence:

        confidence_html = (
            '<div class="wine-detail">'
            "<strong>Confidence:</strong> "
            '<span class="'
            + confidence_css(confidence)
            + '">'
            + safe_text(confidence)
            + "</span>"
            + "</div>"
        )

    st.markdown(
        f"""
        <div class="wine-card">
            {number_html}
            <div class="wine-name">
                {safe_text(wine["name"])}
            </div>
            <div>
                {tag_html}
            </div>
            <div class="wine-detail">
                <strong>Tasting:</strong>
                {safe_text(wine["event_label"])}
            </div>
            <div class="wine-detail">
                <strong>Product ID:</strong>
                {safe_text(wine["product_id"])}
            </div>
            {reason_html}
            {confidence_html}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PAGE INTRODUCTION
# =========================================================

st.markdown(
    """
    <section class="hero">
        <div class="hero-label">
            WineHouse discovery
        </div>
        <h1>Find the wine you remember.</h1>
        <p>
            Choose the tasting if known, add any details you remember,
            and let AI compare the description with the real event-product
            relationships in the WineHouse project dataset.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="notice">
        This is a prototype using synthetic project data.
        Event-product records are used for demonstration and do not prove
        that a bottle was historically served or is currently in stock.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATA SUMMARY
# =========================================================

unique_event_count = events["EventID"].nunique()
unique_product_count = wine_data["ProductID"].nunique()
relationship_count = len(wine_data)

st.markdown(
    f"""
    <div class="record-summary">
        <div class="summary-card">
            <div class="summary-number">
                {unique_event_count}
            </div>
            <div class="summary-label">
                Wine tasting events
            </div>
        </div>
        <div class="summary-card">
            <div class="summary-number">
                {unique_product_count}
            </div>
            <div class="summary-label">
                Unique wine products
            </div>
        </div>
        <div class="summary-card">
            <div class="summary-number">
                {relationship_count}
            </div>
            <div class="summary-label">
                Event-product records
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STEP 1: SELECT EVENT
# =========================================================

st.markdown(
    '<div class="section-label">Step one</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Choose the tasting, if remembered"
)

event_options = events[
    "EventLabel"
].tolist()

selected_event_label = st.selectbox(
    "Tasting date and theme",
    [UNKNOWN] + event_options
)

selected_event_id = None

if selected_event_label != UNKNOWN:

    selected_event_row = events[
        events["EventLabel"]
        == selected_event_label
    ].iloc[0]

    selected_event_id = selected_event_row[
        "EventID"
    ]

    event_products = products_for_event(
        wine_data,
        selected_event_id
    )

    st.success(
        f"{len(event_products)} wines are connected "
        f"to event {selected_event_id}."
    )

    with st.expander(
        "View wines connected to this tasting",
        expanded=True
    ):

        event_candidates = dataframe_to_candidates(
            event_products
        )

        for wine in event_candidates:

            show_wine(
                wine
            )

else:

    st.info(
        "If the tasting is unknown, the application searches "
        "across all wine-event records and uses the other clues "
        "to narrow the candidates."
    )


# =========================================================
# STEP 2: ADD DETAILS
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

    available_types = sorted(
        value
        for value in wine_data[
            "WineType"
        ].unique().tolist()
        if str(value).strip()
    )

    selected_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + available_types
    )

    available_countries = sorted(
        value
        for value in wine_data[
            "CountryOrOrigin"
        ].unique().tolist()
        if str(value).strip()
    )

    selected_country = st.selectbox(
        "Country or origin",
        [UNKNOWN] + available_countries
    )

with right_column:

    description = st.text_area(
        "Describe the wine in your own words",
        placeholder=(
            "For example: it was a light red, smooth rather than "
            "heavy, and possibly from Italy. I remember red fruit "
            "and maybe something earthy."
        ),
        height=175
    )

    st.caption(
        "Useful clues include colour, sweetness, body, fruit, "
        "bubbles, origin, food pairing or approximate date."
    )


# =========================================================
# STEP 3: RUN AI MATCHING
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">Step three</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Ask AI to compare the eligible records"
)

if st.button(
    "Find likely matches",
    type="primary",
    use_container_width=True
):

    supplied_details = sum(
        [
            selected_event_id is not None,
            selected_type != UNKNOWN,
            selected_country != UNKNOWN,
            bool(description.strip())
        ]
    )

    if supplied_details == 0:

        st.warning(
            "Please provide at least one detail before searching."
        )

    else:

        filtered_data = filter_candidate_data(
            wine_data,
            selected_event_id,
            selected_type,
            selected_country
        )

        if filtered_data.empty:

            st.warning(
                "No records match every selected filter. "
                "Change one answer to 'I don't remember' and try again."
            )

        elif not description.strip():

            st.warning(
                "The filters found possible wines, but the AI needs "
                "at least one taste, texture or other descriptive clue "
                "to rank them."
            )

            st.write(
                f"**Remaining eligible wines:** "
                f"{len(filtered_data)}"
            )

        else:

            candidates = dataframe_to_candidates(
                filtered_data
            )

            st.write(
                f"AI is comparing the description with "
                f"**{len(candidates)} eligible event-product records**."
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
                        "There is not enough information "
                        "for a responsible match."
                    )

                    clarifying_question = str(
                        ai_result.get(
                            "clarifying_question",
                            ""
                        )
                    ).strip()

                    if clarifying_question:

                        st.write(
                            "**One useful question:** "
                            + clarifying_question
                        )

                else:

                    matches = validate_matches(
                        ai_result,
                        candidates
                    )

                    if not matches:

                        st.warning(
                            "The AI did not return a valid match "
                            "from the eligible database records. "
                            "Try adding one more detail."
                        )

                    else:

                        st.markdown(
                            "## Likely matches"
                        )

                        st.write(
                            "Every result below comes from an exact "
                            "EventID and ProductID relationship in "
                            "winehouse_data.csv."
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

                        clarification = str(
                            ai_result.get(
                                "clarifying_question",
                                ""
                            )
                        ).strip()

                        if clarification:

                            st.info(
                                "A detail that could improve the result: "
                                + clarification
                            )

                        st.markdown(
                            """
                            <div class="notice">
                                These are possible matches, not guaranteed
                                identifications. Verify the event record and
                                current availability separately before relying
                                on a result.
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
