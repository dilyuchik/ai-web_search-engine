from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search(query_words, index_dir='indexdir'):
    """
    Search for pages containing all query words using Whoosh, and extracts the title of the matching pages as well as the snippets within these pages containing the search query
    """
    indx = open_dir(index_dir)

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
    
    return search_results


# Test the searcher
if __name__ == "__main__":    
    # Test search
    test_query = "platypus"
    results = search(test_query)

    # Print all results
    print(f"\nPages containing your search query \'{test_query}\':")
