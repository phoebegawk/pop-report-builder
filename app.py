import streamlit as st

from pop_utils_web import parse_filename, generate_presentation_from_uploads

st.set_page_config(page_title="PoP Report Builder", layout="wide")

HEADER_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/Header-PoPReportBuilder.png"

# Header
st.image(HEADER_URL, use_container_width=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* GLOBAL BACKGROUND + FONT */
    html, body, .stApp, .stAppViewContainer, .main {
        background-color: #542D54 !important;
        color: #FFFFFF !important;
        font-family: "Montserrat", sans-serif !important;
    }

    /* Remove menu + footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Remove Streamlit warning/toolbar */
    [data-testid="stNotification"], .stNotification, .stAlert, .stToolbar {
        display: none !important;
    }

    /* Default text = WHITE */
    * {
        color: #FFFFFF !important;
    }

    /* ------------------------------------------------------ */
    /* FIX 1 — FILE UPLOADER DROPZONE TEXT → GAWK PURPLE ONLY */
    /* ------------------------------------------------------ */

    /* Strongest selector to override the global white rule */
    .stApp div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] * {
        color: #542D54 !important;
    }

    /* Dropzone icon */
    .stApp div[data-testid="stFileUploaderDropzone"] svg {
        fill: #542D54 !important;
    }

    /* “Browse files” button */
    div[data-testid="stFileUploader"] button {
        color: #542D54 !important;
        background-color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        font-family: "Montserrat", sans-serif !important;
    }

    /* Fix: uploaded file list (white) */
    div[data-testid="stFileUploaderDropzone"] + div * {
        color: #FFFFFF !important;
    }

    /* Remove white chips around uploaded files */
    div[data-testid="stFileUploaderFile"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Delete (X) button styling */
    div[data-testid="stFileUploaderFile"] button {
        background: #542D54 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 6px !important;
    }

    /* -------------------------------------- */
    /* FIX 2 — PAGINATION ARROWS (Next / Prev) */
    /* -------------------------------------- */

    button[aria-label="Next"],
    button[aria-label="Previous"] {
        background: #542D54 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }

    button[aria-label="Next"]:hover,
    button[aria-label="Previous"]:hover {
        background: #6a3a6a !important;
        border-color: #FFFFFF !important;
    }

    /* -------------------------------------- */
    /* TABLE — FULL WIDTH / SMALLER TEXT / NOWRAP */
    /* -------------------------------------- */

    div[data-testid="stHorizontalBlock"],
    div[data-testid="stVerticalBlock"],
    div[data-testid="stDataFrame"] {
        width: 100% !important;
        min-width: 100% !important;
    }

    /* Table text size + nowrap */
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] th {
        font-size: 0.85rem !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }

    /* Horizontal scroll for extra-long rows */
    div[data-testid="stDataFrame"] {
        overflow-x: auto !important;
    }

    /* Pagination + helper text */
    .st-emotion-cache-1y4p8pa,
    .st-emotion-cache-1m8g1qv,
    div[data-testid="stDataFrame"] p {
        color: #FFFFFF !important;
    }

    /* -------------------------------------- */
    /* BUTTONS (Generate PoP Report + Download) */
    /* -------------------------------------- */

    .stButton > button,
    .stDownloadButton > button {
        background-color: #D7DF23 !important;
        color: #542D54 !important;
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        border: none !important;
        font-weight: 700 !important;
        font-family: "Montserrat", sans-serif !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }

    .stButton > button:disabled,
    .stDownloadButton > button:disabled {
        background-color: #d0c0d3 !important;
        color: #777777 !important;
        opacity: 0.5 !important;
    }

    /* -------------------------------------- */
    /* PAGE WIDTH + HEADINGS */
    /* -------------------------------------- */

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1500px !important; /* WIDEST safe width */
    }

    .pop-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #FFFFFF !important;
        text-align: center !important;
    }

    .pop-subtitle {
        font-size: 0.95rem;
        opacity: 0.85;
        margin-bottom: 1.5rem;
        color: #FFFFFF !important;
        text-align: center !important;
    }

    /* Fix Streamlit header bar */
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    header,
    .st-emotion-cache-18ni7ap {
        background-color: #542D54 !important;
    }

    /* File uploader rounding */
    .st-emotion-cache-9j8j93,
    .st-emotion-cache-1vbkxwb {
        border-radius: 12px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="pop-title">Image file naming must follow = Site Name - Site Code - Client - Campaign - DDMMYY - Type.ext</div>',
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    "Drag and drop or browse",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

valid_files = []
file_rows = []

if uploaded_files:
    for f in uploaded_files:
        info = parse_filename(f)
        if info is None:
            status = "❌ Invalid name"
        else:
            status = "✅"
            valid_files.append(f)

        file_rows.append(
            {
                "File": f.name,
                "Site": info["site_name"] if info else "-",
                "Client": info["client"] if info else "-",
                "Campaign": info["campaign"] if info else "-",
                "Live Date": info["live_date_display"] if info else "-",
                "Status": status,
            }
        )

if file_rows:
    st.table(file_rows)

generate_disabled = not valid_files
generate = st.button("Generate PoP Report", disabled=generate_disabled)

pptx_bytes = None
pptx_name = None

if generate and valid_files:
    try:
        pptx_bytes, pptx_name = generate_presentation_from_uploads(valid_files)
        st.success("PoP Report generated successfully.")
    except Exception as e:
        st.error(f"Something went wrong while building the report: {e}")

if pptx_bytes is not None:
    st.download_button(
        "Download PoP Report",
        data=pptx_bytes,
        file_name=pptx_name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
