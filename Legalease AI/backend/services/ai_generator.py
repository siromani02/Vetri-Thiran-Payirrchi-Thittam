import os
import requests
from dotenv import load_dotenv

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.0-flash"
        )

        self.demo_mode = not bool(self.api_key)

    # ============================================================
    # MAIN GENERATION
    # ============================================================

    def generate(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        jurisdiction,
        additional_instructions=""
    ):

        # Gemini API key irundha actual AI generation
        if self.api_key:
            try:
                return self._generate_with_gemini(
                    document_type=document_type,
                    parties=parties,
                    terms=terms,
                    effective_date=effective_date,
                    jurisdiction=jurisdiction,
                    additional_instructions=additional_instructions,
                )

            except Exception as e:
                print("====================================")
                print("GEMINI API ERROR:")
                print(e)
                print("====================================")

                self.demo_mode = True

        # Gemini fail aana reference-style fallback document
        self.demo_mode = True

        return self._generate_demo(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
            jurisdiction=jurisdiction,
            additional_instructions=additional_instructions,
        )

    # ============================================================
    # GEMINI GENERATION
    # ============================================================

    def _generate_with_gemini(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        jurisdiction,
        additional_instructions
    ):

        prompt = f"""
You are LegalEase, an AI-powered legal document drafting
assistant.

Your task is to generate a professional legal agreement based
on the user's information.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

JURISDICTION:
{jurisdiction}

TERMS AND CONDITIONS:
{terms}

ADDITIONAL INSTRUCTIONS:
{additional_instructions}

============================================================
REFERENCE DOCUMENT STYLE
============================================================

The generated document must follow the structure and style of
a professional Freelance Work Contract.

For a Freelance Work Contract, use this organization:

1. Document title
2. Agreement date
3. BETWEEN
4. Party 1 / Service Provider
5. AND
6. Party 2 / Client
7. WITNESSETH
8. WHEREAS introductory paragraph
9. NOW, THEREFORE introductory paragraph
10. Numbered legal sections
11. IN WITNESS WHEREOF
12. Signature information

============================================================
REQUIRED FREELANCE CONTRACT SECTIONS
============================================================

When the document type is Freelance Work Contract, use these
sections in this order:

1. Services
2. Term and Termination
3. Payment
4. Intellectual Property Rights
5. Confidentiality
6. Independent Contractor Status
7. Governing Law
8. Entire Agreement
9. Severability

Each section must contain a useful, professional paragraph
based on the information supplied by the user.

============================================================
DOCUMENT OPENING
============================================================

Start the document with ONLY the document title.

Then write an agreement date such as:

Agreement made this [date].

Then:

Between:

[Service Provider information]

And:

[Client information]

Then:

WITNESSETH:

WHEREAS, the Service Provider is willing to perform such
services for the Client on the terms and conditions set forth
in this Agreement;

NOW, THEREFORE, in consideration of the mutual covenants and
promises contained herein, the parties agree as follows:

============================================================
CONTENT RULES
============================================================

- Use formal professional contract language.
- Use numbered sections.
- Use section headings followed by detailed paragraphs.
- Preserve every important term supplied by the user.
- Do not remove user-provided requirements.
- Do not create fake names, addresses, phone numbers, emails,
  prices, dates, or other personal information.
- If information is missing, use placeholders such as:
  [Service Provider Address]
  [Client Address]
  [Amount]
  [Number of Days]
  [State]
  [Authorized Representative Name]
  [Authorized Representative Title]
- Use the supplied effective date.
- Use the supplied jurisdiction for the Governing Law section.
- Do not add unrelated sections unless they are necessary for
  the document type.
- Do not add explanations about how the document was generated.
- Do not add an AI disclaimer inside the legal document.
- Do not add Markdown headings such as # or ##.
- Do not use Markdown bold markers such as **.
- Do not use bullet points unless they are genuinely required
  by the supplied terms.
- Keep the document readable and suitable for DOCX/PDF export.

============================================================
SIGNATURE SECTION
============================================================

At the end, include:

IN WITNESS WHEREOF, the parties have executed this Agreement
as of the Effective Date.

Then provide signature information for both parties.

Use a structure similar to:

[Service Provider Name]

____________________________
Authorized Representative Signature

[Authorized Representative Title]

[Client Name]

____________________________
Authorized Representative Signature

[Authorized Representative Title]

Do not invent actual signature names if they were not provided.

============================================================
IMPORTANT
============================================================

Return ONLY the legal document.

Do not write:
"Here is your document"
"Sure"
"Below is the agreement"
or any explanation before or after the document.

The result should read like a real professional legal agreement
and should visually work well when converted into a DOCX or PDF.
"""

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/"
            f"{self.model}:generateContent"
        )

        response = requests.post(
            url,
            params={
                "key": self.api_key
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            },
            timeout=90,
        )

        response.raise_for_status()

        data = response.json()

        candidates = data.get(
            "candidates",
            []
        )

        if not candidates:
            raise RuntimeError(
                "Gemini returned no candidates."
            )

        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
        )

        result = "\n".join(
            part.get("text", "")
            for part in parts
            if part.get("text")
        ).strip()

        if not result:
            raise RuntimeError(
                "Gemini returned empty content."
            )

        # Remove accidental Markdown formatting
        result = result.replace("**", "")
        result = result.replace("### ", "")
        result = result.replace("## ", "")
        result = result.replace("# ", "")

        self.demo_mode = False

        return result

    # ============================================================
    # DEMO / FALLBACK DOCUMENT
    # ============================================================

    def _generate_demo(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        jurisdiction,
        additional_instructions
    ):

        # --------------------------------------------------------
        # Split parties
        # --------------------------------------------------------

        party_items = []

        for item in parties.replace(
            ";",
            "\n"
        ).splitlines():

            item = item.strip()

            if item:
                party_items.append(item)

        if len(party_items) >= 2:
            service_provider = party_items[0]
            client = party_items[1]

        elif len(party_items) == 1:
            service_provider = party_items[0]
            client = "[Client Name]"

        else:
            service_provider = "[Service Provider Name]"
            client = "[Client Name]"

        # --------------------------------------------------------
        # Terms
        # --------------------------------------------------------

        term_items = []

        for item in terms.replace(
            ";",
            "\n"
        ).splitlines():

            item = item.strip()

            if item:
                term_items.append(item)

        if not term_items:
            term_items = [
                "The parties agree to perform their respective "
                "obligations under this Agreement."
            ]

        # --------------------------------------------------------
        # Main reference-style document
        # --------------------------------------------------------

        return f"""
{document_type}

Agreement made this {effective_date}.


Between:

{service_provider}


And:

{client}


WITNESSETH:

WHEREAS, the Service Provider is willing to perform such
services for the Client on the terms and conditions set forth
in this Agreement;

NOW, THEREFORE, in consideration of the mutual covenants and
promises contained herein, the parties agree as follows:


1. Services:

The Service Provider agrees to provide the services described
by the parties in connection with this Agreement.

The specific services, deliverables, responsibilities, and
requirements shall be based on the terms provided by the
parties.


2. Term and Termination:

This Agreement shall commence on the Effective Date and shall
terminate upon the completion of the Services as defined in
this Agreement, or upon the occurrence of any of the following
events:

a) Mutual written agreement of the parties;

b) Breach of this Agreement by either party, provided that the
non-breaching party provides written notice of the breach and
allows the breaching party the applicable period to cure the
breach;

c) Upon [Number] days written notice by either party for any
reason.


3. Payment:

The Client agrees to pay the Service Provider according to the
payment terms agreed by the parties.

The amount, payment schedule, invoice requirements, and other
payment conditions shall be as specified in the terms supplied
for this Agreement.


4. Intellectual Property Rights:

All intellectual property rights, including but not limited to
copyrights, patents, trade secrets, trademarks, and other work
product created in connection with the Services, shall be
allocated according to the agreement between the parties.

Unless otherwise specified, the parties should clearly document
ownership and permitted use of the work product.


5. Confidentiality:

The Service Provider acknowledges that during the performance
of the Services, confidential information may be received from
the Client.

Each party agrees to maintain the confidentiality of information
that is identified as confidential or would reasonably be
understood to be confidential.


6. Independent Contractor Status:

The Service Provider is an independent contractor and is not an
employee of the Client.

The Service Provider shall be solely responsible for the payment
of all taxes and other contributions arising from the performance
of the Services.


7. Governing Law:

This Agreement shall be governed by and construed in accordance
with the laws of the State of {jurisdiction}.


8. Entire Agreement:

This Agreement constitutes the entire understanding and
agreement of the parties with respect to the subject matter
hereof and supersedes all prior or contemporaneous
communications, representations, agreements, whether oral or
written.


9. Severability:

If any provision of this Agreement is held to be invalid or
unenforceable, the remaining provisions shall remain in full
force and effect.


TERMS PROVIDED BY THE PARTIES:

{chr(10).join(
    f"- {item}"
    for item in term_items
)}


IN WITNESS WHEREOF, the parties have executed this Agreement
as of the Effective Date.


{service_provider}

____________________________
Authorized Representative Signature

[Authorized Representative Title]


{client}

____________________________
Authorized Representative Signature

[Authorized Representative Title]
"""