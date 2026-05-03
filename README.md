# 🚨 AI Disaster Response Assistant

A real-time, multilingual, and location-aware AI chatbot built to support communities during natural disasters. Developed at the **Pak Angels Generative AI Hackathon** (48-hour sprint). 🏆

🔗 **Live Demo:** [Try it here](https://lnkd.in/ej3DteSV)

---

## 🧠 Key Features

| Feature | Description |
|---------|-------------|
| 💬 AI Chatbot | Powered by Groq LLaMA3 for live disaster guidance |
| 🌐 Multilingual | Auto-detects language (Urdu, Hindi, Japanese, Turkish & more) |
| 📍 GPS-Aware | Detects user location → fetches local emergency numbers |
| 📷 Image Classification | Upload disaster images → classified using Hugging Face model |
| 🛡️ Safety Tips | Tailored guidance for earthquakes, floods, fires & more |
| 🕒 Chat History | Maintains conversation history with local timestamps |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **Streamlit** — Frontend UI
- **Groq API (LLaMA3)** — AI chatbot responses
- **Hugging Face** — Disaster image classification
- **Deep Translator** — Multilingual support
- **Geopy + TimezoneFinder** — GPS & location detection
- **streamlit-js-eval** — Browser geolocation

---

## 📁 Project Structure

```
ai-disaster-response-assistant/
│
├── app.py                  # Main chat assistant page
├── pages/
│   └── image_analysis.py   # Disaster image classification page
├── requirements.txt        # Dependencies
└── README.md
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/mahrukhmobin/ai-disaster-responsee-assistant.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key in .streamlit/secrets.toml
# [secrets]
# GROQ_API_KEY = "your_key_here"

# 4. Run the app
streamlit run app.py
```

---

## 🌍 Supported Countries & Emergency Numbers

| Country | Services |
|---------|---------|
| 🇵🇰 Pakistan | Rescue 1122, Ambulance 115, Police 15 |
| 🇮🇳 India | Ambulance 102, Disaster Helpline 108 |
| 🇺🇸 USA | Emergency 911 |
| 🇬🇧 UK | Emergency 999 |

---

## 👥 Team

| Member | Role |
|--------|------|
| **Mahrukh Mobin** | GUI + Core Python + GPS/Location features |
| Alishba Imran | Groq API integration + emergency numbers |
| Iffa Zainab | Image classification + disaster selection |
| Haleema Ahsan | Multilingual support + final presentation |
| Zoya Rabail | Code integration & deployment |
| Fizza Fatima | Project presentation design |

---

## 🏆 Built At

**Pak Angels Generative AI Hackathon** — organized by Pak Angels, iCodeGuru & ASPIRE Pakistan

---

*Built by [Mahrukh Mobin](https://github.com/mahrukhmobin) — Computer Engineering Student @ UET Lahore*
