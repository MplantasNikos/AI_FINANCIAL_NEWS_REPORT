from transformers import pipeline

#Pretrained model for summarization from Facebook, trained on CNN articles (exactly what we want). 
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)
#Function to call and use the model.
def summarize_text(text):
    if len(text.split()) < 50:
        return text

    result = summarizer(
        text,
        max_length=130,
        min_length=40,
        do_sample=False
    )
    return result[0]["summary_text"]
