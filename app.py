import json
import pandas as pd
import streamlit as st
from google import genai


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="WineHouse Wine Finder",
    layout="wide",
    initial_sidebar_state="collapsed"
)

UNKNOWN = "I don't remember"
MODEL_NAME = "gemini-4-hydrogen"


# =========================================================
# MODERN WINEHOUSE DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --wine: #641d32;
        --wine-dark: #40101f;
        --wine-light: #8d3850;
        --cream: #f7f1e8;
        --paper: #fffdf9;
        --gold: #b59454;
        --gold-light: #d8c599;
        --ink: #251b1d;
        --muted: #766c6e;
        --line: #e5dace;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(181,148,84,0.12), transparent 28rem),
            linear-gradient(180deg, #fffdf9 0%, #f7f1e8 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2.4rem;
        padding-bottom: 5rem;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--wine-dark);
        letter-spacing: -0.02em;
    }

    p, label, div, button, input, textarea {
        font-family: 'DM Sans', Arial, sans-serif;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 48px 52px;
        border-radius: 24px;
        background:
            linear-gradient(115deg, rgba(53,10,25,0.98), rgba(111,29,54,0.92)),
            #641d32;
        color: white;
        box-shadow: 0 24px 60px rgba(64,16,31,0.20);
        margin-bottom: 32px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -70px;
        top: -110px;
        border: 1px solid rgba(216,197,153,0.35);
        border-radius: 50%;
        box-shadow:
            0 0 0 35px rgba(216,197,153,0.06),
            0 0 0 70px rgba(216,197,153,0.04);
    }

    .hero-kicker {
        color: var(--gold-light);
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(2.4rem, 6vw, 4.2rem);
        line-height: 1.02;
        margin: 0 0 16px 0;
        max-width: 710px;
    }

    .hero p {
        color: rgba(255,255,255,0.82);
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 690px;
        margin: 0;
    }

    .section-card {
        background: rgba(255,253,249,0.94);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 26px 28px;
        margin: 18px 0;
        box-shadow: 0 12px 35px rgba(64,16,31,0.06);
    }

    .section-number {
        color: var(--gold);
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .wine-card {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 9px 24px rgba(64,16,31,0.05);
    }

    .wine-visual {
        height: 176px;
        border-radius: 14px;
        background:
            radial-gradient(circle at 50% 28%, rgba(216,197,153,0.35), transparent 30%),
            linear-gradient(145deg, #efe3d4, #fbf7f0);
        border: 1px solid #e1d4c3;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: var(--wine);
        text-align: center;
        padding: 18px;
    }

    .wine-visual-mark {
        width: 46px;
        height: 70px;
        border-radius: 7px 7px 14px 14px;
        background: linear-gradient(180deg, #7c2943, #40101f);
        margin-bottom: 12px;
        position: relative;
        box-shadow: 0 12px 20px rgba(64,16,31,0.20);
    }

    .wine-visual-mark::before {
        content: "";
        position: absolute;
        width: 15px;
        height: 25px;
        left: 15px;
        top: -22px;
        border-radius: 4px 4px 0 0;
        background: #40101f;
    }

    .wine-visual-name {
        font-size: 0.78rem;
        font-weight: 600;
        line-height: 1.35;
    }

    .tag {
        display: inline-block;
        padding: 5px 10px;
        margin: 3px 5px 3px 0;
        border-radius: 999px;
        background: #f1e6df;
        color: var(--wine);
        font-size: 0.78rem;
        font-weight: 600;
    }

    .status-note {
        padding: 15px 17px;
        border-radius: 12px;
        background: #f7f0df;
        border-left: 4px solid var(--gold);
        color: #5f5135;
        line-height: 1.55;
        font-size: 0.9rem;
    }

    .age-card {
        max-width: 680px;
        margin: 70px auto 20px auto;
        padding: 50px;
        border-radius: 26px;
        background:
            linear-gradient(145deg, rgba(54,11,27,0.98), rgba(105,29,52,0.96));
        color: white;
        text-align: center;
        box-shadow: 0 30px 80px rgba(64,16,31,0.28);
    }

    .age-card h1 {
        color: white;
        font-size: 3rem;
        margin: 10px 0 15px 0;
    }

    .age-card p {
        color: rgba(255,255,255,0.80);
        line-height: 1.7;
    }

    .age-label {
        color: var(--gold-light);
        font-size: 0.78rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 600;
    }

    div.stButton > button {
        min-height: 50px;
        border-radius: 10px;
        border: 1px solid var(--wine);
        background: var(--wine);
        color: white;
        font-weight: 600;
        transition: all 0.18s ease;
    }

    div.stButton > button:hover {
        background: var(--wine-dark);
        border-color: var(--wine-dark);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 9px 22px rgba(64,16,31,0.17);
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stTextArea"] > div {
        border-radius: 12px;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    hr {
        border-color: var(--line);
    }

    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.7;
        margin-top: 45px;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 34px 27px;
        }

        .age-card {
            padding: 36px 25px;
            margin-top: 30px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
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
                Please confirm that you meet the legal drinking age requirement
                before continuing.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    yes_column, no_column = st.columns(2)

    with yes_column:
        if st.button(
            "Yes, I am 18 or older",
            use_container_width=True,
            type="primary"
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
            "You must be 18 or older to use the WineHouse Wine Finder."
        )

    st.caption(
        "This confirmation is a prototype age gate and does not independently "
        "verify age or identity."
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
# LOAD REAL CSV DATA
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
        "CalendarStatus",
        "ProductID",
        "ProductName",
        "BeverageType",
        "CountryOrOrigin",
        "Style",
        "ProductStatus",
        "SequenceNo",
        "SelectionStatus",
        "Notes"
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

    # The application is a wine finder, so spirit-only events
    # are excluded from the searchable wine pool.
    dataframe = dataframe[
        dataframe["BeverageType"].str.lower() == "wine"
    ].copy()

    dataframe["WineType"] = (
        dataframe["Style"]
        .str.split(",")
        .str[0]
        .str.strip()
    )

    return dataframe.sort_values(
        ["EventDate", "SequenceNo"]
    )


try:
    wine_data = load_wine_data()

except Exception as error:
    st.error(
        "The WineHouse data file could not be loaded. "
        "Make sure winehouse_data.csv is in the GitHub repository. "
        f"Technical detail: {error}"
    )
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def normalise(value):
    return str(value).strip().lower()


def dataframe_to_candidates(dataframe):

    candidate_records = []

    for _, row in dataframe.iterrows():

        candidate_records.append(
            {
                "record_id": (
                    str(row["EventID"])
                    + "|"
                    + str(row["ProductID"])
                ),
                "event_id": row["EventID"],
                "event": row["EventLabel"],
                "date": row["FormattedDate"],
                "theme": row["Theme"],
                "event_status": row["CalendarStatus"],
                "product_id": row["ProductID"],
                "name": row["ProductName"],
                "type": row["WineType"],
                "country": row["CountryOrOrigin"],
                "style": row["Style"],
                "product_status": row["ProductStatus"],
                "sequence": row["SequenceNo"],
                "selection_status": row["SelectionStatus"],
                "notes": row["Notes"]
            }
        )

    return candidate_records


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
            filtered["WineType"].str.lower()
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

    if first_brace != -1 and last_brace != -1:
        cleaned = cleaned[
            first_brace:last_brace + 1
        ]

    return cleaned


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

A user is trying to identify a wine using an imperfect memory.
Compare the user's description with ONLY the supplied WineHouse records.

USER DESCRIPTION:
{description}

ELIGIBLE WINEHOUSE RECORDS:
{candidate_json}

Return ONLY valid JSON with this exact structure:

{{
  "enough_information": true,
  "clarifying_question": "",
  "matches": [
    {{
      "record_id": "exact supplied record_id",
      "confidence": "Strong possible match",
      "reason": "Short explanation based only on the supplied record"
    }}
  ]
}}

RULES:
1. Return no more than three matches.
2. Use only exact record_id values from the supplied records.
3. Never invent a wine, event, country, style, flavour, or stock claim.
4. Rank by semantic similarity, not only exact word overlap.
5. Valid confidence values:
   - Strong possible match
   - Possible match
   - Weak possible match
6. Explain both supporting evidence and any important mismatch.
7. If the description is too vague, set enough_information to false,
   return an empty matches list, and ask one short clarifying question.
8. Product catalogue presence does not prove current stock.
9. A proposed pairing does not prove that a wine was historically served.
10. Return JSON only.
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

        return json.loads(
            clean_json_response(
                response.text
            )
        )

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

    valid_confidence = [
        "Strong possible match",
        "Possible match",
        "Weak possible match"
    ]

    validated = []
    used_records = set()

    for result in ai_result.get(
        "matches",
        []
    ):

        record_id = str(
            result.get(
                "record_id",
                ""
            )
        ).strip()

        if record_id not in allowed_records:
            continue

        if record_id in used_records:
            continue

        confidence = result.get(
            "confidence",
            "Possible match"
        )

        if confidence not in valid_confidence:
            confidence = "Possible match"

        reason = str(
            result.get(
                "reason",
                "This record matches some of the supplied details."
            )
        ).strip()

        validated.append(
            {
                "wine": allowed_records[record_id],
                "confidence": confidence,
                "reason": reason
            }
        )

        used_records.add(record_id)

        if len(validated) == 3:
            break

    return validated


def wine_visual(name):

    safe_name = (
        str(name)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    st.markdown(
        f"""
        <div class="wine-visual">
            <div class="wine-visual-mark"></div>
            <div class="wine-visual-name">
                {safe_name}
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

    visual_column, detail_column = st.columns(
        [1, 3]
    )

    with visual_column:
        wine_visual(
            wine["name"]
        )

    with detail_column:

        if match_number is not None:
            st.caption(
                f"MATCH {match_number}"
            )

        st.markdown(
            f"### {wine['name']}"
        )

        st.markdown(
            f"""
            <span class="tag">{wine['type']}</span>
            <span class="tag">{wine['country']}</span>
            <span class="tag">{wine['style']}</span>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"**Tasting:** {wine['event']}"
        )

        if reason:
            st.write(
                f"**Why this may match:** {reason}"
            )

        if confidence:
            st.write(
                f"**Confidence:** {confidence}"
            )

        st.caption(
            f"Product status: {wine['product_status']}"
        )

        st.caption(
            f"Event-wine status: {wine['selection_status']}"
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
        <div class="hero-kicker">
            WineHouse discovery
        </div>
        <h1>Find the wine you remember.</h1>
        <p>
            Select the details you know, describe the taste in your own
            words, and let AI compare your memory with the available
            WineHouse tasting records.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="status-note">
        This prototype uses synthetic and proposed project records.
        Results are possible matches, not guaranteed identifications.
        Current stock availability must be checked separately.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STEP 1: EVENT
# =========================================================

st.markdown(
    """
    <div class="section-number">Step one</div>
    """,
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

    selected_event_data = wine_data[
        wine_data["EventLabel"]
        == selected_event
    ]

    st.success(
        f"{len(selected_event_data)} wines are linked "
        "to this tasting record."
    )

    with st.expander(
        "View the wines linked to this tasting"
    ):

        event_candidates = dataframe_to_candidates(
            selected_event_data
        )

        for candidate in event_candidates:
            show_wine(candidate)

else:

    st.info(
        "The tasting is not required. If it is unknown, "
        "the finder can search across all available WineHouse "
        "wine-event records."
    )


# =========================================================
# STEP 2: DETAILS
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-number">Step two</div>
    """,
    unsafe_allow_html=True
)

st.subheader(
    "Add the details you remember"
)

left_column, right_column = st.columns(2)

with left_column:

    wine_types = sorted(
        value
        for value in wine_data[
            "WineType"
        ].unique().tolist()
        if value
    )

    selected_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + wine_types
    )

    countries = sorted(
        value
        for value in wine_data[
            "CountryOrOrigin"
        ].unique().tolist()
        if value
    )

    selected_country = st.selectbox(
        "Country or origin",
        [UNKNOWN] + countries
    )

with right_column:

    description = st.text_area(
        "Describe the wine in your own words",
        placeholder=(
            "For example: it was a light red, smooth rather than heavy, "
            "with cherries and something earthy. I may have tasted it "
            "at an Italian wine evening."
        ),
        height=170
    )

    st.caption(
        "Useful clues include colour, sweetness, body, fruit, spices, "
        "flowers, minerals, bubbles, food pairing or approximate date."
    )


# =========================================================
# STEP 3: MATCHING
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-number">Step three</div>
    """,
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

    supplied_details = sum(
        [
            selected_event != UNKNOWN,
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
            selected_event,
            selected_type,
            selected_country
        )

        if filtered_data.empty:

            st.warning(
                "No WineHouse records match all selected filters. "
                "Change one answer to 'I don't remember' and try again."
            )

        elif not description.strip():

            st.warning(
                "The filters found possible records, but the AI needs "
                "at least one taste, smell, texture or other clue to rank them."
            )

            st.write(
                f"**Remaining records:** {len(filtered_data)}"
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
                "Comparing your description with the WineHouse records..."
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
                        "There is not enough information for "
                        "a responsible match."
                    )

                    question = ai_result.get(
                        "clarifying_question",
                        ""
                    )

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
                            "from the eligible WineHouse records. "
                            "Try adding another detail."
                        )

                    else:

                        st.markdown(
                            "## Your likely matches"
                        )

                        st.write(
                            "Every result below is an actual record "
                            "from the uploaded WineHouse project dataset."
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

                        question = ai_result.get(
                            "clarifying_question",
                            ""
                        )

                        if question:
                            st.info(
                                f"A detail that could improve the result: "
                                f"{question}"
                            )

                        st.markdown(
                            """
                            <div class="status-note">
                                Please verify the tasting record before relying
                                on a match. These project records may contain
                                proposed wine selections, and catalogue presence
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
