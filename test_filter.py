from pubmed_paper_fetcher.filter import extract_company_affiliations, get_corresponding_author_email

# Sample data for testing
authors_data = [
    {"name": "Alice Smith", "affiliation": "Harvard University", "email": "alice@harvard.edu"},
    {"name": "Bob Johnson", "affiliation": "Pfizer Inc.", "email": "bob@pfizer.com"},
    {"name": "Charlie Brown", "affiliation": "MIT", "email": "charlie@mit.edu"},
    {"name": "David Lee", "affiliation": "Genentech Biotech", "email": "david@genentech.com"}
]

# Test the function
company_authors = extract_company_affiliations(authors_data)
corresponding_email = get_corresponding_author_email(authors_data)

print("Company-Affiliated Authors:", company_authors)
print("Corresponding Author Email:", corresponding_email)
