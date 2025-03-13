import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

# PubMed API base URLs
BASE_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BASE_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Keywords to identify non-academic affiliations
COMPANY_KEYWORDS = ["Inc", "Ltd", "LLC", "Corp", "Biotech", "Pharmaceuticals", "Pharma", "Therapeutics", "Biosciences", "Research Labs"]


def fetch_papers(query: str, debug: bool = False) -> List[Dict[str, str]]:
    """
    Fetch research papers from PubMed based on the given query.

    :param query: The search query.
    :param debug: If True, print debug information.
    :return: List of dictionaries containing paper details.
    """
    # Step 1: Search for paper IDs
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Adjust as needed
    }
    
    search_response = requests.get(BASE_SEARCH_URL, params=search_params)
    search_data = search_response.json()
    
    if debug:
        print(f"🔍 PubMed Query: {query}")
        print(f"🔗 Request URL: {search_response.url}")
        print(f"🛠 Raw API Response: {search_data}")

    # Extract PubMed IDs
    pubmed_ids = search_data.get("esearchresult", {}).get("idlist", [])
    
    if not pubmed_ids:
        return []

    # Step 2: Fetch full metadata for each paper
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    fetch_response = requests.get(BASE_FETCH_URL, params=fetch_params)
    root = ET.fromstring(fetch_response.content)

    results = []

    for article in root.findall(".//PubmedArticle"):
        # Extract core details
        pubmed_id = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        pub_date = article.find(".//PubDate/Year")
        publication_date = pub_date.text if pub_date is not None else "Unknown"

        # Extract author info
        authors = []
        company_authors = []
        company_affiliations = []
        corresponding_email = "N/A"

        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            affiliation = author.find(".//AffiliationInfo/Affiliation")
            email = author.find(".//AffiliationInfo/Affiliation").text if author.find(".//AffiliationInfo/Affiliation") is not None else None
            
            if last_name is not None and fore_name is not None:
                author_name = f"{fore_name.text} {last_name.text}"
                authors.append(author_name)

                # Identify company affiliations
                if affiliation is not None:
                    aff_text = affiliation.text
                    for keyword in COMPANY_KEYWORDS:
                        if keyword in aff_text:
                            company_authors.append(author_name)
                            company_affiliations.append(aff_text)
                            break  # No need to check more keywords

            # Extract corresponding author email
            if email and "@" in email:
                corresponding_email = email

        results.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": publication_date,
            "Non-academic Author(s)": "; ".join(company_authors) if company_authors else "N/A",
            "Company Affiliation(s)": "; ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email
        })

    if debug:
        print(f"✅ Processed {len(results)} papers.")

    return results
