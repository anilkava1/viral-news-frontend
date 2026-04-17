import requests

def fetch_trending_news(category):
    # Aapka asli Render API link (Sahi wala)
    live_api_url = f"https://my-news-api-aa2o.onrender.com/my-api?cat={category}"
    
    print(f"--- Fetching news for: {category} ---")
    
    try:
        response = requests.get(live_api_url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"Success! Found {len(results)} news items.")
            return results
        else:
            print("API se sahi response nahi mila.")
            return []
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return []