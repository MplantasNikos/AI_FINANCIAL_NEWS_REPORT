#  AI Financial News Intelligence Report

An end-to-end **AI-powered system** that collects global financial news, analyzes sentiment and category impact using NLP models, and produces 
a **daily professional HTML report** for businesses, investors, and analysts.

This project demonstrates a **production-oriented data science pipeline**, from real-world data ingestion to interpretable AI outputs.

---

##  Project Overview

The system automatically:

1. Collects **latest financial news** from trusted global sources via RSS
2. Cleans and preprocesses the text data
3. Applies **multiple NLP / AI models** for:
   - Sentiment analysis
   - Category classification
   - Confidence estimation
4. Generates a **daily HTML report** summarizing actionable insights

The output is designed to resemble a **real internal market intelligence report**, not a research notebook.

---

##  Data Sources

The project currently ingests data from RSS feeds of major financial news providers that officially support syndication:

- **Reuters**
- **CNBC**
- **Yahoo Finance**
- **MarketWatch**
- **Investing.com**

 **Engineering decision**:  
> RSS feeds were intentionally chosen over full web scraping due to the instability, legal constraints, and JavaScript-heavy nature of modern news websites.  
> This choice ensures **reliability, reproducibility, and scalability**.

---

##  AI & NLP Models Used

###  Financial Sentiment Classification  
**Dataset**: `Financial PhraseBank (sentences_allagree)`

A supervised NLP model trained to classify financial text into:

- **Negative**
- **Neutral**
- **Positive**

This dataset is widely used in academic and industry research for **financial sentiment analysis**, making the model domain-aware (not generic sentiment).

---

###  Sentiment Scoring Logic

Instead of raw labels only, the system computes a **continuous sentiment score**:

- Negative → −1  
- Neutral → 0  
- Positive → +1  

Using the model’s predicted probabilities, a **weighted sentiment score** is calculated per article, allowing:
- ranking
- aggregation
- trend analysis

This transforms NLP output into **business-usable signals**.

---

###  Category Classification

Each article is assigned to a **market-impact category** (e.g. positive / neutral / negative impact) with an associated **confidence score**.

This enables:
- filtering by confidence
- prioritization of high-signal news
- explainable AI outputs

---

###  Confidence Estimation

For every prediction, the system extracts the **maximum model probability** as a confidence metric.

This helps answer:
> *“How certain is the model about this classification?”*

Low-confidence predictions can be ignored or flagged for review.

---

###  Text Summarization (Optional / Experimental)

A **BERT-based summarization model** is included in the pipeline design.

- Currently applied conditionally (only when text length is sufficient)
- Intended for future expansion when full-article ingestion is enabled

This demonstrates extensibility toward **LLM-style workflows**.

---

##  Output: Daily HTML Report

The system generates a clean, professional HTML report containing:

- Article title
- Short summary
- Category & confidence
- Source
- Publication time
- Direct link to original article

📁 File naming convention:
