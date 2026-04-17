from flask import Flask, render_template, jsonify
from news_fetcher import fetch_trending_news

app = Flask(__name__)

# Ye dictionary news ko memory mein store karegi
news_store = {
    "trading": [],
    "india": [],
    "entertainment": []
}

@app.route('/')
def home():
    # Agar news_store khali hai, toh pehle update kar lete hain
    if not news_store["trading"]:
        update_news()
    return render_template('index.html', news=news_store)

@app.route('/update-now')
def update_route():
    try:
        update_news()
        return jsonify({"status": "success", "message": "News updated successfully from Live API"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def update_news():
    categories = ["trading", "india", "entertainment"]
    
    for cat in categories:
        raw_data = fetch_trending_news(cat)
        processed = []
        
        if raw_data:
            for n in raw_data:
                # Yahan humne key names ko API ke mutabiq fix kar diya hai
                processed.append({
                    "title": n.get('title', 'No Title Available'),
                    "description": n.get('description', 'No description available.'),
                    "image": n.get('image', n.get('urlToImage', '')), # Dono handle karega
                    "url": n.get('url', '#')
                })
        
        news_store[cat] = processed

if __name__ == '__main__':
    # Local testing ke liye port 8000, Render ise khud handle karega
    app.run(host='0.0.0.0', port=8000, debug=True)