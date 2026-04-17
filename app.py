from flask import Flask, render_template, jsonify, request, send_from_directory
from news_fetcher import fetch_trending_news
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# News ko memory mein store karne ke liye
news_store = {
    "trading": [],
    "india": [],
    "entertainment": [],
    "cricket": []
}

last_update_time = None

# ==========================================
# SEO & GOOGLE SEARCH CONSOLE FIX (NEW)
# ==========================================
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    # Ye files 'static' folder ke andar se load hongi
    return send_from_directory(os.path.join(app.root_path, 'static'), request.path[1:])

# ==========================================
# NEWS LOGIC FUNCTIONS
# ==========================================
def update_news():
    global last_update_time
    print("--- Fetching Fresh News from API ---")
    
    # Charo categories jo humein dikhani hain
    categories = ["trading", "india", "entertainment", "cricket"]
    
    for cat in categories:
        try:
            data = fetch_trending_news(cat)
            if data:
                news_store[cat] = data
                print(f"Success: Got {len(data)} items for {cat}")
            else:
                print(f"Warning: No data received for {cat}")
        except Exception as e:
            print(f"Error fetching {cat}: {e}")
            
    last_update_time = datetime.now()
    print(f"Update completed at: {last_update_time}")

# ==========================================
# MAIN ROUTES
# ==========================================

@app.route('/')
def home():
    global last_update_time
    
    # AUTO-UPDATE: Agar 30 mins se zyada ho gaye toh khud update karega
    if last_update_time is None or datetime.now() > last_update_time + timedelta(minutes=30):
        update_news()
        
    return render_template('index.html', all_news=news_store)

@app.route('/category/<name>')
def category_page(name):
    name = name.lower()
    
    # Agar category memory mein nahi hai toh update karein
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
            "message": "News updated successfully",
            "time": last_update_time.strftime("%H:%M:%S")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render handles the port automatically
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)