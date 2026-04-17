from flask import Flask, render_template, jsonify
from news_fetcher import fetch_trending_news
from datetime import datetime, timedelta

app = Flask(__name__)

# News store karne ke liye
news_store = {"trading": [], "india": [], "entertainment": []}
last_update_time = None

def update_news():
    global last_update_time
    categories = ["trading", "india", "entertainment"]
    for cat in categories:
        news_store[cat] = fetch_trending_news(cat)
    last_update_time = datetime.now()
    print(f"News updated at {last_update_time}")

@app.route('/')
def home():
    global last_update_time
    # Auto-update logic: Agar data purana hai toh khud update kare
    if last_update_time is None or datetime.now() > last_update_time + timedelta(minutes=30):
        update_news()
    
    return render_template('index.html', all_news=news_store)

@app.route('/category/<name>')
def category_page(name):
    name = name.lower()
    category_news = news_store.get(name, [])
    if not category_news:
        update_news()
        category_news = news_store.get(name, [])
    return render_template('category.html', news=category_news, category_name=name.capitalize())

@app.route('/update-now')
def update_route():
    update_news()
    return jsonify({"status": "success", "message": "Manual refresh successful"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)