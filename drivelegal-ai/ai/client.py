import google.generativeai as genai
import streamlit as st
import base64
import time

def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("Gemini API key not found. Add GEMINI_API_KEY to your secrets.")
        st.stop()
    genai.configure(api_key=api_key)

def get_ai_response(prompt: str, system_prompt: str = "", max_retries: int = 3) -> str:
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

def get_ai_response_with_image(prompt: str, image_bytes: bytes, mime_type: str = "image/jpeg", system_prompt: str = "") -> str:
    """For challan image analysis — Gemini supports vision natively."""
    get_client()
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt if system_prompt else None
    )
    image_part = {"mime_type": mime_type, "data": image_bytes}
    try:
        response = model.generate_content([prompt, image_part])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def stream_ai_response(prompt: str, system_prompt: str = ""):
    """Streaming version for chat UI."""
    get_client()
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt if system_prompt else None
    )
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Error: {str(e)}"
