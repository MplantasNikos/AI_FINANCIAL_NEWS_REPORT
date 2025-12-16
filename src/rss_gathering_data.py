#Websites which we will use to get articles.

RSS_FEEDS = {
    "CNBC": "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "Yahoo Finance": "https://finance.yahoo.com/rss/topstories",
    "MarketWatch": "https://www.marketwatch.com/rss/topstories",
    "Investing.com": "https://www.investing.com/rss/news_25.rss"
}
#Imports
import feedparser
import pandas as pd
from datetime import datetime
import pytz


#Keywords to understand the country mentioned in the article or the title later.
COUNTRY_KEYWORDS = {
    "United States": [
        "us ", "u.s.", "united states", "america", "american",
        "fed", "wall street", "white house", "treasury"
    ],
    "China": [
        "china", "chinese", "beijing", "xi jinping"
    ],
    "United Kingdom": [
        "uk", "britain", "british", "london", "boe"
    ],
    "Europe": [
        "europe", "european", "eurozone", "ecb", "brussels"
    ],
    "Germany": [
        "germany", "german", "berlin"
    ],
    "Japan": [
        "japan", "japanese", "tokyo", "boj"
    ]
}


#Function to change the date format.
def parse_date(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=pytz.UTC)
    return None


#Function to find the country mentioned using the keywords from above.
def detect_country(title, summary):
    text = f"{title} {summary}".lower()

    for country, keywords in COUNTRY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return country

    return "Global"

#Function to get the urls and return the information from the articles we want.

def load_news(feeds, window_hours=24):
    articles = []

    for source, url in feeds.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            articles.append({
                "source": source,
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published_dt": parse_date(entry)
            })

    df = pd.DataFrame(articles)


    now = pd.Timestamp.utcnow()
    cutoff = now - pd.Timedelta(hours=window_hours)

    df = df[
        (df["published_dt"].isna()) |
        (df["published_dt"] >= cutoff)
    ]

    df["text"] = df.apply(
        lambda r: r["summary"] if len(str(r["summary"])) > 120 else r["title"],
        axis=1
    )

    df = df[df["text"].str.len() > 30]

    df["country"] = df.apply(
        lambda r: detect_country(r["title"], r["summary"]),
        axis=1
    )

    return df

