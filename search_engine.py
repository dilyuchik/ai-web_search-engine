from flask import Flask, request, render_template, redirect, url_for
from crawler import crawl
from crawler import search as searching
from spellchecker import SpellChecker  # Import the SpellChecker library

app = Flask(__name__)

# Pre-crawl the website at the startup of the application
def initialize_crawler():
    start_url = 'https://vm009.rz.uos.de/crawl/index.html'  # Define the start URL for crawling
    print("Starting the crawling process...")
    crawl(start_url)  # Initiate crawling
    print("Crawling completed and pages are indexed!")

# Call the crawler during application initialization
initialize_crawler()

@app.route("/")
def index():
    return redirect(url_for('home'))
    
@app.route("/home")
def home():
    # Render the homepage template
    return render_template('home.html')

@app.route("/search")
def search():
    # Retrieve the query parameter from the URL (default is an empty string)
    query = str(request.args.get("query", ""))
    original_query = query  # Save the original query for reference

    # Initialize the spell checker and identify misspelled words in the query
    spell = SpellChecker()
    misspelled = spell.unknown(query.split())
    corrected_query = query  # Default the corrected query to the original query

    for word in misspelled:
        # Replace misspelled words with their corrected versions
        corrected_word = spell.correction(word)
        corrected_query = corrected_query.replace(word, corrected_word)

    # Determine if the query was corrected
    is_corrected = original_query != corrected_query

    # Perform a search using the corrected query
    search_results = searching(corrected_query)

    # Log the search results
    print(f"\nPages containing your search query '{corrected_query}':")
    for url in search_results:
        print(f"- {url}")

    # Render the search results template with the necessary information
    return render_template('search.html', 
                           search_results=search_results, 
                           original_query=original_query,
                           corrected_query=corrected_query,
                           is_corrected=is_corrected)

if __name__ == "__main__":
    app.run(debug=False)
