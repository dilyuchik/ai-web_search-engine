import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict
import os.path
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

### Build index ###

# Store attributes in schema which can later be retrieved and displayed from index
schema = Schema(url=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))

# Create index directory "indexdir" if not existing yet
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

indx = create_in("indexdir", schema) 

# Initialize already visited, unique websites
visited = set()

def crawl(start_url):
    """
    Function to crawl websites starting from a given URL and staying within the same domain of said URL.
    """
    agenda = [start_url]
    base_domain = start_url.split('/')[2]  # Get domain from start_url
    
    while agenda:
        url = agenda.pop(0)  # Get URL from the start of the list
        
        if url in visited: # Do not crawl already crawled URLs
            continue
            
        print("Crawling:", url)
        
        try:
            # Get and parse the page
            r = requests.get(url)
            if r.status_code == 200 and 'text/html' in r.headers.get('Content-Type', ''):
                soup = BeautifulSoup(r.content, 'html.parser')
                
                # Index the page content and title using Whoosh
                text = soup.get_text().lower()
                title = soup.find("title").text
                
                writer = indx.writer()  # index writer, allowing to add documents to index
                writer.add_document(url=url, content=text, title=title) # map field names to URL, content, and title of crawled website
                writer.commit() # save added document to index

                # for word in set(text):  # Using set to avoid duplicates
                #     if url not in indx[word]:
                #         indx[word].append(url)
                
                # Find all links and add them to agenda
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href)
                        # Only follow links to the same domain
                        if base_domain in full_url and full_url not in visited:
                            agenda.append(full_url)               
                
                visited.add(url)
                
        except Exception as e:
            print(f"Error processing {url}: {e}")


def search(query_words):
    """
    Search for pages containing all query words using Whoosh, and extracts the title of the matching pages as well as the snippets within these pages containing the search query
    """

    with indx.searcher() as searcher:
        # Parse query, searching in the "content" field while converting all user input to lowercase
        query = QueryParser("content", indx.schema).parse(query_words.lower())
        results = searcher.search(query)

        # Create empty list store the URLs from each document, which contains the searched words as well as the 
        # pages' title and snippets containing the searched words
        search_results = []
        for hit in results:
            title = hit['title']
            url = hit['url']
            snippet = hit.highlights('content')

            search_results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })

        #search_results = [(hit['url'], hit['title']) for hit in results]
        #print("tuple: ", search_results)
    
    return search_results

    # if not words:
    #     return []
    
    # # Convert search words to lowercase
    # words = [w.lower() for w in words]

    # # Get URLs that contain the first word
    # result_urls = set(index[words[0]])
    
    # # Find intersection with URLs for all other words
    # for word in words[1:]:
    #     result_urls &= set(index[word])
    
    #return list(result_urls)

def corrector(query_words):
    with indx.searcher() as searcher:
        corrector = QueryParser("content", indx.schema).parse(query_words.lower())
        corrected = searcher.correct_query(corrector, query_words)

    return corrected.string

# Test the crawler
if __name__ == "__main__":
    # Test URL
    start_url = 'https://vm009.rz.uos.de/crawl/index.html'
    
    # Crawl the website
    crawl(start_url)
    
    print("\nCrawling completed!")
    print(f"Pages crawled: {len(visited)}")
    #print(f"Words indexed: {len(indx)}")
    
    # Test search
    test_query = "platypus"
    results = search(test_query)

    # Print all results
    print(f"\nPages containing your search query \'{test_query}\':")
    #for url, title in results:
    #   print(f"- {title}")
    #   print(f"- {url}")
    print(corrector("welcome pag"))