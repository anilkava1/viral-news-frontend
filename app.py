from flask import Flask, render_template, jsonify
from news_fetcher import fetch_trending_news

app = Flask(__name__)

# News store karne ke liye dictionary
news_store = {
    "trading": [],
    "india": [],
    "entertainment": []
}

@app.route('/')
def home():
    if not news_store["trading"]:
        update_news()
    return render_template('index.html', all_news=news_store)

# --- NAYA CATEGORY ROUTE ---
@app.route('/category/<name>')
def category_page(name):
    name = name.lower() # Taki trading aur Trading dono chalein
    
    # Pehle check karein ki news memory mein hai ya nahi
    if name in news_store and news_store[name]:
        category_news = news_store[name]
    else:
        # Agar memory khali hai toh ek baar update karke dekhte hain
        update_news()
        category_news = news_store.get(name, [])

    if not category_news:
        return "Category not found or no news available", 404

    # Ye aapki category.html ko load karega aur data bhejega
    return render_template('category.html', news=category_news, category_name=name.capitalize())

@app.route('/update-now')
def update_route():
    try:
        update_news()
        return jsonify({"status": "success", "message": "News updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def update_news():
    categories = ["trading", "india", "entertainment"]
    for cat in categories:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)