
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

LANGUAGE_INSTRUCTIONS = {
    "English": "Answer in simple, clear English.",
    "Tamil": "எளிய, தெளிவான தமிழில் பதிலளிக்கவும். தேவையான legal terms-ஐ English-ல் குறிப்பிடவும்.",
    "Tanglish": "Answer in simple Tanglish using Tamil words written in English letters."
}


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def ask_gemini(prompt):
    client = get_client()

    if client is None:
        return "GEMINI_API_KEY is missing. Check your .env file."

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text or "No answer returned."

        except Exception as e:
            error = str(e).upper()

            if any(code in error for code in [
                "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"
            ]):
                if attempt == 0:
                    time.sleep(2)
                    continue
                return "AI is busy or API quota is exceeded. Try again later."

            return f"AI request failed: {e}"

    return "AI service is temporarily unavailable."


def analyze_legal_document(text, language="English"):
    output_language = LANGUAGE_INSTRUCTIONS.get(
        language, LANGUAGE_INSTRUCTIONS["English"]
    )

    prompt = f"""
You are an Indian legal document analysis assistant.

Respond in this language: {output_language}

Analyze the complete supplied document. Use these headings:
1. Document Type and Purpose
2. All Named People and Their Roles
3. Ownership Claims and Previous Owners
4. Buyers, Sellers and Transferors
5. Legal Heirs and Relationships Explicitly Stated
6. Survey Numbers and Land Details
7. Registration Details, Dates and Amounts
8. Conditions, Restrictions and Missing Information

Rules:
- Preserve every readable name, date, amount and survey number.
- Include every named person and their documented role.
- Do not invent names, relationships or facts.
- Mention unclear or missing information.
- Do not assume a person is an owner or legal heir merely because their name appears.
- Do not claim that ownership or legal validity has been verified.
- This is informational assistance, not legal advice.

DOCUMENT:
{text}
"""
    return ask_gemini(prompt)


def simplify_legal_document(document_text, language="English"):
    output_language = LANGUAGE_INSTRUCTIONS.get(
        language, LANGUAGE_INSTRUCTIONS["English"]
    )

    prompt = f"""
Explain this Indian legal document in simple language.
Respond in: {output_language}

Explain:
- Document type and purpose
- All named people and documented roles
- Ownership claims stated in the document
- Survey numbers and land extent
- Dates, amounts and registration details
- Important conditions and legal terms
- Missing or unclear information

Preserve all names, dates, amounts and survey numbers.
Do not invent facts or assume legal ownership.
This is informational assistance, not legal advice.

DOCUMENT:
{document_text}
"""
    return ask_gemini(prompt)


def ask_document_question(document_text, question, language="English"):
    output_language = LANGUAGE_INSTRUCTIONS.get(
        language, LANGUAGE_INSTRUCTIONS["English"]
    )

    prompt = f"""
You are an Indian legal document assistant.
Respond in: {output_language}

Answer the question using only the supplied document.
Give a direct answer and identify the relevant documented names,
roles, dates or survey numbers.
Do not invent facts or assume ownership.
If the answer is absent, say it is not mentioned.
This is informational assistance, not legal advice.

DOCUMENT:
{document_text}

QUESTION:
{question}
"""
    return ask_gemini(prompt)
