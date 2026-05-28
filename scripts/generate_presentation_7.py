# generate_presentation_7.py
"""Generate a concise 7‑slide PowerPoint deck for the DriveLegal AI hackathon submission.

Run this script (requires python‑pptx) to create `DriveLegal_AI_7Slide_Presentation.pptx` in the `docs/` folder.

    pip install python-pptx
    python scripts/generate_presentation_7.py
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# Output directory (repo root/docs)
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "docs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_path = OUTPUT_DIR / "DriveLegal_AI_7Slide_Presentation.pptx"

prs = Presentation()

# Helper functions
def add_title_slide(title, subtitle="Road Safety Hackathon 2026 – CoERS, IIT Madras × MoRTH"):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle

def add_bullet_slide(title, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    tf = slide.placeholders[1].text_frame
    tf.clear()
    for b in bullets:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(24)
        p.level = 0

def add_image_slide(title, image_path, caption=""):
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title & Content layout
    slide.shapes.title.text = title
    left = Inches(1)
    top = Inches(1.5)
    width = Inches(8)
    slide.shapes.add_picture(image_path, left, top, width=width)
    if caption:
        txBox = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = caption
        p.font.size = Pt(14)
        p.alignment = PP_ALIGN.CENTER

# ----- 7‑Slide Deck -----
# 1. Welcome
add_title_slide("🚦 Welcome to DriveLegal AI", "AI‑powered traffic‑law assistant")

# 2. Problem Statement
add_bullet_slide("The Problem", [
    "Millions of Indian drivers receive over‑charged traffic challans every year.",
    "Legal fine amounts differ across 18+ states – drivers lack clear guidance.",
    "Disputing fines requires a lawyer – costly and time‑consuming.",
    "Language barriers leave rural users unsupported."
])

# 3. Our Solution
add_bullet_slide("Our Solution", [
    "Upload a challan photo – AI instantly validates the fine against the MV Act 2019.",
    "One‑click generation of a printer‑ready dispute letter with legal citations.",
    "Multilingual AI chat (10+ Indian languages) for any traffic‑law query.",
    "Integrated calculators: fine, BAC, penalty points, document expiry, speed limits."
])

# 4. Real‑World Overcharge Demo (image)
add_image_slide("Demo: Over‑charge Detection", "C:/Users/rohit/.gemini/antigravity/brain/ffefbd62-1568-44d6-ad8b-3e37b1379f/real_challan_mockup_1779963537157.png", "AI flags ₹5,000 fine as OVERCHARGED – correct fine is ₹1,000.")

# 5. Impact & Benefits
add_bullet_slide("Impact", [
    "💰 Saves drivers up to ₹50,000 per year by preventing over‑charges.",
    "🛡️ Empowers 30 crore Indian vehicle owners with legal clarity.",
    "🚫 Reduces corruption – officers cannot arbitrarily inflate fines.",
    "🤝 Aligns with MoRTH Vision Zero 2030 and Digital India initiatives."
])

# 6. Roadmap & Future Extensions
add_bullet_slide("Roadmap", [
    "WhatsApp bot for on‑the‑go access.",
    "GPS‑based automatic state detection.",
    "Integration with UMANG & DigiLocker for document verification.",
    "AI‑driven outcome predictor for court cases."
])

# 7. Thank You
add_title_slide("Thank You!", "Visit the live demo: https://rohitheevlsi-drivelegal-ai.onrender.com\nGitHub: https://github.com/rohitheevlsi/rohitheevlsi-drivelegal-ai")

# Save the presentation
prs.save(output_path)
print(f"7‑slide presentation generated at {output_path}")
