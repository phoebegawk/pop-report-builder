import streamlit as st
from pop_utils_web import parse_filename, generate_presentation_from_uploads

st.set_page_config(
    page_title="PoP Report Builder",
    layout="wide",
    page_icon="assets/favicon.png",
)

HEADER_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/Header-PoPReportBuilder.png"
BG_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/PoPReportBuilder-BG.png"

# ---------------------------
# Session State Init
# ---------------------------
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0
if "reset_nonce" not in st.session_state:
    st.session_state["reset_nonce"] = 0
if "pptx_bytes" not in st.session_state:
    st.session_state["pptx_bytes"] = None
if "pptx_name" not in st.session_state:
    st.session_state["pptx_name"] = None

# One flag for ANY full-screen overlay usage (parsing OR generating)
if "overlay_active" not in st.session_state:
    st.session_state["overlay_active"] = False
if "overlay_message" not in st.session_state:
    st.session_state["overlay_message"] = "Uploading…"
if "overlay_submessage" not in st.session_state:
    st.session_state["overlay_submessage"] = "Processing files and building the table."

# ---------------------------
# Callbacks
# ---------------------------
def reset_all():
    st.session_state["pptx_bytes"] = None
    st.session_state["pptx_name"] = None

    st.session_state["overlay_active"] = False
    st.session_state["overlay_message"] = "Uploading…"
    st.session_state["overlay_submessage"] = "Processing files and building the table."

    st.session_state["uploader_key"] += 1
    st.session_state["reset_nonce"] += 1

    st.rerun()


def on_upload_change():
    # Fires AFTER browser finishes uploading and Streamlit receives the files.
    st.session_state["overlay_active"] = True
    st.session_state["overlay_message"] = "Uploading…"
    st.session_state["overlay_submessage"] = "Processing files and building the table."
    st.session_state["pptx_bytes"] = None
    st.session_state["pptx_name"] = None


# ---------------------------
# Header + Styles
# ---------------------------
st.image(HEADER_URL, width="stretch")

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* FORCE MONTSERRAT */
    html, body, .stApp, .stApp * {{
        font-family: "Montserrat", sans-serif !important;
    }}

    html, body, .stApp {{ height: 100%; }}

    .stApp {{
        background-image: url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #FFFFFF !important;
    }}

    .stAppViewContainer, .main, .block-container {{
        background: transparent !important;
    }}

    #MainMenu, footer {{ visibility: hidden !important; }}
    [data-testid="stNotification"], .stAlert, .stToolbar {{ display: none !important; }}

    header[data-testid="stHeader"], header[data-testid="stHeader"] * {{
        background: transparent !important;
        color: #FFFFFF !important;
    }}

    .pop-title {{
        text-align: center !important;
        width: 100%;
        margin: 0 auto;
        font-weight: 700;
        color: #FFFFFF !important;
    }}

    /* Uploader sizing */
    div[data-testid="stFileUploader"] {{
        width: 100% !important;
        max-width: 1180px !important;
        margin: 0 auto !important;
    }}

    /* Hide uploader label */
    div[data-testid="stFileUploader"] label {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* Dropzone text + icon -> purple */
    div[data-testid="stFileUploaderDropzone"] * {{
        color: #542D54 !important;
        fill: #542D54 !important;
    }}
    div[data-testid="stFileUploaderDropzone"] svg {{
        fill: #542D54 !important;
    }}

    /* Also force the small uploader subtext (file limit etc) to purple */
    div[data-testid="stFileUploaderDropzone"] small {{
        color: #542D54 !important;
        opacity: 1 !important;
    }}

    /* Browse files button */
    div[data-testid="stFileUploader"] button {{
        background-color: #FFFFFF !important;
        color: #542D54 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: 1px solid rgba(84,45,84,0.35) !important;
    }}

    /* Remove file list / chips */
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

    /* Table text white */
    div[data-testid="stDataFrame"] *,
    div[data-testid="stTable"] *,
    div[data-testid="stDataFrameScrollable"] *,
    div[data-testid="stDataFrameContainer"] *,
    table, table * {{
        color: #FFFFFF !important;
    }}

    /* Buttons */
    .stButton > button, .stDownloadButton > button {{
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 700 !important;
        border: none !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
        opacity: 1 !important; /* stop grey fade */
    }}

    /* Primary = Gawk Green */
    .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {{
        background-color: #D7DF23 !important;
        color: #542D54 !important;
    }}
    .stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {{
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }}

    /* Secondary = Pink */
    .stButton > button[kind="secondary"] {{
        background-color: #C99CCA !important;
        color: #542D54 !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background-color: #B889B8 !important;
        color: #542D54 !important;
    }}

    /* Disabled buttons: keep readable (no grey text) */
    .stButton > button:disabled,
    .stDownloadButton > button:disabled {{
        opacity: 0.55 !important;
        color: #542D54 !important;
        cursor: not-allowed !important;
    }}

    /* Page width */
    .block-container {{
        max-width: 1500px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }}

    /* ---------------------------
       FULLSCREEN OVERLAY (Uploading)
       --------------------------- */
    .overlay {{
        position: fixed;
        inset: 0;
        background: rgba(30, 10, 30, 0.55);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .overlay-card {{
        width: min(520px, 90vw);
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 16px;
        padding: 24px 26px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }}

    .overlay-title {{
        font-size: 22px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 12px;
        margin-bottom: 6px;
    }}

    .overlay-sub {{
        font-size: 14px;
        font-weight: 600;
        color: rgba(255,255,255,0.85);
        margin: 0;
    }}

    .overlay-spinner {{
        width: 54px;
        height: 54px;
        margin: 0 auto;
        border-radius: 50%;
        border: 6px solid rgba(255,255,255,0.22);
        border-top-color: #D7DF23; /* Gawk Green */
        animation: spin 1s linear infinite;
    }}

    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Overlay Renderer (top of page)
# ---------------------------
overlay_placeholder = st.empty()

def render_overlay():
    if st.session_state.get("overlay_active"):
        overlay_placeholder.markdown(
            f"""
            <div class="overlay">
              <div class="overlay-card">
                <div class="overlay-spinner"></div>
                <div class="overlay-title">{st.session_state.get("overlay_message","Uploading…")}</div>
                <p class="overlay-sub">{st.session_state.get("overlay_submessage","Processing…")}</p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        overlay_placeholder.empty()

render_overlay()

# ---------------------------
# Title
# ---------------------------
st.markdown(
    '<div class="pop-title"><b>Image File Naming Convention ➡️ Site Name - Site Code - Client - Campaign - DDMMYY - Type.ext</b></div>',
    unsafe_allow_html=True,
)
st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# ---------------------------
# Uploader (keyed so Reset clears it)
# ---------------------------
uploaded_files = st.file_uploader(
    "upload",  # hidden by CSS
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state['uploader_key']}",
    on_change=on_upload_change,
)

# ---------------------------
# Parse + Sort (table build)
# ---------------------------
valid_files = []
file_rows = []

if uploaded_files:
    # If user uploaded but callback didn’t fire for some reason, still protect UX:
    if not st.session_state.get("overlay_active"):
        st.session_state["overlay_active"] = True
        st.session_state["overlay_message"] = "Uploading…"
        st.session_state["overlay_submessage"] = "Processing files and building the table."
        render_overlay()

    try:
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

    finally:
        # ALWAYS clear overlay, even if parse_filename throws.
        st.session_state["overlay_active"] = False
        render_overlay()

# ---------------------------
# Show Table
# ---------------------------
if file_rows:
    st.table(file_rows)

# ---------------------------
# Buttons Row
# ---------------------------
generate_disabled = not valid_files
nonce = st.session_state["reset_nonce"]

left_spacer, col1, gap, col2, right_spacer = st.columns([3, 2, 0.25, 2, 3], gap="large")

with col1:
    generate = st.button(
        "Generate Report",
        disabled=generate_disabled,
        type="primary",
        use_container_width=True,
        key=f"generate_report_btn_{nonce}",
    )

with col2:
    st.button(
        "Reset All",
        type="secondary",
        use_container_width=True,
        key=f"reset_all_btn_{nonce}",
        on_click=reset_all,
    )

# ---------------------------
# Generation
# ---------------------------
if generate and valid_files:
    st.session_state["overlay_active"] = True
    st.session_state["overlay_message"] = "Building report…"
    st.session_state["overlay_submessage"] = "Generating your PowerPoint."
    render_overlay()

    try:
        pptx_bytes, pptx_name = generate_presentation_from_uploads(valid_files)
        st.session_state["pptx_bytes"] = pptx_bytes
        st.session_state["pptx_name"] = pptx_name
        st.success("PoP Report generated successfully.")
    except Exception as e:
        st.session_state["pptx_bytes"] = None
        st.session_state["pptx_name"] = None
        st.error(f"Something went wrong while building the report: {e}")
    finally:
        st.session_state["overlay_active"] = False
        render_overlay()

# ---------------------------
# Download Button
# ---------------------------
if st.session_state["pptx_bytes"] is not None:
    st.download_button(
        "Download PoP Report",
        data=st.session_state["pptx_bytes"],
        file_name=st.session_state["pptx_name"] or "PoP_Report.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        type="primary",
        use_container_width=False,
        key=f"download_btn_{nonce}",
    )
