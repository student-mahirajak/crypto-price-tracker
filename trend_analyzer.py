from collections import Counter

def analyze_trends(findings, scam_keywords):
    platform_counts = Counter()
    keyword_counts = Counter()

    for entry in findings:
        text = entry["text"].lower()
        platform = entry["platform"]

        for keyword in scam_keywords:
            if keyword in text:
                keyword_counts[keyword] += 1
                platform_counts[platform] += 1

    return keyword_counts, platform_counts
