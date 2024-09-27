import requests
import xmltodict

# Function to get the PubMed article details from a given PubMed ID
def get_pubmed_data(pmid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
        "tool": "retraction-checker",
        "email": "your_email@example.com"  # Replace with your email for NCBI usage
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to check if the article is retracted
def is_retracted(pmid):
    pubmed_data = get_pubmed_data(pmid)
    if pubmed_data:
        data_dict = xmltodict.parse(pubmed_data)
        docsum = data_dict.get("eSummaryResult", {}).get("DocSum", {})
        if docsum:
            items = docsum.get("Item", [])
            for item in items:
                if item.get("@Name") == "PubTypeList" and "Retracted Publication" in str(item):
                    return True
    return False

# Function that takes a list of PMIDs and returns only retracted ones
def get_retracted_pmids(pmid_list):
    retracted_pmids = []
    for pmid in pmid_list:
        if is_retracted(pmid):
            retracted_pmids.append(pmid)
    return retracted_pmids

# Example usage with 12077603 added
pmid_list = ["12345678", "35163638", "22222222", "12077603"]  # Add more PMIDs as needed
retracted_articles = get_retracted_pmids(pmid_list)

# Output the retracted PubMed IDs (without any human-readable message)
print(retracted_articles)
