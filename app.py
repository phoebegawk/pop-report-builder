import streamlit as st
from pop_utils_web import parse_filename, generate_presentation_from_uploads

st.set_page_config(
    page_title="PoP Report Builder",
    layout="wide",
    page_icon="assets/favicon.png",
)

HEADER_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/Header-PoPReportBuilder.png"
BG_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/PoPReportBuilder-BG.png"

# Header
st.image(HEADER_URL, width="stretch")

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* FORCE MONTSERRAT EVERYWHERE */
    html, body, .stApp, .stApp * {{
        font-family: "Montserrat", sans-serif !important;
    }}

    /* GLOBAL BACKGROUND IMAGE */
    html, body, .stApp {{
        height: 100%;
    }}

    .stApp {{
        background-image: url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #FFFFFF !important;
    }}

    /* MAKE STREAMLIT CONTAINERS TRANSPARENT SO BACKGROUND SHOWS */
    .stAppViewContainer,
    .main,
    .block-container {{
        background: transparent !important;
    }}

    #MainMenu, footer {{ visibility: hidden !important; }}
    [data-testid="stNotification"], .stAlert, .stToolbar {{ display: none !important; }}

    /* HEADER BAR */
    header[data-testid="stHeader"], header[data-testid="stHeader"] * {{
        background: transparent !important;
        color: #FFFFFF !important;
    }}

    /* CENTER THE TITLE LINE */
    .pop-title {{
        text-align: center !important;
        width: 100%;
        margin: 0 auto;
        font-weight: 700;
    }}

    /* CENTER + SIZE THE UPLOADER LIKE "CHECK MY SPECS" */
    div[data-testid="stFileUploader"] {{
        width: 100% !important;
        max-width: 1180px !important;
        margin: 0 auto !important;
    }}

    /* HIDE FILE UPLOADER LABEL */
    div[data-testid="stFileUploader"] label {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* FILE UPLOADER DROPZONE — PURPLE TEXT */
    div[data-testid="stFileUploaderDropzone"] * {{
        color: #542D54 !important;
        fill: #542D54 !important;
    }}
    div[data-testid="stFileUploaderDropzone"] svg {{
        fill: #542D54 !important;
    }}

    /* Browse Files button */
    div[data-testid="stFileUploader"] button {{
        background-color: #FFFFFF !important;
        color: #542D54 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }}

    /* REMOVE FILE LIST / CHIPS */
    div[data-testid="stFileUploaderUploadedFiles"],
    div[data-testid="stFileUploaderFile"],
    ul[role="listbox"],
    li[role="option"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }}

    /* REMOVE ALL PAGINATION (ALL STREAMLIT VERSIONS) */
    div[data-testid="stDataFramePaginator"],
    div[data-testid="stPaginator"],
    div[data-testid="stPagination"],
    div[aria-label="Pagination"],
    div:has(> button[aria-label="Next"]),
    div:has(> button[aria-label="Previous"]),
    button[aria-label="Next"],
    button[aria-label="Previous"],
    div[data-testid="stDataFrame"] > div:nth-child(1):has(span),
    div[data-testid="stDataFrame"] span:contains("Showing page") {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* TABLE TEXT WHITE */
    div[data-testid="stDataFrame"] *,
    div[data-testid="stTable"] *,
    div[data-testid="stDataFrameScrollable"] *,
    div[data-testid="stDataFrameContainer"] *,
    table, table * {{
        color: #FFFFFF !important;
    }}

    /* BUTTONS (Gawk Green + Purple) */
    .stButton > button, .stDownloadButton > button {{
        background-color: #D7DF23 !important;
        color: #542D54 !important;
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 700 !important;
        border: none !important;
        font-family: "Montserrat", sans-serif !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }}

    /* RESET ALL BUTTON (PINK) - STABLE HOOK */
    .pop-reset-btn .stButton > button {{
        background-color: #C99CCA !important;
        color: #542D54 !important;
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 700 !important;
        border: none !important;
        font-family: "Montserrat", sans-serif !important;
    }}
    .pop-reset-btn .stButton > button:hover {{
        background-color: #B889B8 !important;
        color: #542D54 !important;
    }}

    /* PAGE WIDTH */
    .block-container {{
        max-width: 1500px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }}

    /*
      BUTTON ROW LAYOUT (proper fix):
      - keep the two buttons in their own centered row
      - avoid column stretching that causes mismatched button sizes
    */
    .pop-btn-row {{
        max-width: 1180px !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        gap: 28px !important;
    }}

    /* Make the two Streamlit button containers behave like inline blocks */
    .pop-btn-row .stButton {{
        display: inline-block !important;
    }}

    /* Keep labels from wrapping (prevents height mismatch) */
    .pop-btn-row .stButton > button {{
        white-space: nowrap !important;
        line-height: 1.2 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------
# RESET HANDLER (works any time)
# --------------------------------------------------------------
def reset_all():
    st.session_state.clear()
    st.rerun()


# --------------------------------------------------------------
# TITLE
# --------------------------------------------------------------
st.markdown(
    '<div class="pop-title"><b>Image File Naming Convention ➡️ Site Name - Site Code - Client - Campaign - DDMMYY - Type.ext</b></div>',
    unsafe_allow_html=True,
)

st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------
# FILE UPLOADER (label required but hidden in CSS)
# --------------------------------------------------------------
uploaded_files = st.file_uploader(
    "upload",  # required but hidden by CSS
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

# --------------------------------------------------------------
# PARSE + SORT
# --------------------------------------------------------------
valid_files = []
file_rows = []

if uploaded_files:
    temp_rows = []

    for f in uploaded_files:
        info = parse_filename(f)

        if info is None:
            status = "❌ Invalid name"
            parsed_date = None
        else:
            status = "✅"
            valid_files.append(f)
            parsed_date = info["live_date"]

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

    temp_rows.sort(key=lambda x: (x["_sort_date"] is None, x["_sort_date"]))

    for r in temp_rows:
        r.pop("_sort_date", None)

    file_rows = temp_rows

# --------------------------------------------------------------
# SHOW TABLE
# --------------------------------------------------------------
if file_rows:
    st.table(file_rows)

# --------------------------------------------------------------
# GENERATE PRESENTATION + RESET ALL (MATCH CHECK MY SPECS)
# --------------------------------------------------------------
st.markdown('<div class="pop-btn-row">', unsafe_allow_html=True)

generate_disabled = not valid_files
generate = st.button("Generate Report", disabled=generate_disabled)

st.markdown('<div class="pop-reset-btn">', unsafe_allow_html=True)
reset = st.button("Reset All")
st.markdown("</div>", unsafe_allow_html=True)

if reset:
    reset_all()

st.markdown("</div>", unsafe_allow_html=True)

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
