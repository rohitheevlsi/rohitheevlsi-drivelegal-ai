import os
import time
import google.generativeai as genai
import streamlit as st
from laws_data import SYSTEM_PROMPT

# =========================================================
# Model Priority List — tries each in order until one works
# =========================================================
MODEL_PRIORITY = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-pro-latest",
]


# =========================================================
# Configure Gemini Client
# =========================================================

def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
            elif "google" in st.secrets and "GOOGLE_API_KEY" in st.secrets["google"]:
                api_key = st.secrets["google"]["GOOGLE_API_KEY"]
        except Exception:
            pass

    if not api_key:
        st.error(
            "⚠️ Gemini API key not found.\n"
            "Please configure GOOGLE_API_KEY in your Render Environment Variables or .streamlit/secrets.toml."
        )
        st.stop()

    genai.configure(api_key=api_key)


def _build_model(model_name: str, system_prompt: str):
    """Build a GenerativeModel, skipping system_instruction for older models."""
    try:
        return genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt if system_prompt else None,
        )
    except Exception:
        return genai.GenerativeModel(model_name=model_name)


# =========================================================
# Core: try every model until one succeeds
# =========================================================

def get_ai_response(prompt: str, system_prompt: str = "") -> str:
    get_client()
    effective_sp = system_prompt if system_prompt else SYSTEM_PROMPT
    last_error = "Unknown error"

    for model_name in MODEL_PRIORITY:
        try:
            model = _build_model(model_name, effective_sp)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                return response.text
            return str(response)
        except Exception as e:
            last_error = str(e)
            time.sleep(0.5)   # brief pause before trying next model
            continue

    return (
        f"⚠️ All AI models are currently unavailable. "
        f"Last error: {last_error}\n\n"
        f"Please try again in a few minutes or check your API key quota at "
        f"https://aistudio.google.com"
    )


def get_ai_response_with_image(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    system_prompt: str = "",
) -> str:
    get_client()
    effective_sp = system_prompt if system_prompt else SYSTEM_PROMPT
    image_part = {"mime_type": mime_type, "data": image_bytes}
    last_error = "Unknown error"

    for model_name in MODEL_PRIORITY:
        try:
            model = _build_model(model_name, effective_sp)
            response = model.generate_content([prompt, image_part])
            if hasattr(response, "text") and response.text:
                return response.text
            return str(response)
        except Exception as e:
            last_error = str(e)
            time.sleep(0.5)
            continue

    return f"⚠️ Unable to analyse image. Last error: {last_error}"


def stream_ai_response(prompt: str, system_prompt: str = ""):
    get_client()
    effective_sp = system_prompt if system_prompt else SYSTEM_PROMPT
    last_error = "Unknown error"

    for model_name in MODEL_PRIORITY:
        try:
            model = _build_model(model_name, effective_sp)
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text
            return   # success — stop trying other models
        except Exception as e:
            last_error = str(e)
            time.sleep(0.5)
            continue

    yield (
        f"⚠️ All AI models are currently unavailable. "
        f"Last error: {last_error}\n\n"
        f"Please try again in a few minutes."
    )


# =========================================================
# Chat Wrapper
# =========================================================

def chat(messages):
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Challan Validation
# =========================================================

def validate_challan_text(state, violation, fine):
    prompt = f"""
    You are an Indian traffic law expert. Analyze this challan:
    State where issued: {state}
    Violation charged: {violation}
    Fine amount charged: ₹{fine}

    Check if the challan is legally correct and does not exceed the legal bounds.

    STRICT RULES:
    - Start your answer IMMEDIATELY with either "VALID ✅", "OVERCHARGED ❌", or "DISPUTABLE ⚠️"
    - Provide the official legal fine according to the MV Act 2019 / state overrides.
    - Cite the exact Section of the law (e.g., Section 185, Section 129, etc.).
    - Present clear, empowering advice for the citizen on what steps to take.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


def validate_challan_with_image(image_bytes, mime, state, violation, fine):
    prompt = f"""
    Analyze this Indian traffic challan image visually.
    State where issued: {state}
    Violation charged on challan: {violation}
    Fine amount charged: ₹{fine}

    Verify whether the fine is legally correct under the MV Act 2019.
    Start your response immediately with "VALID ✅", "OVERCHARGED ❌", or "DISPUTABLE ⚠️".
    """
    return get_ai_response_with_image(prompt, image_bytes, mime, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Dispute Letter Generator
# =========================================================

def generate_dispute_letter(
    name, address, vehicle, challan_no,
    offence_date, violation, fine_paid, legal_fine, grounds, state
):
    prompt = f"""
    Generate a highly professional, formal, and print-ready dispute letter for a traffic challan.

    Driver Details:
    - Name: {name}
    - Address: {address}
    - Vehicle Number: {vehicle}
    - State of Offence: {state}

    Challan Details:
    - Challan Number: {challan_no}
    - Date of Offence: {offence_date}
    - Violation Alleged: {violation}
    - Fine Charged: ₹{fine_paid}
    - Correct Legal Fine (per MV Act 2019): ₹{legal_fine}

    Dispute Grounds: {grounds}

    Formatting:
    - Formal legal tone, respectful yet firm on legal sections.
    - Print-ready letter with To/From, subject line, body citing MV Act sections, and signature space.
    - Do NOT include markdown code blocks (```).
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Compare States
# =========================================================

def compare_states(state1, state2, violation):
    prompt = f"""
    Compare the traffic rules, fine structures, and penalties between two Indian states.

    Violation: {violation}
    Comparing: {state1} vs {state2}

    Provide:
    - Fine difference (citing exact rates in both states, including multipliers if applicable)
    - Rule differences
    - Key enforcement highlights or unique local rules for both states.

    Use bullet points and a clear side-by-side logical explanation.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Rights Advisor
# =========================================================

def explain_rights(query):
    prompt = f"""
    Explain the legal rights of an Indian citizen in this traffic police checkpoint scenario:

    Situation: {query}

    Address:
    - The relevant citizen rights (e.g., Section 129 CrPC, NALSA free legal aid, right to receipts).
    - What police officers are legally authorized to do.
    - What police officers are strictly PROHIBITED from doing.
    - Practical safety and compliance advice.
    - Concrete, actionable next steps.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# General Legal Query
# =========================================================

def answer_legal_query(query):
    return get_ai_response(query, system_prompt=SYSTEM_PROMPT)
