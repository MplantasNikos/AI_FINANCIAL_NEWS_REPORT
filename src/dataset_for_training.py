from datasets import load_dataset
from src.summarizer import summarize_text
import pandas as pd
from tqdm import tqdm

#Import an already existing financial dataset to use it to train our classifier. 
dataset = load_dataset(
    "financial_phrasebank",
    "sentences_allagree",
    split="train")




#Summarize each article so it is smaller and only the meaning is kept.
#Also getting the labels.
summaries = []
labels = []

for item in tqdm(dataset):
    text = item["sentence"]
    label = item["label"]

    try:
        summary = summarize_text(text)
        summaries.append(summary)
        labels.append(label)

    except Exception as e:
        print("Error on text:", text)
        print(e)


#Export data in CSV, ready to be used in training of the classifier.
ready_data = pd.DataFrame({'article':summaries,'label':labels})

ready_data.to_csv('data/data.csv')
