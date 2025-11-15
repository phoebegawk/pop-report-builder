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

    /* -------------------------------------------------------------- */
    /* GLOBAL BACKGROUND + FONT                                       */
    /* -------------------------------------------------------------- */
    html, body, .stApp, .stAppViewContainer, .main {
        background-color: #542D54 !important;
        color: #FFFFFF !important;
        font-family: "Montserrat", sans-serif !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stNotification"], .stAlert, .stToolbar {
        display: none !important;
    }

    /* Global text white — allowed, but we override uploader later */
    * { color: #FFFFFF !important; }

    /* -------------------------------------------------------------- */
    /* TOP STREAMLIT HEADER BAR                                       */
    /* -------------------------------------------------------------- */
    header[data-testid="stHeader"],
    header[data-testid="stHeader"] div,
    .st-emotion-cache-18ni7ap,
    .st-emotion-cache-1gulkj5,
    .st-emotion-cache-q8sbsg {
        background-color: #542D54 !important;
    }

    /* -------------------------------------------------------------- */
    /* FILE UPLOADER DROPZONE — FORCE PURPLE TEXT (STRONG OVERRIDE)   */
    /* -------------------------------------------------------------- */

    /* Make EVERYTHING inside dropzone purple unless it's a button */
    div[data-testid="stFileUploaderDropzone"] *:not(button) {
        color: #542D54 !important;
        fill: #542D54 !important;
        opacity: 1 !important;
    }

    /* Cloud icon */
    div[data-testid="stFileUploaderDropzone"] svg {
        fill: #542D54 !important;
    }

    /* Browse button */
    div[data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #542D54 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }

    /* -------------------------------------------------------------- */
    /* REMOVE FILE LIST BELOW UPLOADER                               */
    /* -------------------------------------------------------------- */

    div[data-testid="stFileUploaderUploadedFiles"],
    div[data-testid="stFileUploaderFile"],
    ul[role="listbox"],
    li[role="option"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }

    /* -------------------------------------------------------------- */
    /* REMOVE PAGINATION (“Showing page 1 of 2” + arrows)             */
    /* -------------------------------------------------------------- */

    /* All known paginator containers */
    div[data-testid="stPagination"],
    div[data-testid="stPaginator"],
    div[aria-label="Pagination"],
    div[class*="pagination"],
    div:has(> button[aria-label="Next"]),
    div:has(> button[aria-label="Previous"]),
    div:has(> button[aria-label="Next Page"]),
    div:has(> button[aria-label="Previous Page"]) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* -------------------------------------------------------------- */
    /* TABLE STYLING                                                  */
    /* -------------------------------------------------------------- */
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] th {
        font-size: 0.85rem !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stDataFrame"] {
        overflow-x: auto !important;
    }

    /* -------------------------------------------------------------- */
    /* BUTTONS                                                        */
    /* -------------------------------------------------------------- */
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

    /* -------------------------------------------------------------- */
    /* PAGE WIDTH + HEADINGS                                          */
    /* -------------------------------------------------------------- */
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
