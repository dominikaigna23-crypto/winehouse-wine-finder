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
                rgba(53,9,25,0.99),
                rgba(113,30,57,0.94)
            );
        color: white;
        box-shadow: 0 24px 65px rgba(64,16,31,0.22);
        margin-bottom: 34px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        right: -75px;
        top: -120px;
        border: 1px solid rgba(221,203,161,0.35);
        border-radius: 50%;
        box-shadow:
            0 0 0 38px rgba(221,203,161,0.055),
            0 0 0 76px rgba(221,203,161,0.03);
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
        color: rgba(255,255,255,0.82);
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
                rgba(53,9,25,0.99),
                rgba(110,29,55,0.97)
            );
        color: white;
        text-align: center;
        box-shadow: 0 30px 85px rgba(64,16,31,0.30);
    }

    .age-card h1 {
        color: white;
        font-size: 3.1rem;
        margin: 12px 0 18px 0;
    }

    .age-card p {
        color: rgba(255,255,255,0.82);
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
        margin-bottom: 7px;
    }

    .wine-name {
        font-family: Georgia, "Times New Roman", serif;
        color: var(--wine-dark);
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .wine-detail {
        color: var(--text);
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
        line-height: 1.6;
        margin: 20px 0;
        font-size: 0.91rem;
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
# GEMINI
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
# LOAD EVENTS
# =========================================================

@st.cache_data
def load_events():

    df = pd.read_csv("events.csv")

    required = [
        "EventID",
        "EventDateKey",
        "Theme"
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "events.csv is missing: "
            + ", ".join(missing)
        )

    for column in required:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    df["EventDate"] = pd.to_datetime(
        df["EventDateKey"],
        format="%Y%m%d",
        errors="coerce"
    )

    df["DateLabel"] = (
        df["EventDate"]
        .dt.strftime("%d %B %Y")
        .fillna(df["EventDateKey"])
    )

    df["DisplayName"] = (
        df["DateLabel"]
        + " | "
        + df["Theme"]
    )

    return (
        df
        .drop_duplicates(subset=["EventID"])
        .sort_values(
            ["EventDate", "EventID"]
        )
        .reset_index(drop=True)
    )


# =========================================================
# LOAD EVENT-WINE RELATIONSHIPS
# =========================================================

@st.cache_data
def load_event_wines():

    df = pd.read_csv("event_wines.csv")

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
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "event_wines.csv is missing: "
            + ", ".join(missing)
        )

    for column in required:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # The site is a wine finder, so exclude only products
    # explicitly marked as spirits.
    df = df[
        ~df["BeverageType"]
        .str.lower()
        .str.contains("spirit", na=False)
    ].copy()

    # Clean style generated by the export-safe Azure query.
    df["Style"] = (
        df["Style"]
        .str.replace(" /", ",", regex=False)
        .str.replace("/", ",", regex=False)
        .str.strip()
    )

    df["WineType"] = df.apply(
        determine_wine_type,
        axis=1
    )

    return (
        df
        .drop_duplicates(
            subset=[
                "EventID",
                "ProductID"
            ]
        )
        .reset_index(drop=True)
    )


# =========================================================
# TYPE CLASSIFICATION
# =========================================================

def determine_wine_type(row):

    text = (
        str(row["Style"])
        + " "
        + str(row["ProductName"])
    ).lower()

    if "sparkling" in text:
        return "Sparkling"

    if "champagne" in text:
        return "Sparkling"

    if "prosecco" in text:
        return "Sparkling"

    if "crémant" in text or "cremant" in text:
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
# LOAD BOTH FILES
# =========================================================

try:
    events = load_events()
    event_wines = load_event_wines()

except Exception as error:
    st.error(
        "The WineHouse data files could not be loaded. "
        "Make sure events.csv and event_wines.csv are in GitHub "
        f"next to app.py. Technical detail: {error}"
    )
    st.stop()


# =========================================================
# CONNECT EVENTS TO PRODUCTS
# =========================================================

def wines_for_event(event_id):

    return event_wines[
        event_wines["EventID"] == event_id
    ].copy()


def create_candidates(
    wine_rows,
    event_name_lookup
):

    candidates = []

    for _, row in wine_rows.iterrows():

        event_id = row["EventID"]
        product_id = row["ProductID"]

        candidates.append(
            {
                # Internal only. Never displayed on site.
                "record_id": event_id + "|" + product_id,
                "event_id": event_id,
                "product_id": product_id,

                # Visitor-facing values.
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


event_name_lookup = dict(
    zip(
        events["EventID"],
        events["DisplayName"]
    )
)


# =========================================================
# FILTERING
# =========================================================

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
# JSON HELPER
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

    first = cleaned.find("{")
    last = cleaned.rfind("}")

    if first != -1 and last > first:
        cleaned = cleaned[first:last + 1]

    return cleaned


# =========================================================
# AI MATCHING
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

The user is trying to identify a wine from an imperfect memory.

Only wines from the supplied database records are valid answers.

USER DESCRIPTION:
{description}

ELIGIBLE WINE RECORDS:
{records_json}

Return ONLY valid JSON:

{{
    "enough_information": true,
    "clarifying_question": "",
    "matches": [
        {{
            "record_id": "exact supplied record_id",
            "confidence": "Strong possible match",
            "reason": "Short explanation based on supplied record fields"
        }}
    ]
}}

Rules:

1. Return at most three matches.
2. Use only exact record_id values supplied above.
3. Do not invent wines.
4. Do not introduce outside wines.
5. Use semantic reasoning, not only exact word matching.
6. Consider reasonable equivalents:
   not heavy = light;
   powerful = rich/full-bodied;
   bubbles = sparkling;
   crisp may relate to dry/light/fresh styles.
7. Confidence must be:
   Strong possible match,
   Possible match,
   or Weak possible match.
8. Explain the database characteristics supporting each match.
9. Mention a relevant mismatch if useful.
10. If the description is too vague, set enough_information to false,
    return no matches, and ask one short clarifying question.
11. Do not claim current availability.
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


# =========================================================
# VALIDATE AI RESPONSE
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
    already_used = set()

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

        # Reject anything Gemini invented.
        if record_id not in allowed:
            continue

        if record_id in already_used:
            continue

        confidence = str(
            match.get(
                "confidence",
                "Possible match"
            )
        ).strip()

        if confidence not in valid_confidences:
            confidence = "Possible match"

        reason = str(
            match.get(
                "reason",
                "This wine matches some of the remembered details."
            )
        ).strip()

        results.append(
            {
                "wine": allowed[record_id],
                "confidence": confidence,
                "reason": reason
            }
        )

        already_used.add(record_id)

        if len(results) == 3:
            break

    return results


# =========================================================
# DISPLAY WINE
# =========================================================

def display_wine(
    wine,
    position=None,
    confidence=None,
    reason=None
):

    rank_html = ""

    if position is not None:
        rank_html = (
            '<div class="wine-rank">'
            f"Match {position}"
            "</div>"
        )

    tags = []

    if wine["type"]:
        tags.append(wine["type"])

    if wine["country"]:
        tags.append(wine["country"])

    if wine["style"]:
        tags.append(wine["style"])

    tag_html = "".join(
        f'<span class="tag">{tag}</span>'
        for tag in tags
    )

    reason_html = ""

    if reason:
        reason_html = (
            '<div class="wine-detail">'
            "<strong>Why this may match:</strong> "
            f"{reason}"
            "</div>"
        )

    confidence_html = ""

    if confidence:
        confidence_html = (
            '<div class="wine-detail">'
            "<strong>Confidence:</strong> "
            f"{confidence}"
            "</div>"
        )

    st.markdown(
        f"""
        <div class="wine-card">
            {rank_html}

            <div class="wine-name">
                {wine["name"]}
            </div>

            <div>
                {tag_html}
            </div>

            <div class="wine-detail">
                <strong>Tasting:</strong>
                {wine["event"]}
            </div>

            {reason_html}
            {confidence_html}
        </div>
        """,
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

        <h1>
            Find the wine you remember.
        </h1>

        <p>
            Choose a tasting if you remember it, add whatever details
            you know, and let AI compare your description with the
            WineHouse tasting and wine records.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STEP 1 - TASTING
# =========================================================

st.markdown(
    '<div class="section-label">Step one</div>',
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

            tasting_candidates = create_candidates(
                selected_wines,
                event_name_lookup
            )

            for wine in tasting_candidates:
                display_wine(wine)

else:

    st.info(
        "If you do not remember the tasting, the finder "
        "can search across all available wine records."
    )


# =========================================================
# STEP 2 - DETAILS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-label">Step two</div>',
    unsafe_allow_html=True
)

st.subheader(
    "What do you remember about the wine?"
)


left, right = st.columns(2)


with left:

    wine_types = sorted(
        type_name
        for type_name in event_wines[
            "WineType"
        ].unique().tolist()
        if type_name
        and type_name != "Other"
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


with right:

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
# STEP 3 - SEARCH
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
    "Search wines",
    type="primary",
    use_container_width=True
):

    supplied_information = sum(
        [
            selected_event_id is not None,
            selected_type != UNKNOWN,
            selected_country != UNKNOWN,
            bool(description.strip())
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
                "No wines match all of the selected details. "
                "Try changing one answer to 'I don't remember'."
            )


        elif not description.strip():

            candidates = create_candidates(
                filtered,
                event_name_lookup
            )

            st.markdown(
                "## Matching wines"
            )

            st.write(
                "These wines match the filters you selected. "
                "Add a description if you want AI to rank them."
            )

            for wine in candidates:
                display_wine(wine)


        else:

            candidates = create_candidates(
                filtered,
                event_name_lookup
            )

            with st.spinner(
                "Comparing your description with the wine records..."
            ):

                ai_result = rank_with_ai(
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
                        "to identify the wine confidently."
                    )

                    question = str(
                        ai_result.get(
                            "clarifying_question",
                            ""
                        )
                    ).strip()

                    if question:
                        st.write(
                            f"**One helpful question:** {question}"
                        )


                else:

                    matches = validate_matches(
                        ai_result,
                        candidates
                    )


                    if not matches:

                        st.warning(
                            "No reliable match was returned. "
                            "Try adding another detail."
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
                                confidence=match["confidence"],
                                reason=match["reason"]
                            )


                        st.markdown(
                            """
                            <div class="verification">
                                Current bottle availability should be
                                checked separately before purchase.
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
        WineHouse Wine Finder
    </div>
    """,
    unsafe_allow_html=True
)
