import os.path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from whoosh.index import create_in, open_dir
from whoosh.fields import *

### Build index ###

# Store attributes in schema which can later be retrieved and displayed from index
def create_schema():
    schema = Schema(url=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))
    return schema

# Create index directory "indexdir" if not existing yet
# Create index directory if it doesn't exist
def create_index(directory="indexdir"):
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    # Create the index in the directory
    schema = create_schema()
    indx = create_in(directory, schema)
    return indx

def crawl_and_index(start_url, index_dir='indexdir'):
    """
    Function to crawl websites starting from a given URL and staying within the same domain of said URL.
    """
    indx = open_dir(index_dir)
    agenda = [start_url]
    base_domain = start_url.split('/')[2]  # Get domain from start_url

    # Initialize already visited, unique websites
    visited = set()
    
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

# Pre-crawl the website  with a specified starting url
def initialize_crawler(start_url):
    print("Starting the crawling process...")
    crawl_and_index(start_url)  # Initiate crawling
    print("Crawling completed and pages are indexed!")


# Initialize the crawler
if __name__ == "__main__":
    create_index()
    start_url = 'https://vm009.rz.uos.de/crawl/index.html'
    initialize_crawler(start_url=start_url)