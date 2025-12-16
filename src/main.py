from src.classifier_training import *
from src.summarizer import *
from src.rss_gathering_data import *
import pandas as pd
import joblib

#The sites we want to get articles from.
RSS_FEEDS = {
    "CNBC": "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "Yahoo Finance": "https://finance.yahoo.com/rss/topstories",
    "MarketWatch": "https://www.marketwatch.com/rss/topstories",
    "Investing.com": "https://www.investing.com/rss/news_25.rss"
}

#For later use 
SENTIMENT_MAP = [-1, 0, 1]

#For later use
def compute_sentiment_scores(proba):
    return (proba * SENTIMENT_MAP).sum(axis=1)


#With this function from rss_gathering_data.py, we are getting the articles from the web and also doing 
# the necessary processing.

df = load_news(RSS_FEEDS)

#Removing null article summaries, they exist because some of the websites don’t allow us to scrape them. 

df["summary"] = df["summary"].fillna("").str.strip()
df = df[df["summary"].str.len() > 0]


#Checking if any summary is too large, and if so, we use the function summarize_text from summarizer.py to make it fit.

texts = df['summary']
for text in texts:
    if len(text) >=500:
        text = summarize_text(text)



#Loading the pretrained model 
clasifier = joblib.load('models/classifier.joblib')


"""We make sentiment predictions on the new articles, and we also 
assign a score between -1 and 1 called the sentiment score:
 closer to -1 is negative, closer to 0 is neutral, and closer to 1 is positive.
That is the reason
 for the “for later use” at the beginning. We also calculate the 
 confidence of our model for the predicted sentiment, ranging from 0 (not strong) to 1 (strong)."""

preds = clasifier.predict(texts)
proba_preds = clasifier.predict_proba(texts)
sentiment_score = compute_sentiment_scores(proba_preds)
preds_confidence =  proba_preds.max(axis=1)


#Making predictions words .
category = []
for i in range(len(preds)):
    if preds[i] == 0:
        category.append('Negative')
    elif preds[i] == 1 : 
        category.append('Neutral')
    else:
        category.append('Positive')

df['category'] = category
df['sentiment_score'] = sentiment_score
df['category_confidence'] = preds_confidence
df["published_dt"] = df["published_dt"].dt.strftime("%Y-%m-%d %H:%M UTC")


#Making the final exported HTML board.
def category_color(category):
    if str(category).lower() == "positive":
        return "#d4edda"   # green
    elif str(category).lower() == "negative":
        return "#f8d7da"   # red
    else:
        return "#f2f2f2"   # neutral


from datetime import datetime


html_rows = ""

for _, row in df.iterrows():
    html_rows += f"""
    <tr style="background-color:{category_color(row['category'])}">
        <td>{row['title']}</td>
        <td>{row['summary']}</td>
        <td>{row['category']}</td>
        <td>{row['source']}</td>
        <td>{row['published_dt']}</td>
        <td><a href="{row['link']}" target="_blank">Open article</a></td>
        <td>{round(row['category_confidence'], 3)}</td>
    </tr>
    """

today = pd.Timestamp.utcnow().strftime("%Y-%m-%d")
html_filename = f"report-{today}.html"

html_content = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>Daily Market Sentiment Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}
        h1 {{
            text-align: center;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            vertical-align: top;
        }}
        th {{
            background-color: #333;
            color: white;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
    </style>
</head>

<body>
    <h1>Daily Market Sentiment Report</h1>
    <p>Date: {today}</p>

    <table>
        <tr>
            <th>Title</th>
            <th>Summary</th>
            <th>Category</th>
            <th>Source</th>
            <th>Published</th>
            <th>URL</th>
            <th>Confidence</th>
        </tr>
        {html_rows}
    </table>
</body>
</html>
"""

with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_content)


print('ready')
