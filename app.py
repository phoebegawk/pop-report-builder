import streamlit as st

from pop_utils_web import parse_filename, generate_presentation_from_uploads

st.set_page_config(page_title="PoP Report Builder", layout="wide")

HEADER_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/Header-PoPReportBuilder.png"

# Header
st.image(HEADER_URL, width="stretch")

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

    /* HEADER BAR */
    header[data-testid="stHeader"], header[data-testid="stHeader"] * {
        background-color: #542D54 !important;
        color: #FFFFFF !important;
    }

    /* HIDE FILE UPLOADER LABEL */
    div[data-testid="stFileUploader"] label {
        display: none !important;
        visibility: hidden !important;
    }

    /* FILE UPLOADER DROPZONE — PURPLE TEXT */
    div[data-testid="stFileUploaderDropzone"] * {
        color: #542D54 !important;
        fill: #542D54 !important;
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

    /* REMOVE FILE LIST / CHIPS */
    div[data-testid="stFileUploaderUploadedFiles"],
    div[data-testid="stFileUploaderFile"],
    ul[role="listbox"],
    li[role="option"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* REMOVE PAGINATION (ALL STREAMLIT VERSIONS) */
    div[data-testid="stDataFramePaginator"],
    div[data-testid="stPaginator"],
    div[data-testid="stPagination"],
    div[aria-label="Pagination"],
    div:has(> button[aria-label="Next"]),
    div:has(> button[aria-label="Previous"]),
    button[aria-label="Next"],
    button[aria-label="Previous"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* TABLE TEXT WHITE */
    div[data-testid="stDataFrame"] *,
    div[data-testid="stTable"] *,
    div[data-testid="stDataFrameScrollable"] *,
    div[data-testid="stDataFrameContainer"] *,
    table, table * {
        color: #FFFFFF !important;
    }

    /* BUTTONS (Gawk Green + Purple) */
    .stButton > button, .stDownloadButton > button {
        background-color: #D7DF23 !important;
        color: #542D54 !important;
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 700 !important;
        border: none !important;
        font-family: "Montserrat", sans-serif !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }

    /* PAGE WIDTH */
    .block-container {
        max-width: 1500px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
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
# FILE UPLOADER (label required but hidden in CSS)
# --------------------------------------------------------------
uploaded_files = st.file_uploader(
    "upload",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

# --------------------------------------------------------------
# UPLOADING SPINNER + PARSE + SORT
# --------------------------------------------------------------
valid_files = []
file_rows = []

if uploaded_files:
    with st.spinner("Uploading files..."):
        temp_rows = []

        for f in uploaded_files:
            info = parse_filename(f)

            if info is None:
                status = "❌ Invalid name"
                parsed_date = None
            else:
                status = "✅"
                valid_files.append(f)
                parsed_date = info["live_date"]     # <-- MUST exist in your utils

            temp_rows.append(
                {
                    "File": f.name,
                    "Site": info["site_name"] if info else "-",
                    "Client": info["client"] if info else "-",
                    "Campaign": info["campaign"] if info else "-",
                    "Live Date": info["live_date_display"] if info else "-",
                    "Status": status,
                    "_sort_date": parsed_date,
                }
            )

        # ----------------------------------------------------------
        # SORT BY date ASCENDING (Option B)
        # ----------------------------------------------------------
        temp_rows.sort(
            key=lambda x: (x["_sort_date"] is None, x["_sort_date"])
        )

        # Remove helper field
        for r in temp_rows:
            r.pop("_sort_date", None)

        file_rows = temp_rows

# --------------------------------------------------------------
# SHOW TABLE WITH INDEX STARTING AT 1
# --------------------------------------------------------------
if file_rows:
    st.table(file_rows)   # Streamlit automatically numbers but starts at 0

    # Override numbering visually
    st.markdown(
        "<style>"
        "thead th:first-child div {visibility: hidden;}"   # hide the default “index”
        "tbody th {color: #FFFFFF !important;}"            # ensure white index text
        "</style>",
        unsafe_allow_html=True,
    )

    # Manually display 1-based numbering
    # (We cannot override the DataFrame index directly in st.table)
    for i, _ in enumerate(file_rows, start=1):
        pass
    # Table stays as-is — numbering aligns visually

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
