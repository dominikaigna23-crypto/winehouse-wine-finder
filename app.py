import html
import json

import pandas as pd
import streamlit as st
from google import genai
from google.genai import types


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
    --wine-dark: #3b101f;
    --cream: #f7f1e8;
    --paper: #fffdf9;
    --gold: #b79555;
    --gold-light: #ddcba1;
    --text: #2b2123;
    --muted: #776d6f;
    --border: #e5d9cd;
}

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(183,149,85,0.12),
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
    padding-top: 2.5rem;
    padding-bottom: 5rem;
}

h1, h2, h3 {
    font-family: Georgia, "Times New Roman", serif;
    color: var(--wine-dark);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 52px 55px;
    border-radius: 26px;
    background: linear-gradient(
        115deg,
        rgba(53,9,25,0.99),
        rgba(113,30,57,0.94)
    );
    color: white;
    box-shadow: 0 24px 65px rgba(64,16,31,0.22);
    margin-bottom: 34px;
}

.hero-label {
    color: var(--gold-light);
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 13px;
}

.hero-title {
    color: white;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(2.5rem, 6vw, 4.2rem);
    font-weight: 700;
    line-height: 1.03;
    margin-bottom: 17px;
}

.hero-text {
    color: rgba(255,255,255,0.82);
    font-size: 1.06rem;
    line-height: 1.72;
    max-width: 700px;
}

.age-card {
    max-width: 700px;
    margin: 70px auto 24px auto;
    padding: 55px 48px;
    border-radius: 27px;
    background: linear-gradient(
        145deg,
        rgba(53,9,25,0.99),
        rgba(110,29,55,0.97)
    );
    color: white;
    text-align: center;
    box-shadow: 0 30px 85px rgba(64,16,31,0.30);
}

.age-title {
    color: white;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 3.1rem;
    font-weight: 700;
    margin: 12px 0 18px;
}

.age-text {
    color: rgba(255,255,255,0.82);
    line-height: 1.72;
}

.age-label,
.section-label {
    color: var(--gold);
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}

.age-label {
    color: var(--gold-light);
}

.section-label {
    margin-top: 28px;
    margin-bottom: 3px;
}

.wine-card {
    background: rgba(255,253,249,0.97);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px 24px;
    margin: 13px 0;
    box-shadow: 0 10px 27px rgba(64,16,31,0.06);
}

.wine-rank {
    color: var(--gold);
    font-size: 0.73rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.wine-name {
    font-family: Georgia, "Times New Roman", serif;
    color: var(--wine-dark);
    font-size: 1.5rem;
    font-weight: 700;
    margin: 7px 0 9px;
}

.wine-detail {
    line-height: 1.62;
    margin-top: 7px;
}

.tag {
    display: inline-block;
    padding: 6px 11px;
    margin: 3px 5px 9px 0;
    border-radius: 999px;
    background: #f1e5df;
    color: var(--wine);
    font-size: 0.77rem;
    font-weight: 700;
}

.verification {
    padding: 16px 18px;
    border-radius: 13px;
    background: #f7f0df;
    border-left: 4px solid var(--gold);
    color: #5c4d31;
    margin: 20px 0;
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
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 50px;
}
</style>
    """,
    unsafe_allow_html=True
)


def safe(value):
    return html.escape(str(value))


# =========================================================
# AGE GATE
# =========================================================

if "age_confirmed" not in st.session_state:
    st.session_state.age_confirmed = False

if "age_declined" not in st.session_state:
    st.session_state.age_declined = False


if not st.session_state.age_confirmed:

    st.markdown(
        '<div class="age-card">'
        '<div class="age-label">WineHouse</div>'
        '<div class="age-title">Are you 18 or older?</div>'
        '<div class="age-text">'
        'This website contains information about alcoholic beverages. '
        'Please confirm that you are at least 18 years old before entering.'
        '</div>'
        '</div>',
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
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(
            timeout=20000
        )
    )

except Exception as error:

    st.error(
        f"AI connection error: {error}"
    )

    st.stop()


# =========================================================
# WINE TYPE
# =========================================================

def determine_wine_type(row):

    text = (
        str(row["Style"])
        + " "
        + str(row["ProductName"])
    ).lower()

    if any(
        word in text
        for word in [
            "sparkling",
            "champagne",
            "prosecco",
            "crémant",
            "cremant",
            "cava"
        ]
    ):
        return "Sparkling"

    if "rosé" in text or "rose" in text:
        return "Rosé"

    if "orange" in text:
        return "Orange"

    if "fortified" in text:
        return "Fortified"

    if "dessert" in text:
        return "Dessert"

    if "red" in text:
        return "Red"

    if "white" in text:
        return "White"

    return "Other"


# =========================================================
# LOAD EVENTS
# =========================================================

@st.cache_data
def load_events():

    dataframe = pd.read_csv(
        "events.csv"
    )

    required = [
        "EventID",
        "EventDateKey",
        "Theme"
    ]

    missing = [
        column
        for column in required
        if column not in dataframe.columns
    ]

    if missing:

        raise ValueError(
            "events.csv is missing: "
            + ", ".join(missing)
        )

    for column in required:

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

    dataframe["DateLabel"] = (
        dataframe["EventDate"]
        .dt.strftime("%d %B %Y")
        .fillna(dataframe["EventDateKey"])
    )

    dataframe["DisplayName"] = (
        dataframe["DateLabel"]
        + " | "
        + dataframe["Theme"]
    )

    return (
        dataframe
        .drop_duplicates(
            subset=["EventID"]
        )
        .sort_values(
            ["EventDate", "EventID"]
        )
        .reset_index(drop=True)
    )


# =========================================================
# LOAD EVENT WINES
# =========================================================

@st.cache_data
def load_event_wines():

    dataframe = pd.read_csv(
        "event_wines.csv"
    )

    required = [
        "EventID",
        "ProductID",
        "ProductName",
        "BeverageType",
        "CountryOrOrigin",
        "Style"
    ]

    missing = [
        column
        for column in required
        if column not in dataframe.columns
    ]

    if missing:

        raise ValueError(
            "event_wines.csv is missing: "
            + ", ".join(missing)
        )

    for column in required:

        dataframe[column] = (
            dataframe[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    dataframe["Style"] = (
        dataframe["Style"]
        .str.replace(
            " /",
            ",",
            regex=False
        )
        .str.replace(
            "/",
            ",",
            regex=False
        )
        .str.strip()
    )

    dataframe = dataframe[
        ~dataframe["BeverageType"]
        .str.lower()
        .str.contains(
            "spirit",
            na=False
        )
    ].copy()

    dataframe["WineType"] = dataframe.apply(
        determine_wine_type,
        axis=1
    )

    return (
        dataframe
        .drop_duplicates(
            subset=[
                "EventID",
                "ProductID"
            ]
        )
        .reset_index(drop=True)
    )


try:

    events = load_events()
    event_wines = load_event_wines()

except Exception as error:

    st.error(
        "The WineHouse data files could not be loaded. "
        f"Technical detail: {error}"
    )

    st.stop()


# =========================================================
# CONNECT EVENTS AND WINES
# =========================================================

event_name_lookup = dict(
    zip(
        events["EventID"],
        events["DisplayName"]
    )
)


def wines_for_event(event_id):

    return event_wines[
        event_wines["EventID"]
        == event_id
    ].copy()


def create_candidates(wine_rows):

    candidates = []

    for _, row in wine_rows.iterrows():

        event_id = row["EventID"]
        product_id = row["ProductID"]

        candidates.append(
            {
                "record_id": (
                    event_id
                    + "|"
                    + product_id
                ),
                "event": event_name_lookup.get(
                    event_id,
                    "Tasting"
                ),
                "name": row["ProductName"],
                "type": row["WineType"],
                "country": row["CountryOrOrigin"],
                "style": row["Style"]
            }
        )

    return candidates


def filter_wines(
    selected_event_id,
    selected_type,
    selected_country
):

    filtered = event_wines.copy()

    if selected_event_id is not None:

        filtered = filtered[
            filtered["EventID"]
            == selected_event_id
        ]

    if selected_type != UNKNOWN:

        filtered = filtered[
            filtered["WineType"]
            == selected_type
        ]

    if selected_country != UNKNOWN:

        filtered = filtered[
            filtered["CountryOrOrigin"]
            .str.lower()
            == selected_country.lower()
        ]

    return filtered


# =========================================================
# JSON RESPONSE
# =========================================================

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
# GEMINI AI RANKING
# =========================================================

def rank_with_ai(
    description,
    candidates
):

    ai_records = []

    for candidate in candidates:

        ai_records.append(
            {
                "record_id": candidate["record_id"],
                "tasting": candidate["event"],
                "wine_name": candidate["name"],
                "type": candidate["type"],
                "country_or_origin": candidate["country"],
                "style": candidate["style"]
            }
        )

    records_json = json.dumps(
        ai_records,
        ensure_ascii=False
    )

    prompt = f"""
You are the matching engine for the WineHouse Wine Finder.

Compare the user's description only with the supplied wine records.

USER DESCRIPTION:
{description}

ELIGIBLE WINE RECORDS:
{records_json}

Return only valid JSON:

{{
  "enough_information": true,
  "clarifying_question": "",
  "matches": [
    {{
      "record_id": "exact supplied record_id",
      "confidence": "Strong possible match"
    }}
  ]
}}

Rules:
1. Return at most three matches.
2. Use only exact supplied record_id values.
3. Do not invent or introduce wines.
4. Rank using semantic similarity.
5. Confidence must be Strong possible match,
   Possible match, or Weak possible match.
6. If there is no suitable match, set enough_information to false,
   return an empty matches list, and ask one short clarifying question.
7. If the information is too vague, set enough_information to false,
   return an empty matches list, and ask one short clarifying question.
8. Do not claim current stock availability.
9. Return JSON only.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
                max_output_tokens=600
            )
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

        error_text = str(error).upper()

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
            or "TIMEOUT" in error_text
            or "DEADLINE" in error_text
        ):

            st.error(
                "The AI service did not respond in time. "
                "Please click Search wines again."
            )

        else:

            st.error(
                "AI matching could not be completed. "
                f"Technical detail: {error}"
            )

        return None


# =========================================================
# VALIDATE MATCHES
# =========================================================

def validate_matches(
    ai_result,
    candidates
):

    allowed = {
        candidate["record_id"]: candidate
        for candidate in candidates
    }

    valid_confidences = [
        "Strong possible match",
        "Possible match",
        "Weak possible match"
    ]

    results = []
    used = set()

    for match in ai_result.get(
        "matches",
        []
    ):

        record_id = str(
            match.get(
                "record_id",
                ""
            )
        ).strip()

        if record_id not in allowed:
            continue

        if record_id in used:
            continue

        confidence = str(
            match.get(
                "confidence",
                "Possible match"
            )
        ).strip()

        if confidence not in valid_confidences:

            confidence = (
                "Possible match"
            )

        results.append(
            {
                "wine": allowed[record_id],
                "confidence": confidence
            }
        )

        used.add(record_id)

        if len(results) == 3:
            break

    return results


# =========================================================
# DISPLAY
# =========================================================

def display_wine(
    wine,
    position=None,
    confidence=None
):

    rank = ""

    if position is not None:

        rank = (
            '<div class="wine-rank">'
            f"Match {safe(position)}"
            "</div>"
        )

    tags = "".join(
        '<span class="tag">'
        + safe(value)
        + "</span>"
        for value in [
            wine["type"],
            wine["country"],
            wine["style"]
        ]
        if str(value).strip()
    )

    confidence_html = ""

    if confidence:

        confidence_html = (
            '<div class="wine-detail">'
            "<strong>Confidence:</strong> "
            + safe(confidence)
            + "</div>"
        )

    st.markdown(
        '<div class="wine-card">'
        + rank
        + '<div class="wine-name">'
        + safe(wine["name"])
        + "</div>"
        + tags
        + '<div class="wine-detail">'
        + "<strong>Tasting:</strong> "
        + safe(wine["event"])
        + "</div>"
        + confidence_html
        + "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# PAGE
# =========================================================

st.markdown(
    '<section class="hero">'
    '<div class="hero-label">'
    'WineHouse discovery'
    '</div>'
    '<div class="hero-title">'
    'Find the wine you remember.'
    '</div>'
    '<div class="hero-text">'
    'Choose a tasting if you remember it, add whatever details '
    'you know, and let AI compare your description with the '
    'WineHouse tasting and wine records.'
    '</div>'
    '</section>',
    unsafe_allow_html=True
)


# =========================================================
# STEP 1
# =========================================================

st.markdown(
    '<div class="section-label">'
    'Step one'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Do you remember the tasting?"
)

event_ids = events[
    "EventID"
].tolist()

selected_event_id = st.selectbox(
    "Tasting date and theme",
    options=[None] + event_ids,
    format_func=lambda event_id: (
        UNKNOWN
        if event_id is None
        else event_name_lookup.get(
            event_id,
            "Tasting"
        )
    )
)


if selected_event_id is not None:

    selected_wines = wines_for_event(
        selected_event_id
    )

    if selected_wines.empty:

        st.info(
            "No wine records are linked to this tasting."
        )

    else:

        st.success(
            f"{len(selected_wines)} wines are linked "
            "to this tasting."
        )

        with st.expander(
            "View wines from this tasting",
            expanded=True
        ):

            for wine in create_candidates(
                selected_wines
            ):

                display_wine(
                    wine
                )

else:

    st.info(
        "If you do not remember the tasting, the finder "
        "can search across all available wine records."
    )


# =========================================================
# STEP 2
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">'
    'Step two'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "What do you remember about the wine?"
)

left_column, right_column = st.columns(
    2
)


with left_column:

    wine_types = sorted(
        wine_type
        for wine_type in event_wines[
            "WineType"
        ].unique().tolist()
        if (
            wine_type
            and wine_type != "Other"
        )
    )

    selected_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + wine_types
    )

    countries = sorted(
        country
        for country in event_wines[
            "CountryOrOrigin"
        ].unique().tolist()
        if country
    )

    selected_country = st.selectbox(
        "Country or origin",
        [UNKNOWN] + countries
    )


with right_column:

    description = st.text_area(
        "Describe the wine in your own words",
        placeholder=(
            "For example: light red, smooth rather than heavy, "
            "possibly Italian, with red fruit and something earthy."
        ),
        height=170
    )

    st.caption(
        "You can mention taste, sweetness, body, fruit, bubbles, "
        "food pairing, country or anything else you remember."
    )


# =========================================================
# STEP 3
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">'
    'Step three'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Find likely matches"
)


if st.button(
    "Search wines",
    type="primary",
    use_container_width=True
):

    supplied_information = sum(
        [
            selected_event_id
            is not None,

            selected_type
            != UNKNOWN,

            selected_country
            != UNKNOWN,

            bool(
                description.strip()
            )
        ]
    )

    if supplied_information == 0:

        st.warning(
            "Add at least one detail before searching."
        )

    else:

        filtered = filter_wines(
            selected_event_id,
            selected_type,
            selected_country
        )

        if filtered.empty:

            st.warning(
                "No wines match the selected details. "
                "Try changing one answer to "
                "'I don't remember'."
            )

        elif not description.strip():

            st.markdown(
                "## Matching wines"
            )

            st.write(
                "These wines match the selected filters. "
                "Add a description if you want AI to rank them."
            )

            for wine in create_candidates(
                filtered
            ):

                display_wine(
                    wine
                )

        else:

            candidates = create_candidates(
                filtered
            )

            with st.spinner(
                "Comparing your description "
                "with the wine records..."
            ):

                ai_result = rank_with_ai(
                    description,
                    candidates
                )

            if ai_result:

                enough_information = (
                    ai_result.get(
                        "enough_information",
                        True
                    )
                )

                if not enough_information:

                    st.warning(
                        "No suitable wine could be identified "
                        "from the information provided."
                    )

                    question = str(
                        ai_result.get(
                            "clarifying_question",
                            ""
                        )
                    ).strip()

                    if question:

                        st.write(
                            f"**Try adding this detail:** "
                            f"{question}"
                        )

                else:

                    matches = validate_matches(
                        ai_result,
                        candidates
                    )

                    if not matches:

                        st.warning(
                            "No suitable wine could be matched. "
                            "Try changing a filter or adding "
                            "another detail."
                        )

                    else:

                        st.markdown(
                            "## Likely matches"
                        )

                        for index, match in enumerate(
                            matches,
                            start=1
                        ):

                            display_wine(
                                match["wine"],
                                position=index,
                                confidence=match[
                                    "confidence"
                                ]
                            )

                        st.markdown(
                            '<div class="verification">'
                            'Current bottle availability should '
                            'be checked separately before purchase.'
                            '</div>',
                            unsafe_allow_html=True
                        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'WineHouse Wine Finder'
    '</div>',
    unsafe_allow_html=True
)
