# gamify.py

def calculate_xp(actions):
    xp = 0
    if actions.get('logged_in'):
        xp += 10
    if actions.get('price_alert_set'):
        xp += 20
    if actions.get('scam_detected'):
        xp += 30
    if actions.get('darkweb_scanned'):
        xp += 15
    if actions.get('chart_viewed'):
        xp += 5
    return xp

def assign_level(xp):
    if xp < 50:
        return "🔰 Beginner"
    elif xp < 100:
        return "🚀 Intermediate"
    elif xp < 200:
        return "🔥 Pro"
    else:
        return "👑 Crypto Guardian Master"
