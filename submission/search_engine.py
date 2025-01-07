from flask import Flask, request, render_template
from crawler import crawl
from crawler import search as searching
from spellchecker import SpellChecker  # Import the SpellChecker

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    query = str(request.args["query"])
    original_query = query  # Save the original query

    # Spell check the query
    spell = SpellChecker()
    misspelled = spell.unknown(query.split())
    corrected_query = query

    for word in misspelled:
        # Get the closest correction for the misspelled word
        corrected_word = spell.correction(word)
        corrected_query = corrected_query.replace(word, corrected_word)

    # If the query was corrected, we'll pass that info to the frontend
    is_corrected = original_query != corrected_query

    # Test URL
    start_url = 'https://vm009.rz.uos.de/crawl/index.html'
    
    # Crawl the website
    crawl(start_url)
    
    print("\nCrawling completed!")
    
    # Test search
    search_results = searching(corrected_query)
    print("search_results: ", search_results)

    # Print all results
    print(f"\nPages containing your search query \'{corrected_query}\':")
    for url in search_results:
        print(f"- {url}")

    return render_template('search.html', 
                           search_results=search_results, 
                           original_query=original_query,
                           corrected_query=corrected_query,
                           is_corrected=is_corrected)

if __name__ == "__main__":
    app.run(debug=False)
