import os
from flask import Flask, render_template, jsonify, request, send_from_directory
import requests

app = Flask(__name__)

# Aapki Backend API ka URL
API_BASE_URL = "https://my-news-api-aa2o.onrender.com"

# ==========================================
# SEO & GOOGLE SEARCH CONSOLE FIX
# ==========================================
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    # Ye files 'static' folder ke andar honi chahiye
    return send_from_directory(os.path.join(app.root_path, 'static'), request.path[1:])

# ==========================================
# MAIN ROUTES
# ==========================================

@app.route('/')
def index():
    categories = ["india", "trading", "entertainment", "cricket"]
    all_news = {}
    
    for cat in categories:
        try:
            # API se news fetch karna
            response = requests.get(f"{API_BASE_URL}/news/{cat}", timeout=10)
            if response.status_code == 200:
                all_news[cat] = response.json()
            else:
                all_news[cat] = []
        except Exception as e:
            print(f"Error fetching {cat}: {e}")
            all_news[cat] = []
            
    return render_template('index.html', all_news=all_news)

@app.route('/category/<name>')
def category_page(name):
    try:
        # Specific category page news
        response = requests.get(f"{API_BASE_URL}/news/{name.lower()}", timeout=10)
        news_data = response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error fetching category {name}: {e}")
        news_data = []
    return render_template('category.html', category_name=name.capitalize(), news=news_data)

@app.route('/update-now')
def update_news():
    try:
        # Backend ko signal dena news refresh karne ke liye
        refresh_req = requests.get(f"{API_BASE_URL}/update-news", timeout=15)
        if refresh_req.status_code == 200:
            return "News Updated Successfully! <a href='/'>Go Home</a>"
        else:
            return "API is active but refresh failed. <a href='/'>Go Home</a>"
    except Exception as e:
        return f"Failed to connect to API: {e}. <a href='/'>Go Home</a>"

# ==========================================
# RENDER DEPLOYMENT SETTINGS
# ==========================================

if __name__ == '__main__':
    # Render environmental port uthayega, default 5000 rahega
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)