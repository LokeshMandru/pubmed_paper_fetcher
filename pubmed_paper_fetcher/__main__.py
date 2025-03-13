import click
from pubmed_paper_fetcher.fetcher import fetch_papers
from pubmed_paper_fetcher.utils import save_to_csv, save_to_excel

@click.command()
@click.argument("query")
@click.option("-f", "--file", type=str, help="Output filename (CSV or XLSX)")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
def main(query, file, debug):
    """Fetch research papers from PubMed based on a query."""
    if debug:
        print(f"🔍 Searching for papers related to: {query}")

    papers = fetch_papers(query)
    
    if not papers:
        print("❌ No papers found!")
        return

    if file:
        if file.endswith(".xlsx"):
            save_to_excel(papers, file)
        else:
            save_to_csv(papers, file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
