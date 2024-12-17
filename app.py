import streamlit as st
import warnings
import pdfplumber
from io import BytesIO

warnings.filterwarnings("ignore")

# ======================================
# Original Functions (Unchanged)
# ======================================

def is_scanned_pdf(file) -> bool:
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            try:
                if page.extract_text().strip() == "":
                    return True
            except:
                print("error")
                return True
    return False

# Removed ocrmypdf function and its part

def extract_text_from_pdf_per_page(pdf, x_tolerance, y_tolerance, x_density, y_density):
    pdf = pdfplumber.open(pdf)
    pages_text = []
    for page_num, page in enumerate(pdf.pages, start=1):
        text = page.extract_text(
            x_tolerance=x_tolerance,
            y_tolerance=y_tolerance,
            layout=True,
            x_density=x_density,
            y_density=y_density
        )
        if text:
            pages_text.append((page_num, text))
    return pages_text

def extract_text_from_scanned_pdf_per_page(pdf, x_tolerance, y_tolerance, x_density, y_density):
    # Since we're no longer using OCR, simply return an empty result for scanned PDFs
    # or you can add an alternative method for OCR processing here if desired.
    return []

# ======================================
# Streamlit App
# ======================================

def main():
    st.set_page_config(
        page_title="Text Extraction Service",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply custom CSS
    st.markdown("""<style>
        .page-text-area .stTextArea textarea {
            font-size: 14px;
            height: 400px !important;
            width: 100% !important;
            overflow: auto;
            white-space: pre-wrap;
        }
        .main .block-container{
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .st-expander{
            border: 1px solid #4A90E2;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        </style>""", unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📝 Text Extraction Service</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload your PDF documents to extract text. Adjust settings for optimal results.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar for pdfplumber parameters
    st.sidebar.header("🔧 Extraction Settings")
    x_tolerance = st.sidebar.number_input("x_tolerance", value=2.0, step=0.5)
    y_tolerance = st.sidebar.number_input("y_tolerance", value=4.0, step=0.5)
    x_density = st.sidebar.number_input("x_density", value=5.0, step=0.5)
    y_density = st.sidebar.number_input("y_density", value=10.0, step=0.5)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Adjust these settings if you're not satisfied with the extraction results.")

    # File uploader
    uploaded_files = st.file_uploader(
        "📄 Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown(f"### Processing: {uploaded_file.name}")
            with st.spinner('Extracting text...'):
                # Read file bytes
                pdf_bytes = BytesIO(uploaded_file.read())

                if is_scanned_pdf(pdf_bytes):
                    st.info("🔍 Detected a scanned PDF. OCR not available, skipping...")
                    pages_text = extract_text_from_scanned_pdf_per_page(
                        pdf_bytes,
                        x_tolerance=x_tolerance,
                        y_tolerance=y_tolerance,
                        x_density=x_density,
                        y_density=y_density
                    )
                else:
                    st.info("💡 Extracting text from digital PDF...")
                    pages_text = extract_text_from_pdf_per_page(
                        pdf_bytes,
                        x_tolerance=x_tolerance,
                        y_tolerance=y_tolerance,
                        x_density=x_density,
                        y_density=y_density
                    )

                if pages_text:
                    # Display extracted text per page
                    st.markdown("#### Extracted Text:")
                    for page_num, text in pages_text:
                        with st.expander(f"Page {page_num}", expanded=False):
                            st.markdown("<div class='page-text-area'>", unsafe_allow_html=True)
                            st.text_area(
                                label="",
                                value=text,
                                height=400,
                                key=f"{uploaded_file.name}_page_{page_num}",
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No text could be extracted from this file.")

            st.markdown("---")

    else:
        st.info("💡 Please upload PDF files to start the extraction process.")

if __name__ == "__main__":
    main()
