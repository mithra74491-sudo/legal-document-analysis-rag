
import streamlit as st
from src.document_processor import extract_text
from src.legal_analyzer import (
    analyze_legal_document,
    simplify_legal_document,
    ask_document_question
)

st.set_page_config(
    page_title="Legal Document Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ AI-Powered Legal Document Assistant")
st.write("Upload a legal document to analyze, simplify or ask questions.")

language = st.selectbox(
    "Choose Response Language",
    ["English", "Tamil", "Tanglish"]
)

uploaded_file = st.file_uploader(
    "Upload Legal Document",
    type=["pdf", "txt"]
)

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "document_name" not in st.session_state:
    st.session_state.document_name = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "simplified_result" not in st.session_state:
    st.session_state.simplified_result = None

if "question_result" not in st.session_state:
    st.session_state.question_result = None

if uploaded_file is not None:
    if st.session_state.document_name != uploaded_file.name:
        with st.spinner("Reading document..."):
            try:
                text = extract_text(uploaded_file)

                if not text or not text.strip():
                    st.error("No readable text found in the document.")
                else:
                    st.session_state.document_text = text
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.analysis_result = None
                    st.session_state.simplified_result = None
                    st.session_state.question_result = None

            except Exception as e:
                st.error(f"Document reading failed: {e}")

if st.session_state.document_text:
    st.success(f"Document loaded: {st.session_state.document_name}")
    st.write(
        f"Extracted characters: {len(st.session_state.document_text)}"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Analyze Document", use_container_width=True):
            with st.spinner("Analyzing legal document..."):
                st.session_state.analysis_result = (
                    analyze_legal_document(
                        st.session_state.document_text,
                        language
                    )
                )

    with col2:
        if st.button("Simplify Document", use_container_width=True):
            with st.spinner("Simplifying legal document..."):
                st.session_state.simplified_result = (
                    simplify_legal_document(
                        st.session_state.document_text,
                        language
                    )
                )

    if st.session_state.analysis_result is not None:
        st.subheader("Document Analysis")
        st.markdown(st.session_state.analysis_result)

    if st.session_state.simplified_result is not None:
        st.subheader("Simplified Document")
        st.markdown(st.session_state.simplified_result)

    st.divider()
    st.subheader("Ask a Question")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: Who is mentioned as the buyer?"
    )

    if st.button("Get Answer", use_container_width=True):
        if question.strip():
            with st.spinner("Finding the answer..."):
                st.session_state.question_result = (
                    ask_document_question(
                        st.session_state.document_text,
                        question,
                        language
                    )
                )
        else:
            st.warning("Please enter a question.")

    if st.session_state.question_result is not None:
        st.markdown("### Answer")
        st.markdown(st.session_state.question_result)

else:
    st.info("Please upload a PDF or TXT legal document to begin.")

st.caption(
    "This tool provides informational assistance only. "
    "Verify legal matters with a qualified legal professional."
)
