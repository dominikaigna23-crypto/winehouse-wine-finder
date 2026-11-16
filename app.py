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
        --wine-dark: #38101e;
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
        max-width: 1050px;
        padding-top: 2.4rem;
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
        font-size: clamp(2.5rem, 6vw, 4.2rem);
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
        margin-top: 28px;
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
        background: rgba(255, 253, 249, 0.97);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 23px 25px;
        margin: 13px 0;
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

    div.stButton > button {
        min-height: 51px;
        border-radius: 11px;
        border: 1px solid var(--wine);
        background: var(--wine);
        color: white;
        font-weight: 700;
    }

    div.stButton > button:hover {
        background: var(--wine-dark);
        border-color: var(--wine-dark);
        color: white;
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
# LOAD COMPLETE DATABASE EXPORT
# =========================================================

@st.cache_data
def load_database():

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

    # Event names are created only from actual event fields.
    dataframe["EventLabel"] = (
        dataframe["FormattedDate"]
        + " | "
        + dataframe["Theme"]
    )

    # This is a wine finder, so remove only actual spirit products.
    # This does not reduce wine events to four.
    dataframe = dataframe[
        ~dataframe["BeverageType"]
        .str.lower()
        .str.contains("spirit", na=False)
    ].copy()

    # Remove exact duplicate event-product relationships.
    dataframe = dataframe.drop_duplicates(
        subset=[
            "EventID",
            "ProductID"
        ]
    )

    dataframe["WineType"] = dataframe.apply(
        determine_wine_type,
        axis=1
    )

    return dataframe.sort_values(
        [
            "EventDate",
            "EventID",
            "ProductName"
        ]
    ).reset_index(drop=True)


def determine_wine_type(row):

    combined_text = (
        str(row["Style"])
        + " "
        + str(row["ProductName"])
        + " "
        + str(row["BeverageType"])
    ).lower()

    if "sparkling" in combined_text:
        return "Sparkling"

    if "champagne" in combined_text:
        return "Sparkling"

    if "prosecco" in combined_text:
        return "Sparkling"

    if "crémant" in combined_text or "cremant" in combined_text:
        return "Sparkling"

    if "rosé" in combined_text or "rose" in combined_text:
        return "Rosé"

    if "orange" in combined_text:
        return "Orange"

    if "dessert" in combined_text:
        return "Dessert"

    if "sweet" in combined_text:
        return "Sweet"

    if "fortified" in combined_text:
        return "Fortified"

    if "red" in combined_text:
        return "Red"

    if "white" in combined_text:
        return "White"

    return "Other wine"


try:
    database = load_database()
except Exception as error:
    st.error(
        "The WineHouse database export could not be loaded. "
        "Make sure the clean file is named winehouse_data.csv. "
        f"Technical detail: {error}"
    )
    st.stop()


# =========================================================
# CREATE EVENTS TABLE
# =========================================================

def create_events_table(dataframe):

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


events = create_events_table(
    database
)


# =========================================================
# EVENT AND PRODUCT RELATIONSHIP
# =========================================================

def products_for_event(
    dataframe,
    event_id
):

    # This is the relationship your friend described:
    # get EventID from Events, then find all products
    # connected to that same EventID.
    return dataframe[
        dataframe["EventID"] == event_id
    ].copy()


def make_candidate_records(
    dataframe
):

    candidates = []

    for _, row in dataframe.iterrows():

        # IDs are used only internally.
        # They are never displayed to the user.
        internal_record_id = (
            str(row["EventID"])
            + "|"
            + str(row["ProductID"])
        )

        candidates.append(
            {
                "record_id": internal_record_id,
                "event_id": row["EventID"],
                "product_id": row["ProductID"],
                "event_label": row["EventLabel"],
                "event_date": row["FormattedDate"],
                "event_theme": row["Theme"],
                "name": row["ProductName"],
                "country": row["CountryOrOrigin"],
                "style": row["Style"],
                "wine_type": row["WineType"]
            }
        )

    return candidates


def filter_database(
    dataframe,
    selected_event_id,
    selected_wine_type,
    selected_country
):

    filtered = dataframe.copy()

    if selected_event_id is not None:
        filtered = filtered[
            filtered["EventID"] == selected_event_id
        ]

    if selected_wine_type != UNKNOWN:
        filtered = filtered[
            filtered["WineType"] == selected_wine_type
        ]

    if selected_country != UNKNOWN:
        filtered = filtered[
            filtered["CountryOrOrigin"].str.lower()
            == selected_country.lower()
        ]

    return filtered


# =========================================================
# JSON RESPONSE CLEANING
# =========================================================

def clean_json_response(response_text):

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
# AI RANKING
# =========================================================

def rank_candidates_with_ai(
    description,
    candidates
):

    records_for_ai = []

    for candidate in candidates:
        records_for_ai.append(
            {
                "record_id": candidate["record_id"],
                "event_date": candidate["event_date"],
                "event_theme": candidate["event_theme"],
                "product_name": candidate["name"],
                "wine_type": candidate["wine_type"],
                "country_or_origin": candidate["country"],
                "style": candidate["style"]
            }
        )

    records_json = json.dumps(
        records_for_ai,
        ensure_ascii=False
    )

    prompt = f"""
You are the matching engine for the WineHouse Wine Finder.

A person is trying to identify a wine from an imperfect description.

The application has already loaded eligible wine records from the
WineHouse event and product database.

Compare the person's description only with those supplied records.

PERSON'S DESCRIPTION:
{description}

ELIGIBLE DATABASE RECORDS:
{records_json}

Return only valid JSON in this structure:

{{
  "enough_information": true,
  "clarifying_question": "",
  "matches": [
    {{
      "record_id": "exact supplied record_id",
      "confidence": "Strong possible match",
      "reason": "Short explanation using supplied database fields"
    }}
  ]
}}

Rules:

1. Return no more than three matches.
2. Use only exact record_id values supplied above.
3. Never invent a wine, event, origin or style.
4. Never add a wine outside the eligible records.
5. Rank semantically, not only by exact word matching.
6. Consider reasonable similarities:
   not heavy may mean light;
   powerful may mean rich or full-bodied;
   bubbles may mean sparkling;
   fruity may relate to fruit descriptions in style or name.
7. Confidence must be one of:
   Strong possible match
   Possible match
   Weak possible match
8. Explain which supplied fields support the match.
9. Mention a meaningful mismatch when relevant.
10. If the description is too vague:
    set enough_information to false,
    return no matches,
    and ask one short clarifying question.
11. Never claim current stock availability.
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


def validate_ai_matches(
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

        if confidence not in valid_confidences:
            confidence = "Possible match"

        reason = str(
            item.get(
                "reason",
                "This wine matches some of the remembered details."
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
# RESULT DISPLAY
# =========================================================

def safe_text(value):

    return html.escape(
        str(value)
    )


def confidence_class(confidence):

    if confidence == "Strong possible match":
        return "confidence-strong"

    if confidence == "Weak possible match":
        return "confidence-weak"

    return "confidence-possible"


def display_wine(
    wine,
    match_number=None,
    confidence=None,
    reason=None
):

    number_html = ""

    if match_number is not None:
        number_html = (
            '<div class="wine-number">'
            + "Match "
            + safe_text(match_number)
            + "</div>"
        )

    tags = [
        wine["wine_type"],
        wine["country"],
        wine["style"]
    ]

    tags_html = ""

    for tag in tags:
        if str(tag).strip():
            tags_html += (
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
            + confidence_class(confidence)
            + '">'
            + safe_text(confidence)
            + "</span>"
            + "</div>"
        )

    # No EventID or ProductID is shown here.
    st.markdown(
        f"""
        <div class="wine-card">
            {number_html}
            <div class="wine-name">
                {safe_text(wine["name"])}
            </div>
            <div>
                {tags_html}
            </div>
            <div class="wine-detail">
                <strong>Tasting:</strong>
                {safe_text(wine["event_label"])}
            </div>
            {reason_html}
            {confidence_html}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    """
    <section class="hero">
        <div class="hero-label">
            WineHouse discovery
        </div>
        <h1>Find the wine you remember.</h1>
        <p>
            Choose a tasting if known, add any details you remember,
            and let AI compare your description with the wines linked
            to the WineHouse event and product database.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="notice">
        This prototype uses synthetic project data.
        Results are possible matches, not guaranteed identifications.
        Event-product records do not prove historical service or
        current stock availability.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STEP 1: TASTING
# =========================================================

st.markdown(
    '<div class="section-label">Step one</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Choose the tasting, if remembered"
)

event_ids = events[
    "EventID"
].tolist()

# EventID is the real value.
# format_func controls what users see, so no code is displayed.
event_labels = {
    row["EventID"]: row["EventLabel"]
    for _, row in events.iterrows()
}

selected_event_id = st.selectbox(
    "Tasting date and theme",
    options=[None] + event_ids,
    format_func=lambda event_id: (
        UNKNOWN
        if event_id is None
        else event_labels[event_id]
    )
)

if selected_event_id is not None:

    connected_products = products_for_event(
        database,
        selected_event_id
    )

    st.success(
        f"{len(connected_products)} wines are connected "
        "to this tasting."
    )

    with st.expander(
        "View wines from this tasting",
        expanded=True
    ):

        connected_candidates = make_candidate_records(
            connected_products
        )

        for wine in connected_candidates:
            display_wine(wine)

else:

    st.info(
        "If the tasting is unknown, the website searches "
        "across the full wine-event database."
    )


# =========================================================
# STEP 2: REMEMBERED WINE DETAILS
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

    wine_types = sorted(
        value
        for value in database[
            "WineType"
        ].unique().tolist()
        if str(value).strip()
    )

    selected_wine_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + wine_types
    )

    countries = sorted(
        value
        for value in database[
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
            "For example: it was a light red, not very heavy, "
            "possibly Italian, and I remember red fruit and "
            "something earthy."
        ),
        height=175
    )

    st.caption(
        "Useful clues include colour, sweetness, body, bubbles, "
        "fruit, country, food pairing or approximate date."
    )


# =========================================================
# STEP 3: AI SEARCH
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">Step three</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Find likely matches"
)

if st.button(
    "Search the WineHouse database",
    type="primary",
    use_container_width=True
):

    supplied_details = sum(
        [
            selected_event_id is not None,
            selected_wine_type != UNKNOWN,
            selected_country != UNKNOWN,
            bool(description.strip())
        ]
    )

    if supplied_details == 0:

        st.warning(
            "Please provide at least one detail before searching."
        )

    else:

        filtered_database = filter_database(
            database,
            selected_event_id,
            selected_wine_type,
            selected_country
        )

        if filtered_database.empty:

            st.warning(
                "No wines match every selected filter. "
                "Change one answer to 'I don't remember' and try again."
            )

        elif not description.strip():

            candidates_without_ai = make_candidate_records(
                filtered_database
            )

            st.markdown(
                "## Matching database records"
            )

            st.write(
                "The filters found these wines. Add a description "
                "if you want AI to rank them."
            )

            for wine in candidates_without_ai[:20]:
                display_wine(wine)

        else:

            candidates = make_candidate_records(
                filtered_database
            )

            st.write(
                f"AI is comparing the description with "
                f"**{len(candidates)} eligible wines**."
            )

            with st.spinner(
                "Comparing your description with the database..."
            ):

                ai_result = rank_candidates_with_ai(
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
                            "**One useful question:** "
                            + question
                        )

                else:

                    matches = validate_ai_matches(
                        ai_result,
                        candidates
                    )

                    if not matches:

                        st.warning(
                            "The AI did not return a valid wine "
                            "from the eligible database records. "
                            "Try adding another detail."
                        )

                    else:

                        st.markdown(
                            "## Likely matches"
                        )

                        st.write(
                            "Each result below is an actual wine "
                            "connected to an eligible tasting in "
                            "the uploaded database."
                        )

                        for position, match in enumerate(
                            matches,
                            start=1
                        ):

                            display_wine(
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
                            <div class="notice">
                                These are possible matches, not guaranteed
                                identifications. Verify the event record and
                                current availability separately.
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
