# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | AI Client Module
# Centralised Anthropic API calls with error handling & retry logic
# ─────────────────────────────────────────────────────────────────────────────
import anthropic
import base64
import time
import streamlit as st
from laws_data import SYSTEM_PROMPT

MODEL = "claude-opus-4-5"
MAX_TOKENS = 1500


def _get_client() -> anthropic.Anthropic:
    """Return authenticated Anthropic client using API key from st.secrets or env."""
    import os
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set. Add it to .streamlit/secrets.toml or environment variables.")
    return anthropic.Anthropic(api_key=api_key)


def _call_api(messages: list, system: str = SYSTEM_PROMPT, max_retries: int = 3) -> str:
    """Core API call with exponential back-off retry."""
    client = _get_client()
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=messages,
            )
            return response.content[0].text
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except anthropic.APIStatusError as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"API error after {max_retries} attempts: {e.message}") from e
            time.sleep(2 ** attempt)
        except Exception as e:
            raise RuntimeError(f"Unexpected error calling Claude API: {e}") from e
    raise RuntimeError("Max retries exceeded.")


# ── Public helpers ─────────────────────────────────────────────────────────

def chat(conversation_history: list) -> str:
    """Send a multi-turn conversation and return the assistant reply."""
    try:
        return _call_api(conversation_history)
    except Exception as e:
        return f"⚠️ Sorry, I couldn't reach the AI right now. Error: {e}"


def validate_challan_with_image(image_bytes: bytes, mime_type: str, state: str, violation: str, fine_amount: int) -> str:
    """Validate a traffic challan using an uploaded image."""
    try:
        b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": mime_type, "data": b64},
                    },
                    {
                        "type": "text",
                        "text": (
                            f"Validate this traffic challan image.\n"
                            f"State: {state}\nViolation claimed: {violation}\n"
                            f"Fine amount on challan: ₹{fine_amount}\n\n"
                            "1. Confirm the violation and fine match MV Act 2019 for this state.\n"
                            "2. Start with VALID ✅ / OVERCHARGED ❌ / DISPUTABLE ⚠️\n"
                            "3. State the correct legal fine range.\n"
                            "4. List any grounds for dispute if applicable.\n"
                            "5. Provide next steps."
                        ),
                    },
                ],
            }
        ]
        return _call_api(messages)
    except Exception as e:
        return f"⚠️ Could not analyse the challan image. Error: {e}"


def validate_challan_text(state: str, violation: str, fine_amount: int) -> str:
    """Validate a challan by text description (no image)."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Validate this traffic challan.\n"
                    f"State: {state}\nViolation: {violation}\nFine claimed: ₹{fine_amount}\n\n"
                    "1. Is this fine amount correct under MV Act 2019 for this state?\n"
                    "2. Start with VALID ✅ / OVERCHARGED ❌ / DISPUTABLE ⚠️\n"
                    "3. State the correct legal fine.\n"
                    "4. Provide grounds for dispute if applicable and next steps."
                ),
            }
        ]
        return _call_api(messages)
    except Exception as e:
        return f"⚠️ Could not validate the challan. Error: {e}"


def generate_dispute_letter(name: str, address: str, vehicle_no: str, challan_no: str,
                            date: str, violation: str, fine_claimed: int,
                            legal_fine: int, grounds: str, state: str) -> str:
    """Generate a formal, print-ready dispute letter."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Generate a formal dispute letter for an Indian traffic challan.\n\n"
                    f"Driver: {name}\nAddress: {address}\nVehicle No: {vehicle_no}\n"
                    f"Challan No: {challan_no}\nDate of Offence: {date}\n"
                    f"Violation Alleged: {violation}\nFine Charged: ₹{fine_claimed}\n"
                    f"Correct Legal Fine: ₹{legal_fine}\nState: {state}\n"
                    f"Grounds for Dispute: {grounds}\n\n"
                    "Write a complete, professional, print-ready letter to the Traffic Police Inspector. "
                    "Include: proper salutation, all facts, legal sections, constitutional rights invoked, "
                    "specific relief requested, and a professional closing. "
                    "Format clearly with paragraphs. Add [YOUR SIGNATURE] placeholder at the end."
                ),
            }
        ]
        return _call_api(messages, max_retries=2)
    except Exception as e:
        return f"⚠️ Could not generate the dispute letter. Error: {e}"


def answer_legal_query(question: str, language: str = "English") -> str:
    """Answer a general traffic law question, optionally in a regional language."""
    try:
        lang_note = f" Respond entirely in {language}." if language != "English" else ""
        messages = [{"role": "user", "content": question + lang_note}]
        return _call_api(messages)
    except Exception as e:
        return f"⚠️ Could not answer your question. Error: {e}"


def compare_states(state1: str, state2: str, violation: str) -> str:
    """Compare a violation's fine/rules across two states."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"Compare the traffic rules and fines for '{violation}' between "
                    f"{state1} and {state2}.\n"
                    "Include: exact fine amounts, legal sections, unique state rules, "
                    "enforcement intensity, and which state is stricter. "
                    "Present in a clear table-like format."
                ),
            }
        ]
        return _call_api(messages)
    except Exception as e:
        return f"⚠️ Could not compare states. Error: {e}"


def explain_rights(scenario: str) -> str:
    """Explain a driver's rights in a given scenario."""
    try:
        messages = [
            {
                "role": "user",
                "content": (
                    f"A driver is in this situation: {scenario}\n\n"
                    "Explain clearly:\n"
                    "1. Their legal rights under the Constitution and MV Act\n"
                    "2. What the officer CAN legally do\n"
                    "3. What the officer CANNOT do\n"
                    "4. Exact steps the driver should take\n"
                    "5. Emergency contacts if needed"
                ),
            }
        ]
        return _call_api(messages)
    except Exception as e:
        return f"⚠️ Could not explain rights. Error: {e}"
