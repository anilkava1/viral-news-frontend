import requests
import time

def fetch_trending_news(category):
    live_api_url = f"https://my-news-api-aa2o.onrender.com/my-api?cat={category}"
    
    try:
        # 30 seconds timeout taaki API ko jagne ka time mile
        response = requests.get(live_api_url, timeout=30)
        
        # Check karein ki response sahi hai ya nahi
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        else:
            print(f"API Error: Status Code {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []