import streamlit as st

from pop_utils_web import parse_filename, generate_presentation_from_uploads

st.set_page_config(page_title="PoP Report Builder", layout="wide")

HEADER_URL = "https://raw.githubusercontent.com/phoebegawk/pop-report-builder/main/assets/Header-PoPReportBuilder.png"

# Header
st.image(HEADER_URL, use_container_width=True)

# Styles – mirrored from Mock Up Machine where possible
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* GLOBAL FONT + BACKGROUND */
    html, body, .stApp, .stAppViewContainer, .main {
        background-color: #542D54 !important;
        color: #FFFFFF !important;
        font-family: "Montserrat", sans-serif !important;
    }

    /* Remove default Streamlit menu & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: visible;}

    /* Streamlit writes many elements using attribute selectors */
    * {
        color: #FFFFFF !important;
    }

    /* Override Streamlit uploader hint text */
    div[data-testid="stFileUploader"] * {
        color: #FFFFFF !important;
    }

    /* Table text (dataframe/table elements) */
    div[data-testid="stDataFrame"] *, 
    .stDataFrame *, 
    .stTable * {
        color: #FFFFFF !important;
    }

    /* Pagination text ("Showing page 1 of X") */
    .st-emotion-cache-1y4p8pa, .st-emotion-cache-1m8g1qv, div[data-testid="stDataFrame"] p {
        color: #FFFFFF !important;
    }

    /* Status text (like “Done!”, errors, warnings) */
    .stAlert, .stToast, [data-testid="stNotification"], [data-testid="stNotificationContent"], .st-emotion-cache-1wdo8hj {
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        background-color: #D7DF23 !important;
        color: #542D54 !important;
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        border: none !important;
        font-weight: 700 !important;
        font-family: "Montserrat", sans-serif !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #C8D51E !important;
        color: #542D54 !important;
    }
    .stButton > button:disabled,
    .stDownloadButton > button:disabled {
        background-color: #d0c0d3 !important;
        color: #777777 !important;
        opacity: 0.5 !important;
    }

    /* Page padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px !important;
    }

    /* Title and subtitle */
    .pop-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #FFFFFF !important;
    }
    .pop-subtitle {
        font-size: 0.95rem;
        opacity: 0.85;
        margin-bottom: 1.5rem;
        color: #FFFFFF !important;
    }

    /* File uploader border rounding */
    .st-emotion-cache-9j8j93, .st-emotion-cache-1vbkxwb {
        border-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="pop-title">Drop your PoP images</div>'
    '<div class="pop-subtitle">Use the same filenames as the desktop PoP Report Builder. '
    'We’ll read the client, campaign and live date from the first valid file.</div>',
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
            status = "✅ OK"
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
