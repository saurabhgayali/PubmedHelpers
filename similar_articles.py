import requests
import time

def get_similar_articles(pmid):
    similar_articles = []  # List to store similar article PMIDs
    retstart = 0
    retmax = 100  # Number of records to fetch per request
    error_message = None

    while True:
        # Construct API URL to retrieve similar articles using "neighbor" command
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id={pmid}&cmd=neighbor&retmode=json&retmax={retmax}&retstart={retstart}"

        # Wait to respect API call limits (10 calls per second)
        time.sleep(0.1)

        # Make API request
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            linksets = data.get('linksets', [])
            
            if not linksets:
                print("No similar articles found, exiting loop.")
                break
            
            # Extract similar article PMIDs
            new_articles = []  # Temporary list for new similar articles
            for linkset in linksets:
                for linksetdb in linkset.get('linksetdbs', []):
                    if linksetdb['linkname'] == 'pubmed_pubmed':
                        for link in linksetdb.get('links', []):
                            if link not in similar_articles:  # Add new articles only
                                new_articles.append(link)

            # Extend main list if new similar articles are found
            if new_articles:
                similar_articles.extend(new_articles)
                print(f"New similar articles found for PMID {pmid}: {new_articles}")
            else:
                print("No new similar articles found, exiting loop.")
                break

            # Increment retstart to paginate through results
            retstart += retmax

            # Print progress
            print(f"Calls made for {retstart} articles. Total similar articles collected: {len(similar_articles)}")

        elif response.status_code == 429:
            # Handle rate-limiting
            error_message = "Error: 429 Too Many Requests - Exceeded rate limit."
            print(error_message)
            break
        else:
            # Handle other errors
            error_message = f"Error: {response.status_code}"
            print(error_message)
            break

    return {
        "error": error_message,
        "total_similar_articles": len(similar_articles),
        "articles": similar_articles
    }

# Example usage
pmid = "35163638"  # Replace with your PubMed ID
result = get_similar_articles(pmid)
print(f"Total similar articles retrieved: {result['total_similar_articles']}")
if result['error']:
    print(result['error'])
