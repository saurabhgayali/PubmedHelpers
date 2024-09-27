import requests
import time

def get_all_citing_articles(pmid):
    all_articles = []
    cited_in_links = []  # List to store links from pubmed_pubmed_citedin
    retstart = 0
    retmax = 100  # Number of records to fetch per request
    error_message = None
    previous_length = 0  # To track the length of cited_in_links

    while True:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id={pmid}&cmd=neighbor&retmode=json&retmax={retmax}&retstart={retstart}"

        # Wait to respect the API call limit (10 calls per second)
        time.sleep(0.1)  # Sleep for 0.1 seconds between calls

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            links = data.get('linksets', [])
            if not links:  # Break if no linksets are found
                print("No linksets found, exiting loop.")
                break
            
            # Extract citing articles specifically from pubmed_pubmed_citedin
            new_links = []  # Temporary list to collect new links
            for linkset in links:
                for linksetdb in linkset.get('linksetdbs', []):
                    if linksetdb['linkname'] == 'pubmed_pubmed_citedin':
                        # Add new links to the temporary list
                        for link in linksetdb.get('links', []):
                            if link not in cited_in_links:  # Check if link is new
                                new_links.append(link)

            # If there are new links, extend the main list
            if new_links:
                cited_in_links.extend(new_links)
                print(f"Citing articles for PMID {pmid}: {new_links}")
            else:
                print("No new citing articles found, exiting loop.")
                break  # Exit if no new links were found

            retstart += retmax  # Move to the next set of results
            
            # Print the number of calls made
            print("Calls made for " + str(retstart) + " number of papers")

        elif response.status_code == 429:
            # Handle rate limiting
            error_message = "Error: 429 Too Many Requests - Exceeded the rate limit."
            print(error_message)
            break  # Exit loop if rate limit is exceeded
        else:
            error_message = f"Error: {response.status_code}"
            print(error_message)
            break

    return {
        "error": error_message,
        "total_citing_articles": len(cited_in_links),
        "articles": cited_in_links
    }

# Example usage
result = get_all_citing_articles("35163638")
print(f"Total citing articles retrieved: {result['total_citing_articles']}")
if result['error']:
    print(result['error'])
