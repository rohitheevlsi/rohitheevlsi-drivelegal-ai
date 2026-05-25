import os
import time
import google.generativeai as genai
import streamlit as st

# =========================================================
# Configure Gemini Client
# =========================================================

def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "Gemini API key not found.\n"
            "Add GEMINI_API_KEY in Render Environment Variables."
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

            if hasattr(response, "text"):
                return response.text

            return str(response)

        except Exception as e:

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

            else:
                return f"Error: {str(e)}"


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

        if hasattr(response, "text"):
            return response.text

        return str(response)

    except Exception as e:
        return f"Error analyzing image: {str(e)}"


# =========================================================
# Streaming Response
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

            if hasattr(chunk, "text") and chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Error: {str(e)}"


# =========================================================
# Chat Wrapper
# =========================================================

def chat(messages):

    prompt = "\n".join(
        [f"{m['role']}: {m['content']}" for m in messages]
    )

    return get_ai_response(
        prompt,
        system_prompt=(
            "You are DriveLegal AI, "
            "an expert in Indian traffic laws, "
            "Motor Vehicle Act 2019, "
            "challans, citizen rights, "
            "fines, road safety, and traffic procedures."
        )
    )


# =========================================================
# Challan Validation
# =========================================================

def validate_challan_text(
    state,
    violation,
    fine
):

    prompt = f"""
    You are an Indian traffic law expert.

    State: {state}

    Violation: {violation}

    Fine Issued: ₹{fine}

    Check if the challan is legally correct.

    Mention:
    - legal fine
    - whether overcharged
    - section of law
    - citizen advice

    Use simple language.
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
    Analyze this Indian traffic challan image.

    State: {state}

    Violation: {violation}

    Fine Issued: ₹{fine}

    Verify whether:
    - challan looks genuine
    - fine amount is legal
    - any suspicious issue exists

    Give clear legal explanation.
    """

    return get_ai_response_with_image(
        prompt,
        image_bytes,
        mime
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
    Write a professional dispute letter.

    Name: {name}

    Address: {address}

    Vehicle Number: {vehicle}

    Challan Number: {challan_no}

    Date of Offence: {offence_date}

    Violation: {violation}

    Fine Paid: ₹{fine_paid}

    Correct Legal Fine: ₹{legal_fine}

    Grounds for Dispute:
    {grounds}

    State: {state}

    Requirements:
    - formal legal tone
    - respectful
    - print-ready
    - professional formatting
    """

    return get_ai_response(prompt)


# =========================================================
# Compare States
# =========================================================

def compare_states(
    state1,
    state2,
    violation
):

    prompt = f"""
    Compare traffic rules and penalties.

    Violation:
    {violation}

    Compare:
    {state1}
    vs
    {state2}

    Mention:
    - fine difference
    - rule difference
    - enforcement difference
    """

    return get_ai_response(prompt)


# =========================================================
# Rights Advisor
# =========================================================

def explain_rights(query):

    prompt = f"""
    Explain the legal rights of an Indian citizen
    in this traffic police situation:

    {query}

    Mention:
    - legal rights
    - what police can do
    - what police cannot do
    - safety advice
    - practical next steps

    Keep it simple.
    """

    return get_ai_response(prompt)


# =========================================================
# General Legal Query
# =========================================================

def answer_legal_query(query):

    return get_ai_response(
        query,
        system_prompt=(
            "You are an expert in Indian traffic laws."
        )
    )
