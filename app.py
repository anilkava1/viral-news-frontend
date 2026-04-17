from flask import Flask, render_template, jsonify
import requests
from news_fetcher import fetch_trending_news

app = Flask(__name__)

news_store = {"trading": [], "india": [], "entertainment": []}

def update_news():
    categories = ["trading", "india", "entertainment"]
    for cat in categories:
        try:
            raw_data = fetch_trending_news(cat)
            processed = []
            if raw_data:
                for n in raw_data:
                    processed.append({
                        "title": n.get('title', 'No Title'),
                        "description": n.get('description', 'No description'),
                        "image": n.get('image', n.get('urlToImage', '')),
                        "url": n.get('url', '#')
                    })
            news_store[cat] = processed
        except Exception as e:
            print(f"Error updating {cat}: {e}")

@app.route('/')
def home():
    try:
        if not news_store["trading"]:
            update_news()
        return render_template('index.html', all_news=news_store)
    except Exception as e:
        return f"Home Page Error: {str(e)}", 500

@app.route('/category/<name>')
def category_page(name):
    try:
        name = name.lower()
        if not news_store.get(name):
            update_news()
        category_news = news_store.get(name, [])
        return render_template('category.html', news=category_news, category_name=name.capitalize())
    except Exception as e:
        return f"Category Page Error: {str(e)}", 500

@app.route('/update-now')
def update_route():
    update_news()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)