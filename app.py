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
if "uploading_flag" not in st.session_state:
    st.session_state["uploading_flag"] = False

# ---------------------------
# Callbacks
# ---------------------------
def reset_all():
    # clear generated output
    st.session_state["pptx_bytes"] = None
    st.session_state["pptx_name"] = None
    st.session_state["uploading_flag"] = False

    # force reset widgets (uploader + buttons)
    st.session_state["uploader_key"] += 1
    st.session_state["reset_nonce"] += 1

    st.rerun()

def on_upload_change():
    # Fires after upload completes (browser-side), then app reruns.
    st.session_state["uploading_flag"] = True
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
    }}

    div[data-testid="stFileUploader"] {{
        width: 100% !important;
        max-width: 1180px !important;
        margin: 0 auto !important;
    }}

    div[data-testid="stFileUploader"] label {{
        display: none !important;
        visibility: hidden !important;
    }}

    div[data-testid="stFileUploaderDropzone"] * {{
        color: #542D54 !important;
        fill: #542D54 !important;
    }}
    div[data-testid="stFileUploaderDropzone"] svg {{
        fill: #542D54 !important;
    }}

    div[data-testid="stFileUploader"] button {{
        background-color: #FFFFFF !important;
        color: #542D54 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }}

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

    div[data-testid="stDataFrame"] *,
    div[data-testid="stTable"] *,
    div[data-testid="stDataFrameScrollable"] *,
    div[data-testid="stDataFrameContainer"] *,
    table, table * {{
        color: #FFFFFF !important;
    }}

    .stButton > button, .stDownloadButton > button {{
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 700 !important;
        border: none !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
    }}

    .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {{
        background-color: #D7DF23 !important;
        color: #542D54 !important;
    }}
    .stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {{
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }}

    .stButton > button[kind="secondary"] {{
        background-color: #C99CCA !important;
        color: #542D54 !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background-color: #B889B8 !important;
        color: #542D54 !important;
    }}

    .block-container {{
        max-width: 1500px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }}

    /* =========================
       FULL-SCREEN UPLOADING OVERLAY
       Shows while we are parsing/building table/report.
       ========================= */
    .upload-overlay {{
        position: fixed;
        inset: 0;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(84, 45, 84, 0.65);
        backdrop-filter: blur(4px);
    }}

    .upload-card {{
        width: min(520px, 92vw);
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.30);
        border-radius: 18px;
        padding: 26px 22px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 0 18px 55px rgba(0,0,0,0.35);
    }}

    .upload-title {{
        font-weight: 800;
        font-size: 22px;
        margin: 0 0 6px 0;
        letter-spacing: 0.5px;
    }}

    .upload-sub {{
        font-weight: 600;
        font-size: 15px;
        margin: 0 0 16px 0;
        opacity: 0.95;
    }}

    .loader {{
        width: 68px;
        height: 68px;
        border-radius: 50%;
        border: 7px solid rgba(255,255,255,0.25);
        border-top-color: #D7DF23;
        margin: 0 auto 10px auto;
        animation: spin 0.9s linear infinite;
    }}

    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

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
# Parse + Sort (with full-screen overlay)
# ---------------------------
valid_files = []
file_rows = []

if uploaded_files:
    # Show overlay immediately when we start doing server-side work
    st.markdown(
        """
        <div class="upload-overlay">
            <div class="upload-card">
                <div class="loader"></div>
                <div class="upload-title">Uploading…</div>
                <div class="upload-sub">Processing files and building the table.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    # done processing
    st.session_state["uploading_flag"] = False

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
# Generation (with full-screen overlay)
# ---------------------------
if generate and valid_files:
    st.markdown(
        """
        <div class="upload-overlay">
            <div class="upload-card">
                <div class="loader"></div>
                <div class="upload-title">Building…</div>
                <div class="upload-sub">Generating your PoP Report now.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        pptx_bytes, pptx_name = generate_presentation_from_uploads(valid_files)
        st.session_state["pptx_bytes"] = pptx_bytes
        st.session_state["pptx_name"] = pptx_name
        st.success("PoP Report generated successfully.")
    except Exception as e:
        st.session_state["pptx_bytes"] = None
        st.session_state["pptx_name"] = None
        st.error(f"Something went wrong while building the report: {e}")

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
