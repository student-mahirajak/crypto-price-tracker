import streamlit as st
import requests
import json
from datetime import datetime
import plotly.graph_objs as go
import os
# 🎨 Custom CSS Styling
st.markdown("""
    <style>
    /* Page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Headings color */
    h1, h2, h3 {
        color: #00f7ff !important;
    }

    /* Sidebar style */
    .css-1d391kg {  /* sidebar */
        background-color: #111827;
    }
    .css-1v0mbdj {  /* sidebar radio labels */
        color: white !important;
    }

    /* Metric style */
    .stMetric {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
    }

    /* Links and text */
    a {
        color: #00f7ff !important;
        font-weight: 600;
    }

    /* Emojis & alerts spacing */
    .stMarkdown {
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Custom modules
from tracker import fetch_crypto_prices
from alerts import voice_alert, desktop_alert
from news_sentiment import fetch_crypto_news
from darkweb_scanner import scan_dark_web
from gamify import calculate_xp, assign_level
from darkweb_scanner import scan_dark_web, get_scam_trend_data


# ✅ Gamification: User activity tracking
user_actions = {
    'logged_in': True,
    'price_alert_set': False,
    'scam_detected': False,
    'darkweb_scanned': False,
    'chart_viewed': False
}

# Function to fetch 7-day data
def fetch_7day_price_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 7,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    dates = [datetime.fromtimestamp(item[0] / 1000).strftime('%b %d') for item in data['prices']]
    prices = [item[1] for item in data['prices']]
    return dates, prices

# Set page config
st.set_page_config(page_title="Crypto Guardian", layout="wide")
st.title("💹 Crypto Guardian: Live Price Tracker")
st.markdown("Track Bitcoin, Ethereum and more with Smart Alerts & News Sentiment")
# Sidebar Navigation
st.sidebar.title("🚀 Navigation")
selected_page = st.sidebar.radio("Choose Section", ["Dashboard", "News", "Dark Web", "Stats","Quiz"])

if selected_page == "Dashboard":
    st.title("💹 Crypto Guardian: Live Price Tracker")
    # threshold alerts + chart
    ...

   

elif selected_page == "Quiz":
   
    # Show quiz content

    st.markdown("## 🎯 Crypto Scam Awareness Quiz")
    st.write("Test your scam-spotting skills! Choose wisely...")

    with st.form("quiz_form"):
        q1 = st.radio("1. 'Send ETH and get double back!'", ["Scam", "Legit"])
        q2 = st.radio("2. 'You’ve won 2 BTC in our giveaway, click to claim!'", ["Scam", "Legit"])
        q3 = st.radio("3. 'Reminder: Your wallet was accessed from a new device, secure it now.'", ["Scam", "Legit"])
        submit_quiz = st.form_submit_button("Submit Answers")

    if submit_quiz:
        score = 0
        if q1 == "Scam": score += 1
        if q2 == "Scam": score += 1
        if q3 == "Legit": score += 1

        st.markdown("---")
        if score == 3:
            st.success("🎉 Perfect! You're a scam-fighting pro!")
            st.balloons()
        else:
            st.warning(f"🚨 You got {score}/3 correct. Stay alert!")



# Load config.json
with open("config.json") as f:
    config = json.load(f)

crypto_ids = ['bitcoin', 'ethereum']
prices = fetch_crypto_prices(crypto_ids)
st.write("DEBUG: Prices ->", prices)


st.markdown("## 🔎 Current Prices")
col1, col2 = st.columns(2)

for i, coin in enumerate(crypto_ids):
    price = prices[coin]['usd']
    threshold = config[coin]['threshold']
    delta = price - threshold

    with [col1, col2][i]:
        st.markdown(f"### {'📈' if i == 0 else '💰'} {coin.capitalize()}")
        st.metric(label="Current Price", value=f"${price}", delta=f"{delta:+.2f}")

        msg = f"{coin.capitalize()} price ${price} crossed your threshold ${threshold}!"

        # Prevent duplicate alerts
        last_alert_msg = ""
        if os.path.exists("alert_log.txt"):
            with open("alert_log.txt", "r") as log:
                lines = log.readlines()
                if lines:
                    last_alert_msg = lines[-1].strip().split(" - ")[-1]

        if price >= threshold and msg != last_alert_msg:
            voice_alert(msg)
            desktop_alert(msg)

            user_actions['price_alert_set'] = True  # ✅ XP Trigger

            with open("alert_log.txt", "a") as log:
                log.write(f"{datetime.now()} - {msg}\n")

# 🔥 Mood Sentiment from CryptoPanic
st.markdown("## 📰 Latest Crypto News + Mood")
news_items = fetch_crypto_news()

for post in news_items:
    title = post['title']
    url = post['url']
    sentiment = post['sentiment']
    emoji = "😐"
    if sentiment == 'positive':
        emoji = "😄"
    elif sentiment == 'negative':
        emoji = "😠"
    st.markdown(f"{emoji} [{title}]({url})")

# 🕵️‍♀️ Dark Web Scam Radar
st.markdown("## 🛑 Dark Web Scam Monitor")
scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"🕒 Last scanned at: **{scan_time}**")

scam_keywords = [
    "btc giveaway", "free ethereum", "private keys", "wallet",
    "seed phrase", "send eth", "drain", "scam"
]
alerts = []
darkweb_data = scan_dark_web()

for keyword, sentence in darkweb_data:
    lower_sentence = sentence.lower()
    for scam_word in scam_keywords:
        if scam_word in lower_sentence:
            alerts.append((scam_word, sentence))
            break

if alerts:
    for kw, alert in alerts:
        st.error(f"🚨 **Alert:** Keyword '**{kw}**' found in:\n> _{alert}_")
        user_actions['scam_detected'] = True
else:
    st.success("✅ No crypto-related scams detected on the dark web.")

st.info("✅ Scan completed successfully.")
user_actions['darkweb_scanned'] = True

# 📊 Selectable Coin Trend Chart (7-Day)
st.markdown("## 📈 7-Day Price Trend Viewer")

coin_options = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Solana": "solana",
    "Ripple": "ripple"
}
selected_coin_name = st.selectbox("Choose a coin:", list(coin_options.keys()))
selected_coin_id = coin_options[selected_coin_name]

# Plot chart
dates, prices = fetch_7day_price_data(selected_coin_id)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates, y=prices,
    mode='lines+markers',
    name=selected_coin_name,
    line=dict(color='cyan')
))
fig.update_layout(
    title=f"{selected_coin_name} - 7-Day Price Trend",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)
user_actions['chart_viewed'] = True

# 🎮 Gamification
st.markdown("## 🎮 Gamification Stats")

xp = calculate_xp(user_actions)
level = assign_level(xp)

st.markdown(f"**XP Gained:** `{xp}`")
st.markdown(f"**Current Level:** `{level}`")

xp_percent = min(xp / 200, 1.0)
st.progress(xp_percent)


