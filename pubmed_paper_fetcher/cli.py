import click
import pandas as pd
from pubmed_paper_fetcher.fetch import fetch_papers

@click.command()
@click.argument("query")
@click.option("-f", "--file", type=click.Path(), help="Output CSV filename")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
def main(query: str, file: str, debug: bool):
    """
    Fetch papers from PubMed based on a query and save as CSV.
    """
    click.echo(f"🔍 Searching for papers on: {query}")

    # Fetch papers
    papers = fetch_papers(query, debug)

    if not papers:
        click.echo("❌ No papers found for the given query.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(papers)

    # Save to file or print
    if file:
        df.to_csv(file, index=False)
        click.echo(f"✅ Results saved to {file}")
    else:
        click.echo(df.to_string())

if __name__ == "__main__":
    main()
