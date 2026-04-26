import streamlit as st
import spacy
import cv2
from PIL import Image, ExifTags
import numpy as np

# ---------------- SETUP ----------------
st.set_page_config(page_title="Digital Footprint Analyzer", layout="centered")

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ---------------- UI HEADER ----------------
st.title("🔍 Digital Footprint Leakage Analyzer")
st.markdown("### AI-powered OSINT Risk Detection System")
st.info("This system analyzes text, images, and metadata to detect potential privacy and security risks.")

# ---------------- TEXT ANALYSIS ----------------
st.header("📝 Text Analysis")
text = st.text_area("Enter your post or message")

def analyze_text(text):
    text_lower = text.lower()
    risks = []

    # 🔴 HIGH RISK (Violence / Threat)
    high_risk = ["kill", "murder", "attack", "bomb", "shoot", "terrorist"]

    # 🔴 HIGH RISK (Defense / Sensitive Info)
    defense_risk = [
        "military", "army", "navy", "airforce",
        "camp", "base", "bunker", "weapon",
        "missile", "soldier", "troop", "deployment",
        "militant", "terrorist group", "location of camp"
    ]

    # 🟡 MEDIUM RISK
    medium_risk = ["location", "address", "phone", "email"]

    # 🟢 LOW RISK
    low_risk = ["going to", "travel", "hotel", "tomorrow"]

    # Detect risks
    for word in high_risk:
        if word in text_lower:
            risks.append((word, "HIGH"))

    for word in defense_risk:
        if word in text_lower:
            risks.append((word, "HIGH"))

    for word in medium_risk:
        if word in text_lower:
            risks.append((word, "MEDIUM"))

    for word in low_risk:
        if word in text_lower:
            risks.append((word, "LOW"))

    # 🔥 Intent Detection
    if any(word in text_lower for word in high_risk + defense_risk) and \
       any(intent in text_lower for intent in ["will", "going to", "plan", "located at"]):
        risks.append(("intent_detected", "HIGH"))

    # NLP Named Entities
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return risks, entities

# ---------------- IMAGE ANALYSIS ----------------
st.header("🖼️ Image Analysis")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

def analyze_image(image):
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

# ---------------- METADATA ----------------
def extract_metadata(image):
    metadata = {}
    try:
        exif = image._getexif()
        if exif:
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                metadata[decoded] = str(value)
    except:
        pass
    return metadata

# ---------------- RISK SCORING ----------------
def calculate_risk(risks, metadata):
    score = 0

    for word, level in risks:
        if level == "HIGH":
            score += 70
        elif level == "MEDIUM":
            score += 30
        else:
            score += 10

    # Metadata risk
    if "GPSInfo" in metadata:
        score += 30

    score = min(score, 100)

    if score >= 70:
        return score, "🔴 High Risk"
    elif score >= 30:
        return score, "🟡 Medium Risk"
    else:
        return score, "🟢 Low Risk"

# ---------------- AI EXPLANATION ----------------
def generate_explanation(risks, score):
    if not risks:
        return "No major risks detected. Content appears safe."

    explanation = "The system detected potential risks based on:\n"

    for word, level in risks:
        explanation += f"- '{word}' identified as {level} risk\n"

    if score >= 70:
        explanation += "\n🚨 This content includes sensitive or dangerous information."
    elif score >= 30:
        explanation += "\n⚠️ This content has moderate risk indicators."
    else:
        explanation += "\n✅ Minimal risk detected."

    return explanation

# ---------------- MAIN BUTTON ----------------
if st.button("🚀 Analyze Data"):

    st.subheader("📊 Analysis Results")

    text_risks = []
    metadata = {}

    # -------- TEXT --------
    if text:
        text_risks, entities = analyze_text(text)

        st.write("### 🔎 Text Analysis")

        if text_risks:
            st.write("Detected Risks:")
            for r in text_risks:
                st.write(f"{r[0]} → {r[1]} risk")
        else:
            st.write("No risky keywords found")

        st.write("Named Entities:")
        if entities:
            for ent in entities:
                st.write(f"{ent[0]} ({ent[1]})")
        else:
            st.write("No entities found")

    # -------- IMAGE --------
    if uploaded_file:
        image = Image.open(uploaded_file)

        st.write("### 🖼️ Uploaded Image")
        st.image(image, caption="Input Image", use_column_width=True)

        edges = analyze_image(image)
        st.write("### Edge Detection Output")
        st.image(edges, caption="Processed Image", use_column_width=True)

        metadata = extract_metadata(image)

        st.write("### 📍 Metadata")
        if metadata:
            for key, value in list(metadata.items())[:10]:
                st.write(f"{key}: {value}")
        else:
            st.write("No metadata found")

    # -------- FINAL RISK --------
    score, level = calculate_risk(text_risks, metadata)

    st.write("### ⚠️ Final Risk Assessment")
    st.write(f"Risk Score: {score}/100")
    st.write(f"Risk Level: {level}")

    # 🚨 ALERTS
    if score >= 70:
        st.error("🚨 CRITICAL THREAT OR SENSITIVE DATA DETECTED")

    if any(word in [r[0] for r in text_risks] for word in ["military", "army", "camp", "base", "militant"]):
        st.error("🚨 Sensitive Defense Information Detected")

    # 🤖 AI EXPLANATION
    st.write("### 🤖 AI Explanation")
    explanation = generate_explanation(text_risks, score)
    st.write(explanation)