import requests

def fetch_trending_news(category):
    # DHYAN DEIN: Yahan ?cat={category} hona chahiye
    live_api_url = f"https://my-news-api-aa2o.onrender.com/my-api?cat={category}"
    
    print(f"--- Fetching news for: {category} ---")
    
    try:
        # 30 seconds timeout diya hai kyunki Gemini thoda time leta hai
        response = requests.get(live_api_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # API ke results nikal rahe hain
            results = data.get('results', [])
            print(f"Success! Found {len(results)} items for {category}")
            return results
        else:
            print(f"API Error: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return []