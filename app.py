from flask import Flask, render_template, request
from datetime import datetime
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)


@app.route("/")
def home():
  return render_template('home.html')


@app.route("/<fn>")
def index(fn):
  return render_template(f"{fn}.html")


@app.route("/review/listreview")
def review():
  with open("./data/review.json", 'r') as review_json:
    out_json = json.load(review_json)

  return out_json


@app.route("/review/postreview", methods=('POST', ))
def post_review():
  data = request.get_json()
  user = data.get("username")
  text = data.get("txt")
  time = datetime.now().isoformat()
  rating = data.get("pg_rating")
  sentiment = 'neutral'
  load_json = []
  try:
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
      sentiment = 'positive'
    elif scores['compound'] <= -0.05:
      sentiment = 'negative'
  except Exception as e:
    print(e)
  try:
    with open("./data/review.json", "r") as file:
      load_json = json.load(file)
  except Exception as e:
    print(e)

  data_dict = {
    "name": user,
    "datetime": time,
    "review": text,
    "review_type": sentiment,
    "rating": rating
  }
  load_json = [data_dict] + load_json
  with open('./data/review.json', 'w') as jf:
    json.dump(load_json, jf, indent=2)

  return {"Message": "success"}

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
