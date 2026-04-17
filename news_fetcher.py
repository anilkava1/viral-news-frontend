import requests

def fetch_trending_news(category):
    # Aapka asli Live API link
    live_api_url = f"https://my-news-api-aa2o.onrender.com/my-api?cat={category}"
    
    try:
        # Timeout 30 seconds rakha hai taaki API 'jaag' sake
        response = requests.get(live_api_url, timeout=30)
        data = response.json()
        
        if data.get('status') == 'success':
            return data['results']
        return []
    except Exception as e:
        print(f"Error fetching from Live API: {e}")
        return []