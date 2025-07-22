import requests
from textblob import TextBlob

def fetch_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=becf030ca5f9c3d45eec2864427a85e8ebd7c5be&currencies=BTC,ETH"
    response = requests.get(url)
    data = response.json()

    results = data.get('results', [])
    if not isinstance(results, list):
        results = []

    news_items = []
    for post in results[:5]:  # Top 5 news only
        title = post.get('title', 'No Title')
        link = post.get('url', '#')
        sentiment_score = TextBlob(title).sentiment.polarity

        if sentiment_score > 0.2:
            mood = "positive"
        elif sentiment_score < -0.2:
            mood = "negative"
        else:
            mood = "neutral"

        news_items.append({
            "title": title,
            "url": link,
            "sentiment": mood
        })

    return news_items




