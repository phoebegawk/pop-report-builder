import streamlit as st

from pop_utils_web import parse_filename, generate_presentation_from_uploads

st.set_page_config(page_title="PoP Report Builder", layout="wide")

HEADER_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/Header-PoPReportBuilder.png"

# Header
st.image(HEADER_URL, width="stretch")

# --------------------------------------------------------------
# STYLE BLOCK (ALL VISUAL LOGIC)
# --------------------------------------------------------------
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

    #MainMenu, footer { visibility: hidden !important; }
    [data-testid="stNotification"], .stAlert, .stToolbar { display: none !important; }

    /* TOP STREAMLIT HEADER BAR */
    header[data-testid="stHeader"],
    header[data-testid="stHeader"] * {
        background-color: #542D54 !important;
        color: #FFFFFF !important;
    }

    /* HIDE FILE UPLOADER LABEL (BUT KEEP IT IN PYTHON) */
    div[data-testid="stFileUploader"] label {
        display: none !important;
        visibility: hidden !important;
    }

    /* FILE UPLOADER DROPZONE — GAWK PURPLE TEXT */
    div[data-testid="stFileUploaderDropzone"] * {
        color: #542D54 !important;
        fill: #542D54 !important;
        opacity: 1 !important;
    }

    div[data-testid="stFileUploaderDropzone"] svg {
        fill: #542D54 !important;
    }

    /* Browse Files button */
    div[data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #542D54 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }

    /* REMOVE FILE LIST / CHIPS / DELETE / PAGINATION */
    div[data-testid="stFileUploaderUploadedFiles"],
    div[data-testid="stFileUploaderFile"],
    ul[role="listbox"],
    li[role="option"],
    div[data-testid="stPagination"],
    div[data-testid="stPaginator"],
    div[aria-label="Pagination"],
    div[class*="pagination"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* TABLE STYLING */
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] th {
        font-size: 0.85rem !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }
    div[data-testid="stDataFrame"] {
        overflow-x: auto !important;
    }

    /* BUTTON STYLING (Gawk Green + Purple Text) */
    .stButton > button,
    .stDownloadButton > button {
        background-color: #D7DF23 !important;
        color: #542D54 !important;
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        border: none !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }

    /* PAGE WIDTH */
    .block-container {
        max-width: 1500px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }

    .pop-title, .pop-subtitle {
        text-align: center !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------
# TITLE
# --------------------------------------------------------------
st.markdown(
    '<div class="pop-title">Image file naming must follow = Site Name - Site Code - Client - Campaign - DDMMYY - Type.ext</div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------
# FILE UPLOADER (label required to avoid TypeError)
# --------------------------------------------------------------
uploaded_files = st.file_uploader(
    "upload",                        # required but hidden via CSS
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

# --------------------------------------------------------------
# FILE PARSING + TABLE
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# GENERATE PRESENTATION
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------------------
if pptx_bytes is not None:
    st.download_button(
        "Download PoP Report",
        data=pptx_bytes,
        file_name=pptx_name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
