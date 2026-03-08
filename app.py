import requests
import json
from bs4 import BeautifulSoup
import re

def analyze_tech_stack(url: str) -> dict:
    """Analyze a website to guess its core tech stack."""
    if not url.startswith("http"):
        url = "https://" + url
        
    stack = {"framework": "Unknown", "styling": "Unknown", "analytics": []}
    
    try:
        response = requests.get(url, timeout=5)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Meta framework detection
        if "next/router" in html or "_next" in html:
            stack["framework"] = "Next.js (React)"
        elif "data-reactroot" in html:
            stack["framework"] = "React"
        elif "vue" in html.lower():
            stack["framework"] = "Vue.js"
            
        # Styling detection
        if "tailwind" in html.lower():
            stack["styling"] = "Tailwind CSS"
        elif "Mui" in html:
            stack["styling"] = "Material UI"
            
        # Analytics detection
        if "google-analytics" in html or "gtag" in html:
            stack["analytics"].append("Google Analytics")
        if "segment.com" in html:
            stack["analytics"].append("Segment")
            
        return stack
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    target = "vercel.com"
    print(f"🔍 Analyzing {target}...")
    result = analyze_tech_stack(target)
    print(json.dumps(result, indent=2))
