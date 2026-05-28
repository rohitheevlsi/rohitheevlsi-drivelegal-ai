import os
import time
import google.generativeai as genai
import streamlit as st
from laws_data import SYSTEM_PROMPT

# =========================================================
# Configure Gemini Client
# =========================================================

def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            pass

    if not api_key:
        st.error(
            "Gemini API key not found.\n"
            "Please configure GOOGLE_API_KEY in Streamlit Secrets (.streamlit/secrets.toml) or as an Environment Variable."
        )
        st.stop()

    genai.configure(api_key=api_key)


# =========================================================
# Basic AI Response
# =========================================================

def get_ai_response(
    prompt: str,
    system_prompt: str = "",
    max_retries: int = 3
) -> str:
    get_client()

    effective_system_prompt = system_prompt if system_prompt else SYSTEM_PROMPT

    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=effective_system_prompt if effective_system_prompt else None
            )
            response = model.generate_content(prompt)
            if hasattr(response, "text"):
                return response.text
            return str(response)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                # Fallback to gemini-1.5-flash
                try:
                    fallback_model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=effective_system_prompt if effective_system_prompt else None
                    )
                    response = fallback_model.generate_content(prompt)
                    if hasattr(response, "text"):
                        return response.text
                    return str(response)
                except Exception as fe:
                    return f"Error: {str(e)} (Fallback error: {str(fe)})"


# =========================================================
# Image AI Response
# =========================================================

def get_ai_response_with_image(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    system_prompt: str = ""
) -> str:
    get_client()

    effective_system_prompt = system_prompt if system_prompt else SYSTEM_PROMPT

    image_part = {
        "mime_type": mime_type,
        "data": image_bytes
    }

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=effective_system_prompt if effective_system_prompt else None
        )
        response = model.generate_content(
            [prompt, image_part]
        )
        if hasattr(response, "text"):
            return response.text
        return str(response)
    except Exception as e:
        # Fallback to gemini-1.5-flash
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=effective_system_prompt if effective_system_prompt else None
            )
            response = model.generate_content(
                [prompt, image_part]
            )
            if hasattr(response, "text"):
                return response.text
            return str(response)
        except Exception as fe:
            return f"Error analyzing image: {str(e)} (Fallback error: {str(fe)})"


# =========================================================
# Streaming Response
# =========================================================

def stream_ai_response(
    prompt: str,
    system_prompt: str = ""
):
    get_client()

    effective_system_prompt = system_prompt if system_prompt else SYSTEM_PROMPT

    # Try 2.0-flash first
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=effective_system_prompt if effective_system_prompt else None
        )
        response = model.generate_content(
            prompt,
            stream=True
        )
        for chunk in response:
            if hasattr(chunk, "text") and chunk.text:
                yield chunk.text
    except Exception as e:
        # Fallback to gemini-1.5-flash on failure (like 429 quota exceeded)
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=effective_system_prompt if effective_system_prompt else None
            )
            response = model.generate_content(
                prompt,
                stream=True
            )
            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text
        except Exception as fe:
            yield f"Error: {str(e)} (Fallback error: {str(fe)})"



# =========================================================
# Chat Wrapper
# =========================================================

def chat(messages):
    prompt = "\n".join(
        [f"{m['role']}: {m['content']}" for m in messages]
    )
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Challan Validation
# =========================================================

def validate_challan_text(
    state,
    violation,
    fine
):
    prompt = f"""
    You are an Indian traffic law expert. Analyze this textual challenge:
    State where issued: {state}
    Violation charged: {violation}
    Fine amount charged: ₹{fine}

    Check if the challan is legally correct and does not exceed the legal bounds.
    
    Make sure to follow these strict return rules:
    - Start your answer immediately with either "VALID ✅", "OVERCHARGED ❌", or "DISPUTABLE ⚠️"
    - Provide the official legal fine according to the MV Act 2019 / state overrides in the database.
    - Cite the exact Section of the law (e.g., Section 185, Section 129, etc.).
    - Present clear, empowering advice for the citizen on what steps they should take.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


def validate_challan_with_image(
    image_bytes,
    mime,
    state,
    violation,
    fine
):
    prompt = f"""
    Analyze this Indian traffic challan image visually.
    State where issued: {state}
    Violation charged on challan: {violation}
    Fine amount charged: ₹{fine}

    Verify whether:
    - The challan image appears genuine and lists the correct details.
    - The fine amount is legally correct under the MV Act 2019 / state overrides in the database.
    - Any discrepancies or suspicious issues exist.

    Provide a clear, respectful, and empowering legal explanation. 
    Start your response immediately with either "VALID ✅", "OVERCHARGED ❌", or "DISPUTABLE ⚠️" based on the fine amount and legal details matching.
    """
    return get_ai_response_with_image(
        prompt,
        image_bytes,
        mime,
        system_prompt=SYSTEM_PROMPT
    )


# =========================================================
# Dispute Letter Generator
# =========================================================

def generate_dispute_letter(
    name,
    address,
    vehicle,
    challan_no,
    offence_date,
    violation,
    fine_paid,
    legal_fine,
    grounds,
    state
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

    Dispute Details:
    - Grounds for Dispute: {grounds}

    Formatting and Tone:
    - Formal legal tone, highly respectful yet firm on legal sections.
    - Output must be a print-ready letter format with To/From placeholders, subject line, body paragraphs citing appropriate Motor Vehicle Act sections, and signature space.
    - Do not include markdown code block syntax (like ```) in the letter text itself; make it directly copyable.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Compare States
# =========================================================

def compare_states(
    state1,
    state2,
    violation
):
    prompt = f"""
    Compare the traffic rules, fine structures, and penalties between two Indian states.

    Violation: {violation}
    Comparing: {state1} vs {state2}

    Provide:
    - Fine difference (citing exact rates in both states, including multipliers if applicable)
    - Rule difference
    - Key enforcement highlights or unique local rules for both states.
    
    Render the comparison clearly using bullet points and a side-by-side logical explanation.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# Rights Advisor
# =========================================================

def explain_rights(query):
    prompt = f"""
    Explain the legal rights of an Indian citizen in this specific traffic police checkpoint or highway scenario:

    Situation: {query}

    Address:
    - The relevant citizen rights (e.g., Section 129 CrPC, NALSA free legal aid, right to receipts).
    - What police officers are legally authorized to do.
    - What police officers are strictly prohibited from doing (e.g., taking car keys without FIR, demanding spot cash without e-challan).
    - Practical safety and compliance advice.
    - Concrete, actionable next steps.
    """
    return get_ai_response(prompt, system_prompt=SYSTEM_PROMPT)


# =========================================================
# General Legal Query
# =========================================================

def answer_legal_query(query):
    return get_ai_response(query, system_prompt=SYSTEM_PROMPT)
