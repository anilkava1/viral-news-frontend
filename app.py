import os
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
from news_fetcher import fetch_trending_news
from gemini_engine import rewrite_to_viral

load_dotenv()
app = Flask(__name__)

# Global storage for news
news_data = {"india": [], "trading": [], "entertainment": [], "cricket": []}

@app.route('/')
def index():
    return render_template('index.html', all_news=news_data)

@app.route('/category/<name>')
def category(name):
    cat_news = news_data.get(name, [])
    return render_template('category.html', category_name=name, news_list=cat_news)

@app.route('/update-now')
def update():
    global news_data
    print("Auto-updating all sections...")
    
    categories = ["india", "trading", "entertainment", "cricket"]
    for cat in categories:
        raw = fetch_trending_news(cat)
        processed = []
        for i, n in enumerate(raw):
            # Top 10 news ko AI se rewrite karwana (Speed ke liye)
            if i < 10:
                try:
                    ai_content = rewrite_to_viral(n['title'], n.get('description', ''))
                    lines = ai_content.split('\n')
                    title = lines[0].replace('Headline:', '').strip()
                    body = "<br>".join(lines[1:]).replace('Body:', '').strip()
                    processed.append({
                        "title": title or n['title'],
                        "content": body or n['description'],
                        "image": n['urlToImage'], "url": n['url']
                    })
                except:
                    processed.append({"title": n['title'], "content": n['description'], "image": n['urlToImage'], "url": n['url']})
            else:
                # Baaki news ko seedha add karna list lambi karne ke liye
                processed.append({
                    "title": n['title'], "content": n['description'],
                    "image": n['urlToImage'], "url": n['url']
                })
        news_data[cat] = processed
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)