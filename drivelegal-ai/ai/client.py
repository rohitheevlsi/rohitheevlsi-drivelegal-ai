# =========================
# Wrapper Functions
# =========================

def chat(messages):
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    return get_ai_response(
        prompt,
        system_prompt="You are DriveLegal AI, an expert in Indian traffic laws."
    )


def validate_challan_text(state, violation, fine):
    prompt = f"""
    State: {state}
    Violation: {violation}
    Fine Issued: ₹{fine}

    Check whether this challan is legally valid under Indian Motor Vehicle Act 2019.
    """
    return get_ai_response(prompt)


def validate_challan_with_image(image_bytes, mime, state, violation, fine):
    prompt = f"""
    Analyze this traffic challan image.

    State: {state}
    Violation: {violation}
    Fine: ₹{fine}

    Verify whether the challan appears legally correct.
    """
    return get_ai_response_with_image(prompt, image_bytes, mime)


def generate_dispute_letter(
    name, address, vehicle, challan_no,
    offence_date, violation, fine_paid,
    legal_fine, grounds, state
):
    prompt = f"""
    Write a formal legal dispute letter.

    Name: {name}
    Address: {address}
    Vehicle: {vehicle}
    Challan Number: {challan_no}
    Offence Date: {offence_date}
    Violation: {violation}
    Fine Paid: ₹{fine_paid}
    Legal Fine: ₹{legal_fine}
    Grounds: {grounds}
    State: {state}

    Make it professional and ready to print.
    """
    return get_ai_response(prompt)


def compare_states(state1, state2, violation):
    prompt = f"""
    Compare traffic rules and fines for {violation}
    between {state1} and {state2}.
    """
    return get_ai_response(prompt)


def explain_rights(query):
    prompt = f"""
    Explain the legal rights of an Indian citizen
    in this traffic police situation:

    {query}
    """
    return get_ai_response(prompt)


def answer_legal_query(query):
    return get_ai_response(query)
