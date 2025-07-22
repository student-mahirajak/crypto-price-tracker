import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Streamlit page setting
st.set_page_config(page_title="Crypto Heatmap", layout="wide")
st.title("🧊 Crypto Heatmap Dashboard")
st.markdown("### Top Coins with Green/Red Heatmap")

# Dropdown: Kitne top coins dekhne hai
top_n = st.selectbox("Kitne coins dikhane hai?", [5, 10, 15, 20], index=1)

# CoinGecko API se data lao
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': top_n,
    'page': 1,
    'sparkline': False
}
response = requests.get(url, params=params)
data = response.json()

# Data ko table bana ke store karo
df = pd.DataFrame(data)[['id', 'symbol', 'current_price', 'price_change_percentage_24h']]
df['color'] = df['price_change_percentage_24h'].apply(lambda x: 'green' if x > 0 else 'red')

# Plot TreeMap (color blocks)
fig = px.treemap(
    df,
    path=['id'],
    values='current_price',
    color='price_change_percentage_24h',
    color_continuous_scale='RdYlGn',
    title='24h Price Change Heatmap'
)

# Show graph
st.plotly_chart(fig, use_container_width=True)

