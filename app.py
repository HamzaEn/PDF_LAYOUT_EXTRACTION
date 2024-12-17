import streamlit as st
import warnings
import pdfplumber
from io import BytesIO

warnings.filterwarnings("ignore")

# ======================================
# Functions
# ======================================

def is_scanned_pdf(file) -> bool:
    """Check if the given PDF file is scanned by trying to extract text from each page."""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            try:
                text = page.extract_text()
                if not text or text.strip() == "":
                    return True
            except:
                return True
    return False

def extract_text_from_page(pdf, page_number, x_tolerance, y_tolerance, x_density, y_density):
    """Extract text from a single page of the PDF with the given extraction parameters."""
    # Open PDF once per extraction for simplicity (cache usage recommended for performance)
    with pdfplumber.open(pdf) as pdf_obj:
        if page_number < 1 or page_number > len(pdf_obj.pages):
            return None
        page = pdf_obj.pages[page_number - 1]
        text = page.extract_text(
            x_tolerance=x_tolerance,
            y_tolerance=y_tolerance,
            layout=True,
            x_density=x_density,
            y_density=y_density
        )
        return text

# ======================================
# Theming
# ======================================
def apply_theme(theme_name):
    """Apply a custom theme based on user selection."""
    if theme_name == "Default":
        st.markdown("<style>body { background-color: #ffffff; }</style>", unsafe_allow_html=True)
    elif theme_name == "Dark":
        st.markdown("""
        <style>
        body { background-color: #1E1E1E; color: #f0f0f0; }
        .sidebar .sidebar-content { background-color: #2C2C2C; }
        </style>""", unsafe_allow_html=True)
    elif theme_name == "Solarized Light":
        st.markdown("""
        <style>
        body { background-color: #FDF6E3; color: #586e75; }
        .sidebar .sidebar-content { background-color: #EEE8D5; }
        </style>""", unsafe_allow_html=True)
    elif theme_name == "Solarized Dark":
        st.markdown("""
        <style>
        body { background-color: #002b36; color: #839496; }
        .sidebar .sidebar-content { background-color: #073642; }
        </style>""", unsafe_allow_html=True)

# ======================================
# Streamlit App
# ======================================

def main():
    st.set_page_config(
        page_title="PDF Text Extraction Service",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar - Global Settings
    st.sidebar.header("🎨 Appearance")
    theme_name = st.sidebar.selectbox(
        "Choose a Theme:",
        ["Default", "Dark", "Solarized Light", "Solarized Dark"],
        help="Select a visual theme for the app."
    )
    apply_theme(theme_name)

    st.sidebar.header("📜 Instructions")
    st.sidebar.markdown("""
    1. Upload a PDF file.
    2. If it's a digital PDF, the text can be extracted directly.
    3. If it's scanned, currently no OCR is applied, so no text will be extracted.
    4. Use the 'Page Controls' below the main area to select a page and adjust parameters.
    5. Adjust parameters and see the extracted text update in real-time.
    """, unsafe_allow_html=True)

    # Main App Interface
    st.markdown(f"<h1 style='text-align: center; margin-bottom:0;'>📝 PDF Text Extraction Service</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:16px;'>Upload your PDF and adjust extraction parameters per page.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # File uploader
    uploaded_files = st.file_uploader(
        "📄 Upload PDF files (only .pdf)",
        type=["pdf"],
        accept_multiple_files=False,
    )

    if uploaded_files:
        # Load PDF bytes
        pdf_bytes = BytesIO(uploaded_files.read())

        # Check if scanned
        scanned = is_scanned_pdf(pdf_bytes)

        if scanned:
            st.warning("🔍 The uploaded PDF appears to be scanned. No text extraction is possible without OCR.")
        else:
            st.success("💡 The uploaded PDF is a digital PDF. You can extract text directly.")

        # Get basic info about PDF
        with pdfplumber.open(pdf_bytes) as pdf_obj:
            total_pages = len(pdf_obj.pages)

        if total_pages == 0:
            st.error("This PDF has no pages or couldn't be read.")
            return

        st.markdown(f"**PDF Loaded:** {uploaded_files.name} | **Total Pages:** {total_pages}")

        # Page Controls
        st.markdown("### Page Controls")
        st.markdown("Use the controls below to select a page and adjust the extraction parameters. Your changes will be reflected immediately.")
        
        page_col, param_col = st.columns([1, 3])
        
        # Select page
        with page_col:
            selected_page = st.number_input(
                "Page Number",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1,
                help="Select which page to extract text from."
            )

        # Extraction parameters per page
        with param_col:
            st.subheader("Extraction Parameters")
            x_tolerance = st.slider("x_tolerance", min_value=0.0, max_value=10.0, value=2.0, step=0.5,
                                    help="Adjust X tolerance for text extraction layout.")
            y_tolerance = st.slider("y_tolerance", min_value=0.0, max_value=10.0, value=4.0, step=0.5,
                                    help="Adjust Y tolerance for text extraction layout.")
            x_density = st.slider("x_density", min_value=1.0, max_value=20.0, value=5.0, step=0.5,
                                  help="Adjust X density for the text layout analysis.")
            y_density = st.slider("y_density", min_value=1.0, max_value=20.0, value=10.0, step=0.5,
                                  help="Adjust Y density for the text layout analysis.")

        # Extract text with current parameters if not scanned
        if not scanned:
            extracted_text = extract_text_from_page(
                pdf=pdf_bytes,
                page_number=selected_page,
                x_tolerance=x_tolerance,
                y_tolerance=y_tolerance,
                x_density=x_density,
                y_density=y_density
            )

            st.markdown("### Extracted Text")
            if extracted_text:
                # Display extracted text in a text area with some styling
                st.markdown("<div class='page-text-area' style='border:1px solid #ccc; border-radius:5px; padding:10px;'>", unsafe_allow_html=True)
                st.text_area(
                    label=f"Page {selected_page} Text:",
                    value=extracted_text,
                    height=300,
                )
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info(f"No text could be extracted from page {selected_page}. Try adjusting the parameters above.")
        else:
            # If scanned, just show a message
            st.info("No text extraction available for scanned PDFs without OCR.")

    else:
        st.info("💡 Please upload a PDF file to start the extraction process.")

if __name__ == "__main__":
    main()
