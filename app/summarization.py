from transformers import pipeline

summarizer = pipeline("summarization")

def generate_summary(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False) 