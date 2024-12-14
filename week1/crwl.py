import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

# The index will store words and their corresponding URLs
index = defaultdict(list)
visited = set()

def crawl(start_url):
    agenda = [start_url]
    base_domain = start_url.split('/')[2]  # Get domain from start_url
    
    while agenda:
        url = agenda.pop(0)  # Get URL from the start of the list
        
        if url in visited:
            continue
            
        print("Crawling:", url)
        
        try:
            # Get and parse the page
            r = requests.get(url)
            if r.status_code == 200 and 'text/html' in r.headers.get('Content-Type', ''):
                soup = BeautifulSoup(r.content, 'html.parser')
                
                # Index the page content
                text = soup.get_text().lower().split()
                for word in set(text):  # Using set to avoid duplicates
                    if url not in index[word]:
                        index[word].append(url)
                
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

def search(words):
    """Search for pages containing all given words"""
    if not words:
        return []
    
    # Convert search words to lowercase
    words = [w.lower() for w in words]
    
    # Get URLs that contain the first word
    result_urls = set(index[words[0]])
    
    # Find intersection with URLs for all other words
    for word in words[1:]:
        result_urls &= set(index[word])
    
    return list(result_urls)

# Test the crawler
if __name__ == "__main__":
    # Test URL
    start_url = 'https://vm009.rz.uos.de/crawl/index.html'
    
    # Crawl the website
    crawl(start_url)
    
    print("\nCrawling completed!")
    print(f"Pages crawled: {len(visited)}")
    print(f"Words indexed: {len(index)}")
    
    # Test search
    test_words = ['welcome', 'page']
    results = search(test_words)
    print(f"\nPages containing {test_words}:")
    for url in results:
        print(f"- {url}")