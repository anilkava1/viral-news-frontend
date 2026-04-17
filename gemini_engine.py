import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def rewrite_to_viral(title, description):
    prompt = f"""
    Rewrite this news in catchy viral Hinglish. 
    Format:
    Headline: [Viral Title]
    Body: [Viral Summary]
    
    News Title: {title}
    News Desc: {description}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"Headline: {title}\nBody: {description}"