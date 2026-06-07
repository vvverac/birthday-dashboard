import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="What's your Birthday Mood",
    page_icon="🎂",
    layout="centered"
)

month_df = pd.read_csv("month_info.csv")

def get_zodiac(month, day):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries ♈"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus ♉"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini ♊"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer ♋"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo ♌"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo ♍"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra ♎"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio ♏"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius ♐"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn ♑"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius ♒"
    else:
        return "Pisces ♓"

# Title first
st.markdown(
    """
    <div style="text-align:center; margin-top:25px;">
        <div style="font-size:44px; font-weight:700; color:#2F2F3A;">
            What's your Birthday Mood 🎂
        </div>
        <div style="font-size:18px; color:#4f4f4f; margin-top:10px; margin-bottom:25px;">
            Choose your birthday to discover your birth flower, birthstone, and today's mood!
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Birthday input
birthday = st.date_input(
    "Choose your birthday:",
    value=date(2004, 11, 8),
    min_value=date(1950, 1, 1),
    max_value=date.today()
)

# Month info after birthday exists
info = month_df[month_df["month"] == birthday.month].iloc[0]
bg_color = info["color"]

# Styling after bg_color exists
st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(255,255,255,0.88), transparent 28%),
            radial-gradient(circle at bottom right, rgba(255,255,255,0.78), transparent 30%),
            linear-gradient(135deg, {bg_color} 0%, #ffffff 100%);
    }}

    div[data-testid="stMetric"] {{
        background-color: rgba(255,255,255,0.78);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.8);
        text-align: center;
    }}

    .birth-card {{
        background-color: rgba(255,255,255,0.76);
        padding: 28px 18px;
        border-radius: 28px;
        box-shadow: 0 6px 22px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.85);
        text-align: center;
        margin-top: 18px;
        margin-bottom: 20px;
    }}

    .small-label {{
        font-size: 15px;
        letter-spacing: 1.6px;
        color: #7A6F6F;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}

    .big-name {{
        font-size: 34px;
        font-weight: 650;
        color: #2F2F3A;
        margin-bottom: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

today = date.today()
next_birthday = date(today.year, birthday.month, birthday.day)

if next_birthday < today:
    next_birthday = date(today.year + 1, birthday.month, birthday.day)

days_left = (next_birthday - today).days
weekday = birthday.strftime("%A")
zodiac = get_zodiac(birthday.month, birthday.day)

st.write("Your birthday is:", birthday)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Countdown", days_left)

with col2:
    st.metric("Born On", weekday)

with col3:
    st.metric("Zodiac", zodiac)

left_img, center_text, right_img = st.columns([1.05, 2.4, 1.05])

with left_img:
    st.image(info["flower_img"], width=260)

with center_text:
    st.markdown(
        f"""
        <div class="birth-card">
            <div class="small-label">Birth Flower</div>
            <div class="big-name">{info["flower"]}</div>
            <div class="small-label">Birthstone</div>
            <div class="big-name">{info["birthstone"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right_img:
    st.image(info["gem_img"], width=260)

st.subheader("Your mood today:")

try:
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    cat_url = response.json()[0]["url"]
    st.image(cat_url, use_container_width=True)
except:
    st.warning("The cute companion is taking a short break. Please refresh later.")

