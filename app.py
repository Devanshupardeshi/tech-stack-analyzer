import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def analyze_tech_stack(url: str) -> dict:
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

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    target_url = ""
    if request.method == "POST":
        target_url = request.form.get("url", "")
        if target_url:
            result = analyze_tech_stack(target_url)
    return render_template("index.html", result=result, target_url=target_url)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
