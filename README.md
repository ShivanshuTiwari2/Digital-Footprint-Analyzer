# 🔍 Digital Footprint Leakage Analyzer

## 📌 Overview
This project is an AI-based system that analyzes user-generated content (text and images) to detect potential privacy and security risks.

It identifies:
- Threat-related content
- Sensitive defense/military information
- Personal data exposure
- Image metadata risks

---

## 🚀 Features
- 🧠 NLP-based text analysis using spaCy
- ⚠️ Threat detection (kill, attack, etc.)
- 🪖 Military-sensitive data detection (army, camp, base)
- 🖼️ Image processing using OpenCV
- 📍 Metadata extraction from images
- 📊 Risk scoring system (Low / Medium / High)
- 🤖 AI-generated explanation

---

## 🛠️ Tech Stack
- Python
- Streamlit
- spaCy (NLP)
- OpenCV
- PIL (Image processing)

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m streamlit run app.py
