import re
from typing import List, Dict, Optional

# List of keywords to identify company-affiliated authors
COMPANY_KEYWORDS = ["Inc.", "Ltd.", "LLC", "Pharma", "Biotech", "Therapeutics", "Corporation", "GmbH", "S.A."]

def extract_company_affiliations(authors: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Identifies company-affiliated authors from a list of authors.

    :param authors: List of dictionaries, each containing 'name', 'affiliation', and 'email'.
    :return: List of dictionaries containing only non-academic authors.
    """
    company_authors = []

    for author in authors:
        affiliation = author.get("affiliation", "")
        
        # Check if affiliation contains company-related keywords
        if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
            company_authors.append({
                "name": author.get("name"),
                "affiliation": affiliation,
                "email": author.get("email", "N/A")
            })
    
    return company_authors

def get_corresponding_author_email(authors: List[Dict[str, str]]) -> Optional[str]:
    """
    Extracts the email of the corresponding author if available.

    :param authors: List of dictionaries, each containing 'name', 'affiliation', and 'email'.
    :return: Email of the corresponding author, or None if not found.
    """
    for author in authors:
        if "@" in author.get("email", ""):
            return author["email"]
    
    return None
