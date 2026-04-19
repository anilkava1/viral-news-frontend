from flask import Flask, render_template, jsonify, request, send_from_directory
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# ==========================================
# CONFIGURATION (Hugging Face Backend Link)
# ==========================================
# Aapka Hugging Face API ka sahi URL
API_BASE_URL = "https://anilkava-viral-news-india.hf.space/my-api"

# News ko memory mein store karne ke liye
news_store = {
    "trading": [],
    "india": [],
    "entertainment": [],
    "cricket": []
}

last_update_time = None

# ==========================================
# SEO & GOOGLE SEARCH CONSOLE FIX
# ==========================================
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(os.path.join(app.root_path, 'static'), request.path[1:])

# ==========================================
# NEWS LOGIC (Fetching from Hugging Face)
# ==========================================
def update_news():
    global last_update_time
    print("--- Fetching Fresh News from Hugging Face API ---")
    
    categories = ["trading", "india", "entertainment", "cricket"]
    
    for cat in categories:
        try:
            # Hugging Face Backend ko 'cat' parameter ke saath call kar rahe hain
            response = requests.get(f"{API_BASE_URL}?cat={cat}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Backend ke JSON structure ke hisaab se 'results' nikal rahe hain
                news_items = data.get('results', [])
                if news_items:
                    news_store[cat] = news_items
                    print(f"Success: Got {len(news_items)} items for {cat}")
                else:
                    print(f"Warning: No items in 'results' for {cat}")
            else:
                print(f"Error: API returned status code {response.status_code} for {cat}")
                
        except Exception as e:
            print(f"Error connecting to Hugging Face for {cat}: {e}")
            
    last_update_time = datetime.now()
    print(f"Update completed at: {last_update_time}")

# ==========================================
# MAIN ROUTES
# ==========================================

@app.route('/')
def home():
    global last_update_time
    if last_update_time is None or datetime.now() > last_update_time + timedelta(minutes=30):
        update_news()
    return render_template('index.html', all_news=news_store)

@app.route('/category/<name>')
def category_page(name):
    name = name.lower()
    if name not in news_store or not news_store[name]:
        update_news()
    
    category_news = news_store.get(name, [])
    if not category_news:
        return "Category not found or no news available", 404
        
    return render_template('category.html', news=category_news, category_name=name.capitalize())

@app.route('/update-now')
def update_route():
    try:
        update_news()
        return jsonify({
            "status": "success", 
            "message": "News updated successfully via Hugging Face",
            "time": last_update_time.strftime("%H:%M:%S")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)