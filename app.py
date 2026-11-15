import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="WineHouse Wine Finder",
    page_icon="🍷",
    layout="wide"
)

# ---------------------------------------------------------
# DEMO DATA
# Replace this later with exported Azure data.
# Each tasting contains six wines.
# ---------------------------------------------------------

wines = [
    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "2026-03-13",
        "name": "Santorini Assyrtiko",
        "type": "White",
        "country": "Greece",
        "style": "Dry",
        "notes": "crisp citrus lemon mineral salty fresh",
        "status": "Proposed"
    },
    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "2026-03-13",
        "name": "Moschofilero",
        "type": "White",
        "country": "Greece",
        "style": "Aromatic",
        "notes": "floral rose citrus light fresh",
        "status": "Proposed"
    },
    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "2026-03-13",
        "name": "Agiorgitiko",
        "type": "Red",
        "country": "Greece",
        "style": "Medium-bodied",
        "notes": "red berries cherry soft spice",
        "status": "Proposed"
    },
    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "2026-03-13",
        "name": "Xinomavro",
        "type": "Red",
        "country": "Greece",
        "style": "Full-bodied",
        "notes": "dark fruit tomato herbs earthy tannins",
        "status": "Proposed"
    },
    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "2026-03-13",
        "name": "Greek Rosé",
        "type": "Rosé",
        "country": "Greece",
        "style": "Dry",
        "notes": "strawberry watermelon fresh light",
        "status": "Proposed"
    },
    {
        "event": "13 March 2026 | Greek Wines & Meze",
        "date": "2026-03-13",
        "name": "Mavrodaphne",
        "type": "Dessert",
        "country": "Greece",
        "style": "Sweet",
        "notes": "raisins dried fruit caramel sweet",
        "status": "Proposed"
    },
    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "2026-07-10",
        "name": "Pinot Grigio",
        "type": "White",
        "country": "Italy",
        "style": "Light",
        "notes": "pear citrus crisp light refreshing",
        "status": "Proposed"
    },
    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "2026-07-10",
        "name": "Vermentino",
        "type": "White",
        "country": "Italy",
        "style": "Dry",
        "notes": "lemon herbs mineral salty fresh",
        "status": "Proposed"
    },
    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "2026-07-10",
        "name": "Prosecco",
        "type": "Sparkling",
        "country": "Italy",
        "style": "Fresh",
        "notes": "apple pear floral light bubbles",
        "status": "Proposed"
    },
    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "2026-07-10",
        "name": "Chianti Classico",
        "type": "Red",
        "country": "Italy",
        "style": "Medium-bodied",
        "notes": "cherry herbs red fruit earthy",
        "status": "Proposed"
    },
    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "2026-07-10",
        "name": "Valpolicella",
        "type": "Red",
        "country": "Italy",
        "style": "Light",
        "notes": "sour cherry red berries light soft",
        "status": "Proposed"
    },
    {
        "event": "10 July 2026 | Italian Summer Wines",
        "date": "2026-07-10",
        "name": "Italian Rosato",
        "type": "Rosé",
        "country": "Italy",
        "style": "Dry",
        "notes": "strawberry peach fresh summer",
        "status": "Proposed"
    },
    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "2026-10-09",
        "name": "Primitivo",
        "type": "Red",
        "country": "Italy",
        "style": "Full-bodied",
        "notes": "plum blackberry jam spice rich",
        "status": "Proposed"
    },
    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "2026-10-09",
        "name": "Italian Pinot Noir",
        "type": "Red",
        "country": "Italy",
        "style": "Light",
        "notes": "cherry raspberry earthy light",
        "status": "Proposed"
    },
    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "2026-10-09",
        "name": "French Pinot Noir",
        "type": "Red",
        "country": "France",
        "style": "Light",
        "notes": "red berries cherry mushroom earthy",
        "status": "Proposed"
    },
    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "2026-10-09",
        "name": "Rioja Reserva",
        "type": "Red",
        "country": "Spain",
        "style": "Full-bodied",
        "notes": "dark cherry vanilla oak spice",
        "status": "Proposed"
    },
    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "2026-10-09",
        "name": "Malbec",
        "type": "Red",
        "country": "Argentina",
        "style": "Full-bodied",
        "notes": "blackberry plum chocolate rich",
        "status": "Proposed"
    },
    {
        "event": "9 October 2026 | Autumn Reds",
        "date": "2026-10-09",
        "name": "Côtes du Rhône",
        "type": "Red",
        "country": "France",
        "style": "Medium-bodied",
        "notes": "black fruit pepper herbs spice",
        "status": "Proposed"
    }
]

UNKNOWN = "I don't remember"


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def normalise(text):
    return str(text).lower().strip()


def calculate_match(wine, selected_type, selected_country,
                    selected_style, taste_words):
    score = 0
    reasons = []

    if selected_type != UNKNOWN:
        if normalise(wine["type"]) == normalise(selected_type):
            score += 4
            reasons.append(f"{wine['type']} wine")
        else:
            score -= 2

    if selected_country != UNKNOWN:
        if normalise(wine["country"]) == normalise(selected_country):
            score += 4
            reasons.append(f"from {wine['country']}")
        else:
            score -= 2

    if selected_style != UNKNOWN:
        if normalise(selected_style) in normalise(wine["style"]):
            score += 3
            reasons.append(f"{wine['style']} style")

    if taste_words:
        searchable_text = normalise(
            wine["name"] + " " +
            wine["type"] + " " +
            wine["country"] + " " +
            wine["style"] + " " +
            wine["notes"]
        )

        words = [
            word.strip(".,!?")
            for word in normalise(taste_words).split()
            if len(word.strip(".,!?")) >= 3
        ]

        matched_words = []

        for word in words:
            if word in searchable_text:
                score += 2
                matched_words.append(word)

        if matched_words:
            reasons.append(
                "matching description: " +
                ", ".join(matched_words[:5])
            )

    return score, reasons


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("🍷 WineHouse Wine Finder")

st.write(
    "Help a guest identify a wine remembered from a past tasting. "
    "Enter only the details the guest remembers."
)

st.info(
    "Prototype notice: This version uses synthetic demonstration data. "
    "Suggested wines must be verified against the event record. "
    "The application does not confirm current stock availability."
)

# ---------------------------------------------------------
# TASTING SELECTION
# ---------------------------------------------------------

st.subheader("1. Which tasting does the guest remember?")

event_names = sorted(set(wine["event"] for wine in wines))
event_options = [UNKNOWN] + event_names

selected_event = st.selectbox(
    "Tasting date and theme",
    event_options
)

if selected_event != UNKNOWN:
    candidate_wines = [
        wine for wine in wines
        if wine["event"] == selected_event
    ]

    st.success(
        f"{len(candidate_wines)} wines are linked to this tasting."
    )

    with st.expander("Show wines linked to this tasting"):
        for wine in candidate_wines:
            st.markdown(
                f"**{wine['name']}**  \n"
                f"{wine['type']} | {wine['country']} | "
                f"{wine['style']} | Status: {wine['status']}"
            )
else:
    candidate_wines = wines

    st.caption(
        "The tasting is unknown, so the finder will search across "
        "all available tasting-wine records."
    )

# ---------------------------------------------------------
# WINE DESCRIPTION
# ---------------------------------------------------------

st.subheader("2. What does the guest remember?")

col1, col2 = st.columns(2)

with col1:
    wine_types = sorted(set(wine["type"] for wine in wines))

    selected_type = st.selectbox(
        "Wine colour or type",
        [UNKNOWN] + wine_types
    )

    countries = sorted(set(wine["country"] for wine in wines))

    selected_country = st.selectbox(
        "Country of origin",
        [UNKNOWN] + countries
    )

with col2:
    styles = sorted(set(wine["style"] for wine in wines))

    selected_style = st.selectbox(
        "Wine style",
        [UNKNOWN] + styles
    )

    taste_words = st.text_input(
        "Taste, smell or other details",
        placeholder="For example: cherry, citrus, mineral, light, sweet..."
    )

# ---------------------------------------------------------
# SEARCH BUTTON
# ---------------------------------------------------------

st.subheader("3. Find likely matches")

if st.button("🔎 Find my wine", type="primary", use_container_width=True):

    remembered_answers = 0

    if selected_event != UNKNOWN:
        remembered_answers += 1

    if selected_type != UNKNOWN:
        remembered_answers += 1

    if selected_country != UNKNOWN:
        remembered_answers += 1

    if selected_style != UNKNOWN:
        remembered_answers += 1

    if taste_words.strip():
        remembered_answers += 1

    if remembered_answers == 0:
        st.warning(
            "Not enough information to identify the wine. "
            "Please add at least one remembered detail."
        )

    else:
        ranked_results = []

        for wine in candidate_wines:
            score, reasons = calculate_match(
                wine,
                selected_type,
                selected_country,
                selected_style,
                taste_words
            )

            ranked_results.append({
                "wine": wine,
                "score": score,
                "reasons": reasons
            })

        ranked_results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        positive_results = [
            result for result in ranked_results
            if result["score"] > 0
        ]

        if not positive_results:
            st.warning(
                "No confident match was found. Try changing one answer "
                "or adding another taste or smell detail."
            )

        else:
            st.subheader("Most likely matches")

            top_results = positive_results[:3]

            for position, result in enumerate(top_results, start=1):
                wine = result["wine"]
                score = result["score"]
                reasons = result["reasons"]

                if score >= 8:
                    confidence = "Strong possible match"
                elif score >= 4:
                    confidence = "Possible match"
                else:
                    confidence = "Weak possible match"

                with st.container(border=True):
                    st.markdown(
                        f"### {position}. {wine['name']}"
                    )

                    st.write(
                        f"**{wine['type']} | {wine['country']} | "
                        f"{wine['style']}**"
                    )

                    st.write(
                        f"**Tasting:** {wine['event']}"
                    )

                    st.write(
                        f"**Stored notes:** {wine['notes']}"
                    )

                    if reasons:
                        st.write(
                            "**Why it may match:** " +
                            "; ".join(reasons)
                        )

                    st.write(
                        f"**Confidence:** {confidence}"
                    )

                    st.caption(
                        f"Event-wine status: {wine['status']}"
                    )

            st.warning(
                "Staff verification required: confirm the wine against "
                "the event record and check current availability before "
                "answering the guest."
            )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "WineHouse Wine Finder | Data and AI project prototype | "
    "Synthetic demonstration data"
)
