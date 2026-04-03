# 🩺 Aai — Maternal Misinformation Detection System

An AI-powered system that detects and debunks dangerous pregnancy myths
spreading across Indian communities. Built for anyone who has ever received
a scary health claim on WhatsApp and didn't know what to believe.

## 🔗 Live Demo
[maternal-health-mvp-msyjrkpubd7v4efzgu2msy.streamlit.app](https://maternal-health-mvp-msyjrkpubd7v4efzgu2msy.streamlit.app)

## 🚀 What it does
- Accepts text input or WhatsApp screenshot
- Preprocesses and cleans the input automatically
- Extracts specific health claims from the message
- Searches real medical databases (WHO, NCBI, MoHFW)
- Returns a cited verdict with severity and confidence score
- Minimizes hallucination using evidence grounding — says "insufficient evidence" when unsure

## ⚙️ Tech Stack
- **Groq (Llama 3.3 70B)** — claim extraction + response generation
- **Tavily** — live medical evidence search
- **Streamlit** — UI + deployment

## 📊 Output Format
Every response includes:
- Verdict (TRUE / FALSE / PARTIALLY TRUE / UNVERIFIED)
- Severity (🔴 DANGEROUS / 🟠 HARMFUL / 🟢 BENIGN)
- Confidence score (0-100%)
- Cited sources (clickable URLs)

## 🏥 Target Users
Pregnant women, their families, ASHA workers, Anganwadi workers,
community health volunteers — anyone navigating maternal health
information in India.

## ⚠️ Disclaimer
This tool is for informational purposes only.
Always consult a qualified healthcare worker.
