import requests
import pandas as pd
import typer
from rich.console import Console
from xml.etree import ElementTree as ET
import re  # For email extraction
import logging
from pathlib import Path

console = Console()
app = typer.Typer()

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Keywords to detect company affiliations
COMPANY_KEYWORDS = [
    "Inc.", "Ltd.", "Pharma", "Biotech", "Laboratories", "Corp", "Therapeutics",
    "GmbH", "LLC", "SA", "Diagnostics", "Technologies", "Health", "Medical"
]

# Email regex pattern
EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"


def fetch_pubmed_papers(query: str, max_results: int = 10, debug: bool = False):
    """Fetch research papers from PubMed based on the user query."""
    if debug:
        console.print(f"🔍 Searching for papers related to: [bold green]{query}[/bold green]")

    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    response = requests.get(PUBMED_SEARCH_URL, params=search_params)
    if response.status_code != 200:
        console.print("[bold red]❌ Failed to fetch papers from PubMed![/bold red]")
        return []

    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    console.print(f"✅ Found [bold yellow]{len(paper_ids)}[/bold yellow] papers.")

    if not paper_ids:
        return []

    return fetch_paper_details(paper_ids, debug)


def fetch_paper_details(paper_ids, debug=False):
    """Fetch detailed information for given paper IDs."""
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }

    fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)

    if fetch_response.status_code != 200:
        console.print("[bold red]❌ Failed to fetch paper details![/bold red]")
        return []

    root = ET.fromstring(fetch_response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "N/A"

        # Extract author details
        non_academic_authors = []
        company_affiliations = set()
        corresponding_email = "N/A"

        author_list = article.findall(".//Author")
        for author in author_list:
            last_name = author.find("LastName")
            first_name = author.find("ForeName")
            full_name = f"{first_name.text} {last_name.text}" if first_name is not None and last_name is not None else "Unknown"

            # Check for affiliation
            affiliation_info = author.find(".//AffiliationInfo/Affiliation")
            if affiliation_info is not None:
                affiliation_text = affiliation_info.text.lower()

                # Detect non-academic authors (exclude universities/hospitals)
                if not any(keyword in affiliation_text for keyword in ["university", "institute", "college", "hospital"]):
                    non_academic_authors.append(full_name)

                    # Check if affiliation is a pharmaceutical/biotech company
                    if any(keyword.lower() in affiliation_text for keyword in COMPANY_KEYWORDS):
                        company_affiliations.add(affiliation_info.text)

                # Extract email if available
                found_emails = re.findall(EMAIL_PATTERN, affiliation_text)
                if found_emails and corresponding_email == "N/A":
                    corresponding_email = found_emails[0]

            # Extract email from `<ElectronicAddress>`
            email_element = author.find(".//ElectronicAddress")
            if email_element is not None and corresponding_email == "N/A":
                corresponding_email = email_element.text

        papers.append({
            "PubMed ID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-Academic Authors": "; ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliations": "; ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email
        })

    return papers


def save_to_csv(papers, filename="result.csv"):
    """Save the results to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    console.print(f"✅ Results saved to: [bold cyan]{filename}[/bold cyan]")


def save_to_excel(papers, filename="result.xlsx"):
    """Save the results to an Excel file."""
    df = pd.DataFrame(papers)
    df.to_excel(filename, index=False)
    console.print(f"✅ Results saved to: [bold cyan]{filename}[/bold cyan]")


@app.command()
def run_pipeline(query: str, file: str = typer.Option(None, "--file", "-f"), debug: bool = typer.Option(False, "--debug", "-d")):
    """
    Fetch research papers from PubMed based on a query.

    Example Usage:
        python fetch_papers.py "cancer research" -f "papers.xlsx" -d
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        console.print("[bold blue]Debug mode enabled.[/bold blue]")

    papers = fetch_pubmed_papers(query, debug=debug)

    if not papers:
        console.print("[bold red]❌ No papers found.[/bold red]")
        return

    if file:
        if file.endswith(".csv"):
            save_to_csv(papers, file)
        elif file.endswith(".xlsx"):
            save_to_excel(papers, file)
        else:
            console.print("[bold red]❌ Unsupported file format. Use .csv or .xlsx[/bold red]")
    else:
        console.print(pd.DataFrame(papers))  # Print results if no file is specified


if __name__ == "__main__":
    app()
