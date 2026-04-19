import requests

def fetch_trending_news(category):
    # Naya Hugging Face API Link (Ismein ?cat=category ka format hai)
    live_api_url = f"https://anilkava-viral-news-india.hf.space/my-api?cat={category}"
    
    print(f"--- Fetching news for: {category} from Hugging Face ---")
    
    try:
        # Timeout 30 seconds rakha hai taaki Hugging Face aur Gemini mast response dein
        response = requests.get(live_api_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # Backend ke JSON structure ke hisaab se 'results' nikal rahe hain
            results = data.get('results', [])
            print(f"Success! Found {len(results)} items for {category}")
            return results
        else:
            print(f"API Error: Status {response.status_code} on Hugging Face")
            return []
            
    except Exception as e:
        print(f"Connection Error to Hugging Face: {e}")
        return []