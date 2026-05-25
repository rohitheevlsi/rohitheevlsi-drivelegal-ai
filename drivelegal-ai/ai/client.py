import google.generativeai as genai
import streamlit as st
import time

# =========================================================
# Configure Gemini Client
# =========================================================

def get_client():
    api_key = (
        st.secrets.get("GEMINI_API_KEY")
        or st.secrets.get("GOOGLE_API_KEY")
    )

    if not api_key:
        st.error(
            "Gemini API key not found. "
            "Add GEMINI_API_KEY to Streamlit secrets."
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

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt if system_prompt else None
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return f"Error: {str(e)}"


# =========================================================
# Image Analysis
# =========================================================

def get_ai_response_with_image(
    prompt: str,
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    system_prompt: str = ""
) -> str:

    get_client()

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt if system_prompt else None
    )

    image_part = {
        "mime_type": mime_type,
        "data": image_bytes
    }

    try:
        response = model.generate_content(
            [prompt, image_part]
        )

        return response.text

    except Exception as e:
        return f"Error analyzing image: {str(e)}"


# =========================================================
# Streaming AI Response
# =========================================================

def stream_ai_response(
    prompt: str,
    system_prompt: str = ""
):

    get_client()

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt if system_prompt else None
    )

    try:
        response = model.generate_content(
            prompt,
            stream=True
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Error: {str(e)}"


# =========================================================
# Wrapper Functions For App Compatibility
# =========================================================

def chat(messages):

    prompt = "\n".join(
        [f"{m['role']}: {m['content']}" for m in messages]
    )

    return get_ai_response(
        prompt,
        system_prompt=(
            "You are DriveLegal AI, "
            "an expert in Indian traffic laws."
        )
    )


def validate_challan_text(
    state,
    violation,
    fine
):

    prompt = f"""
    State: {state}

    Violation: {violation}

    Fine Issued: ₹{fine}

    Check whether this challan is legally valid
    under Indian Motor Vehicle Act 2019.

    Mention:
    - correct legal fine
    - whether overcharged
    - citizen rights
    """

    return get_ai_response(prompt)


def validate_challan_with_image(
    image_bytes,
    mime,
    state,
    violation,
    fine
):

    prompt = f"""
    Analyze this traffic challan image.

    State: {state}

    Violation: {violation}

    Fine Issued: ₹{fine}

    Verify whether this challan appears legally correct.

    Mention:
    - correct legal fine
    - whether overcharged
    - suspicious details if any
    """

    return get_ai_response_with_image(
        prompt,
        image_bytes,
        mime
    )


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
    Write a professional legal dispute letter.

    Name: {name}

    Address: {address}

    Vehicle Number: {vehicle}

    Challan Number: {challan_no}

    Offence Date: {offence_date}

    Violation: {violation}

    Fine Charged: ₹{fine_paid}

    Correct Legal Fine: ₹{legal_fine}

    Grounds:
    {grounds}

    State: {state}

    Make the letter:
    - formal
    - respectful
    - legally strong
    - ready to print
    """

    return get_ai_response(prompt)


def compare_states(
    state1,
    state2,
    violation
):

    prompt = f"""
    Compare traffic laws and fines for:

    Violation: {violation}

    State 1: {state1}

    State 2: {state2}

    Explain differences clearly.
    """

    return get_ai_response(prompt)


def explain_rights(query):

    prompt = f"""
    Explain the legal rights of an Indian citizen
    in this traffic police situation:

    {query}

    Mention:
    - citizen rights
    - police limits
    - legal procedure
    - safety advice
    """

    return get_ai_response(prompt)


def answer_legal_query(query):

    return get_ai_response(
        query,
        system_prompt=(
            "You are an Indian traffic law expert."
        )
    )
