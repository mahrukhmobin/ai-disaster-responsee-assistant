import streamlit as st
import requests
from datetime import datetime
from deep_translator import GoogleTranslator
from geopy.geocoders import Nominatim
from streamlit_lottie import st_lottie
from timezonefinder import TimezoneFinder
import pytz
from streamlit_js_eval import get_geolocation

# ---------------------------
# API Key (from secrets)
# ---------------------------
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ---------------------------
# Rescue numbers dictionary
# ---------------------------
rescue_contacts = {
    "Pakistan": {
        "Ambulance": "115",
        "Fire Brigade": "16",
        "Rescue Service": "1122",
        "Police": "15"
    },
    "India": {
        "Ambulance": "102",
        "Fire Brigade": "101",
        "Disaster Helpline": "108",
        "Police": "100"
    },
    "USA": {
        "Emergency Services": "911",
        "Fire Rescue Division": "888-772-3207"
    },
    "United Kingdom": {
        "Emergency Services": "999",
        "Non-Emergency Police Line": "101"
    }
}

# ---------------------------
# Timezone Helper
# ---------------------------
def get_timezone(lat, lon):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if tz_name:
        try:
            return pytz.timezone(tz_name)
        except Exception:
            return pytz.timezone("Asia/Karachi")
    return pytz.timezone("Asia/Karachi")

# ---------------------------
# Session setup
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "tz" not in st.session_state:
    st.session_state.tz = pytz.timezone("Asia/Karachi")

# ---------------------------
# CSS Styling
# ---------------------------
st.markdown("""
    <style>
    body { background-color: #0d1117; color: white; }
    h1, h2, h3, h4, h5 { color: white; }
    input, textarea, .stTextInput>div>div>input { background-color: #161b22 !important; color: white !important; }
    .chat-bubble { background-color: #f0f0f0; color: #000; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 10px; }
    .answer-box { background-color: #d6f5f5; padding: 1rem; border-radius: 12px; color: #000; }
    .contact-box { background-color: #ffeecc; padding: 1rem; border-radius: 10px; color: #000; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .sidebar .sidebar-content { background-color: #161b22; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.markdown("# 🌍 AI Disaster Response Assistant")
page = st.sidebar.radio("Navigation", ["Chat Assistant", "Image Analysis"])

if page == "Image Analysis":
    st.switch_page("pages/image_analysis.py")



# ---------------------------
# Main Page (Chat Assistant)
# ---------------------------
st.markdown("""
    <h1 style='text-align: center; background-color: #008080; color: white; padding: 1rem; border-radius: 12px;'>
    💬 AI Disaster Chat Assistant
    </h1>
""", unsafe_allow_html=True)

# ---------------------------
# Language Selection
# ---------------------------
language_options = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Japanese": "ja",
    "Turkish": "tr",
    "Italian": "it"
}
preferred_language = st.selectbox("🌐 Select your preferred language for responses:", list(language_options.keys()))
target_lang_code = language_options[preferred_language]

# ---------------------------
# Manual Location Dropdown
# ---------------------------
st.markdown("## 📍 Set Your Location")

location_options = {
    "Karachi, Pakistan": "Pakistan",
    "Islamabad, Pakistan": "Pakistan",
    "Lahore , Pakistan": "Pakistan",
    "Mumbai, India": "India",
    "London, UK": "United Kingdom",
    "Los Angeles, USA": "USA",
    "Miami, USA": "USA"
}

selected_location = st.selectbox("Choose a location:", list(location_options.keys()))
selected_country = location_options[selected_location]
st.markdown(f"🌍 Selected Country: **{selected_country}**")

# Overwrite country and user_location if user selects manually
user_location = selected_location
country = selected_country

# ---------------------------
# Get Location & Timezone
# ---------------------------
location_data = get_geolocation()
user_location = "Unknown"
city = ""
country = ""

if location_data and location_data.get("coords"):
    lat = location_data["coords"]["latitude"]
    lon = location_data["coords"]["longitude"]
    st.success(f"📍 GPS Location: {lat:.4f}, {lon:.4f}")
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((lat, lon), language='en')
        city = location.raw['address'].get('city', '') or location.raw['address'].get('town', '')
        country = location.raw['address'].get('country', '')
        user_location = f"{city}, {country}"
        st.markdown(f"📌 You are in {user_location}")
        st.session_state.tz = get_timezone(lat, lon)
    except Exception:
        st.warning("🌐 Could not resolve full address or timezone from GPS.")

# ---------------------------
# Display rescue numbers
# ---------------------------
if country in rescue_contacts:
    st.markdown("### 🚨 Local Emergency Numbers")
    contacts = rescue_contacts[country]
    for service, number in contacts.items():
        st.markdown(f"<div class='contact-box'>📞 <strong>{service}</strong>: {number}</div>", unsafe_allow_html=True)

# ---------------------------
# Chat UI
# ---------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🧠 Ask your question (any language):")
    user_input = st.text_area(" ", placeholder="e.g. زلزلے کے دوران مجھے کیا کرنا چاہیے؟ or What to do in a flood?", height=120)

    if st.button("🔍 Get Help"):
        if user_input.strip():
            try:
                translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

                if "emergency number" in translated_input.lower():
                    if selected_country in rescue_contacts:
                        contacts = rescue_contacts[selected_country]
                        st.markdown("### 🚨 Emergency Contact Details")
                        for service, number in contacts.items():
                            st.markdown(f"<div class='contact-box'>📞 <strong>{service}</strong>: {number}</div>", unsafe_allow_html=True)
                        st.stop()
                    else:
                        st.warning("🚫 No emergency data found for selected country.")
                        st.stop()

                location_context = f"The user is currently in {user_location}. Provide disaster-specific advice and include local rescue contact details if relevant. "
                prompt = f"{location_context}Answer this disaster-related question: {translated_input}"

                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

                if response.status_code == 200:
                    answer_en = response.json()['choices'][0]['message']['content']
                    translated_answer = GoogleTranslator(source='en', target=target_lang_code).translate(answer_en)
                    st.markdown(f"<div class='answer-box'>{translated_answer}</div>", unsafe_allow_html=True)

                    now = datetime.now(st.session_state.tz)
                    timestamp = now.strftime("%I:%M %p")
                    st.session_state.history.append({"time": timestamp, "question": user_input})
                else:
                    st.error("❌ Error: " + response.text)
            except Exception as e:
                st.error(f"⚠ Exception occurred: {e}")

with col2:
    st.markdown("### 📜 Chat History")
    if st.session_state.history:
        for entry in reversed(st.session_state.history):
            st.markdown(f"""
                <div class='chat-bubble'>
                    🕒 {entry['time']}<br><strong>{entry['question']}</strong>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No questions asked yet.")

    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.success("Chat history cleared.")
