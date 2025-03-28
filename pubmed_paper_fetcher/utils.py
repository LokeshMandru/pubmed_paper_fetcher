import re
from typing import List, Dict, Tuple

# List of common academic email domains
ACADEMIC_DOMAINS = [".edu", ".ac.uk", ".ac.in"]

# List of keywords indicating a pharmaceutical/biotech company
COMPANY_KEYWORDS = [
    "pharma", "biotech", "therapeutics", "inc", "ltd", "corp", "gmbh", "laboratories"
]

# Example list of known pharmaceutical/biotech companies (expandable)
KNOWN_COMPANIES = ["Pfizer", "Moderna", "AstraZeneca", "Novartis", "Gilead", "Regeneron"]

def is_non_academic(email: str) -> bool:
    """
    Determine if an email belongs to a non-academic institution.
    
    Args:
        email (str): Email address of an author.
    
    Returns:
        bool: True if non-academic, False otherwise.
    """
    if not email:
        return False  # No email provided

    domain = email.split("@")[-1]
    if any(domain.endswith(acad) for acad in ACADEMIC_DOMAINS):
        return False  # Academic email detected
    
    return True  # Likely non-academic

def extract_company_affiliations(affiliations: List[str]) -> Tuple[List[str], List[str]]:
    """
    Extracts non-academic authors and company affiliations.

    Args:
        affiliations (List[str]): List of author affiliations.

    Returns:
        Tuple[List[str], List[str]]: (Non-academic authors, Company names)
    """
    non_academic_authors = []
    company_names = []

    for aff in affiliations:
        if any(keyword.lower() in aff.lower() for keyword in COMPANY_KEYWORDS):
            company_names.append(aff)  # Identified company affiliation
            non_academic_authors.append(aff.split(",")[0])  # Extract author name if present
        elif any(company.lower() in aff.lower() for company in KNOWN_COMPANIES):
            company_names.append(aff)
            non_academic_authors.append(aff.split(",")[0])

    return non_academic_authors, company_names
