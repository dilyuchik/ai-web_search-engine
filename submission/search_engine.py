from flask import Flask, request, render_template
from crawler import crawl
from crawler import search as searching

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    query = str(request.args["query"])

    # Test URL
    start_url = 'https://vm009.rz.uos.de/crawl/index.html'
    
    # Crawl the website
    crawl(start_url)
    
    print("\nCrawling completed!")
    
    # Test search
    search_results = searching(query)
    print("search_results: ", search_results)

    # Print all results
    print(f"\nPages containing your search query \'{query}\':")
    for url in search_results:
       print(f"- {url}")

    return render_template('search.html', search_results=search_results)

if __name__ == "__main__":
    app.run(debug=False)