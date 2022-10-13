from transformers import pipeline
from Functions.Historical_News import historical_news
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis")

model = TFAutoModelForSequenceClassification.from_pretrained("finiteautomata/bertweet-base-sentiment-analysis")

def bert(ticker, start, end):
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    news = historical_news.get_news_by_ticker(ticker, start, end)

    for i, n in enumerate(news):
        print(i, n)
        print(classifier(n))

bert('AAPL.US', '2021-01-01', '2021-09-09')
    