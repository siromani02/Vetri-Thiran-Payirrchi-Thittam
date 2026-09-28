import html
import os
import re
import sys
from datetime import date
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# ============================================================
# PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
LOGO_PATH = ROOT_DIR / "Image" / "Logo.png"
# ============================================================
# IMPORTS
# ============================================================

from backend.services.document_service import (
    create_docx,
    create_pdf,
    create_txt,
)

# ============================================================
# ENV
# ============================================================

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """<style>
.stApp {
    background: linear-gradient(180deg, #0b0f16 0%, #111722 100%);
    color: #ffffff;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.brand-wrapper {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 28px;
}

.brand-logo {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
    margin-bottom: 4px;
}

.brand-subtitle {
    color: #aeb7c5;
    font-size: 15px;
    letter-spacing: 0.3px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 5px;
}

.section-description {
    color: #9da7b5;
    font-size: 14px;
    margin-bottom: 18px;
}

[data-testid="stForm"] {
    background: #151b25;
    border: 1px solid #303846;
    border-radius: 14px;
    padding: 25px;
}

label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background-color: #202733 !important;
    color: #ffffff !important;
    border: 1px solid #3d4655 !important;
    border-radius: 8px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus {
    border-color: #7c8cff !important;
    box-shadow: 0 0 0 1px #7c8cff !important;
}

input::placeholder,
textarea::placeholder {
    color: #8792a3 !important;
}

.stButton button {
    border-radius: 8px !important;
    font-weight: 700 !important;
    min-height: 46px !important;
}

.stButton button[kind="primary"] {
    background: #6c63ff !important;
    border: none !important;
    color: white !important;
}

.stButton button[kind="primary"]:hover {
    background: #584ff0 !important;
}

.preview-shell {
    background: #202531;
    border: 1px solid #4b5565;
    border-radius: 12px;
    padding: 22px;
    margin-top: 10px;
}

.preview-paper {
    background: #ffffff;
    color: #222222;
    border-radius: 4px;
    padding: 45px 55px;
    min-height: 700px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.30);
}

.preview-brand {
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    color: #111111;
    margin-bottom: 2px;
}

.preview-subtitle {
    text-align: center;
    color: #666666;
    font-size: 11px;
    margin-bottom: 14px;
}

.preview-line {
    height: 1px;
    background: #222222;
    margin-bottom: 25px;
}

.preview-title {
    text-align: center;
    font-size: 21px;
    font-weight: 800;
    color: #111111;
    margin-bottom: 22px;
}

.legal-notice {
    background: #f5f5f5;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 13px 15px;
    font-size: 11px;
    line-height: 1.55;
    color: #333333;
    margin-bottom: 25px;
}

.legal-section-heading {
    font-size: 13px;
    font-weight: 800;
    color: #111111;
    margin-top: 20px;
    margin-bottom: 7px;
}

.legal-body {
    font-size: 11px;
    line-height: 1.7;
    color: #333333;
    margin-bottom: 8px;
}

.signature-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 25px;
}

.signature-box {
    border-top: 1px solid #999999;
    padding-top: 10px;
    font-size: 11px;
    color: #333333;
    line-height: 2;
}

.preview-footer {
    border-top: 1px solid #cccccc;
    margin-top: 35px;
    padding-top: 9px;
    color: #777777;
    font-size: 9px;
    text-align: center;
}

.download-title {
    font-size: 21px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 25px;
    margin-bottom: 12px;
}

.stDownloadButton button {
    background: #202733 !important;
    border: 1px solid #414b5c !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    min-height: 44px !important;
    font-weight: 600 !important;
}

.stDownloadButton button:hover {
    background: #2b3443 !important;
    border-color: #69758a !important;
}

.stTextArea textarea {
    font-family: Arial, sans-serif !important;
    font-size: 14px !important;
    line-height: 1.65 !important;
}

hr {
    border-color: #29313e !important;
}
</style>""",
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="brand-wrapper">',
    unsafe_allow_html=True,
)

if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=180)

st.markdown(
    '<div class="brand-subtitle">AI-Powered Legal Document Generator</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ============================================================
# LEGAL WARNING
# ============================================================

st.warning(
    "LegalEase creates AI-generated drafts for informational purposes only. "
    "Review documents with a qualified legal professional before signing."
)

# ============================================================
# SESSION STATE
# ============================================================

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

if "generated_type" not in st.session_state:
    st.session_state.generated_type = "Legal Document"

# ============================================================
# DOCUMENT INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Create your legal document</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    "Enter the document details below and generate a structured legal document."
    "</div>",
    unsafe_allow_html=True,
)

with st.form("document_form"):
    col1, col2 = st.columns(2)

    with col1:
        document_type = st.text_input(
            "Document type",
            value="Freelance Work Contract",
        )

        parties = st.text_area(
            "Parties involved",
            value=(
                "Jane Doe (Service Provider); "
                "TechNova Inc. (Client)"
            ),
            height=120,
        )

        effective_date = st.date_input(
            "Effective date",
            value=date.today(),
        )

        jurisdiction = st.text_input(
            "Jurisdiction",
            value="Not specified",
        )

    with col2:
        terms = st.text_area(
            "Terms and conditions",
            value=(
                "Work must be delivered within 30 days of the effective date;\n"
                "Payment will be made within 7 days of invoice;\n"
                "The client retains all intellectual property rights;\n"
                "Confidentiality must be maintained at all times."
            ),
            height=185,
        )

        additional_instructions = st.text_area(
            "Additional instructions (optional)",
            value=(
                "Use simple, professional language. "
                "Include clear sections and signature spaces."
            ),
            height=90,
        )

    submitted = st.form_submit_button(
        "Generate document",
        type="primary",
        use_container_width=True,
    )

# ============================================================
# GENERATE DOCUMENT
# ============================================================

if submitted:
    if (
        not document_type.strip()
        or not parties.strip()
        or not terms.strip()
    ):
        st.error(
            "Please complete document type, parties, and terms."
        )
    else:
        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.isoformat(),
            "jurisdiction": jurisdiction.strip() or "Not specified",
            "additional_instructions": additional_instructions.strip(),
        }

        try:
            with st.spinner("Generating your legal document..."):
                response = requests.post(
                    f"{BACKEND_URL}/api/generate",
                    json=payload,
                    timeout=100,
                )

            if response.ok:
                result = response.json()
                generated = result.get("content", "")

                if generated:
                    st.session_state.generated_text = generated
                    st.session_state.generated_type = document_type.strip()

                    st.success("Document generated successfully.")

                    if result.get("demo_mode"):
                        st.info(
                            "Demo mode is active. Gemini was not used for this document."
                        )
                else:
                    st.error("The backend returned an empty document.")
            else:
                st.error(
                    f"Backend error: {response.text}"
                )

        except requests.RequestException as exc:
            st.error("Could not connect to FastAPI backend.")
            st.caption(str(exc))

# ============================================================
# DOCUMENT PREVIEW
# ============================================================

if st.session_state.generated_text:
    st.divider()

    st.markdown(
        '<div class="section-title">📄 Editable document preview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        "You can edit the generated document before downloading it."
        "</div>",
        unsafe_allow_html=True,
    )

    edited_text = st.text_area(
        "Edit the generated document",
        value=st.session_state.generated_text,
        height=520,
        label_visibility="collapsed",
    )

    st.session_state.generated_text = edited_text

    # ========================================================
    # FORMATTED PREVIEW
    # ========================================================

    def build_preview(text):
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        title = st.session_state.generated_type.upper()

        for line in lines[:15]:
            clean_line = line.strip()
            lower = clean_line.lower()

            if (
                "agreement" in lower
                or "contract" in lower
                or "non-disclosure" in lower
                or lower == "nda"
                or "lease" in lower
                or "employment" in lower
            ):
                if len(clean_line) <= 100:
                    title = clean_line.upper()
                    break

        html_parts = [
            '<div class="preview-shell">',
            '<div class="preview-paper">',
            '<div class="preview-brand">⚖ LegalEase</div>',
            '<div class="preview-subtitle">'
            "AI-Powered Legal Document Generator"
            "</div>",
            '<div class="preview-line"></div>',
            '<div class="preview-title">',
            html.escape(title),
            "</div>",
            '<div class="legal-notice">',
            "<b>IMPORTANT LEGAL NOTICE</b><br><br>",
            "This document is an AI-generated draft for "
            "informational purposes only. It is not legal advice. "
            "Consult a qualified legal professional before using "
            "or signing this document.",
            "</div>",
        ]

        title_skipped = False

        for line in lines:
            lower = line.lower().strip()

            if not title_skipped:
                if lower == title.lower():
                    title_skipped = True
                    continue
                title_skipped = True

            if lower in {
                "legalease",
                "⚖ legalease",
                "ai-powered legal document generator",
            }:
                continue

            if lower.startswith("important legal notice"):
                continue

            if "this document is an ai-generated draft" in lower:
                continue

            safe_line = html.escape(line)

            if re.match(r"^\d+\s*[\.\)]\s+", line):
                html_parts.append(
                    '<div class="legal-section-heading">'
                    f"{safe_line}"
                    "</div>"
                )
            elif (
                line.upper() == line
                and len(line) < 100
                and len(re.sub(r"[^A-Za-z]", "", line)) >= 4
            ):
                html_parts.append(
                    '<div class="legal-section-heading">'
                    f"{safe_line}"
                    "</div>"
                )
            else:
                html_parts.append(
                    '<div class="legal-body">'
                    f"{safe_line}"
                    "</div>"
                )

        html_parts.extend(
            [
                '<div class="legal-section-heading">SIGNATURES</div>',
                '<div class="signature-grid">',
                '<div class="signature-box">',
                "<b>PARTY 1</b><br><br>",
                "Signature: ______________________________<br>",
                "Name: ___________________________________<br>",
                "Date: ___________________________________",
                "</div>",
                '<div class="signature-box">',
                "<b>PARTY 2</b><br><br>",
                "Signature: ______________________________<br>",
                "Name: ___________________________________<br>",
                "Date: ___________________________________",
                "</div>",
                "</div>",
                '<div class="preview-footer">',
                "LegalEase | AI-Powered Legal Document Generator",
                "</div>",
                "</div></div>",
            ]
        )

        return "".join(html_parts)

    st.markdown(
        build_preview(edited_text),
        unsafe_allow_html=True,
    )

    # ========================================================
    # DOWNLOADS
    # ========================================================

    st.markdown(
        '<div class="download-title">📥 Download document</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "Download TXT",
            data=create_txt(edited_text),
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Download DOCX",
            data=create_docx(
                edited_text,
                st.session_state.generated_type,
            ),
            file_name="legalease_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

    with col3:
        st.download_button(
            "Download PDF",
            data=create_pdf(edited_text),
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
