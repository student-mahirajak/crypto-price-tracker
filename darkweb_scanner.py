# darkweb_scanner.py

def get_scam_trend_data():
    findings = [
        "BTC giveaway scam ongoing in Telegram",
        "Found private keys leak for bitcoin wallet",
        "Ethereum drain tool for sale",
        "Send ETH and get double back!",
        "Telegram ETH drain phishing link",
        "BTC giveaway scam ongoing in Telegram",
    ]

    scam_keywords = ['private keys', 'btc giveaway', 'drain', 'send eth', 'wallet', 'telegram']

    trend_counts = {keyword: 0 for keyword in scam_keywords}

    for sentence in findings:
        for keyword in scam_keywords:
            if keyword in sentence.lower():
                trend_counts[keyword] += 1

    return trend_counts
def scan_dark_web():
    # your dark web scraping or sample return logic
    return [
        ("btc giveaway", "BTC giveaway scam ongoing in Telegram"),
        ("private keys", "Found private keys leak for bitcoin wallet"),
        ("drain", "Ethereum drain tool for sale"),
        ("send eth", "Send ETH and get double back!"),
    ]


