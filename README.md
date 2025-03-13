PubMed Paper Fetcher
A Python CLI tool to fetch research papers from PubMed based on a user query. It identifies papers with authors affiliated with pharmaceutical or biotech companies and exports the results to a CSV file.

🚀 Features
✔ Fetch research papers from PubMed API
✔ Supports advanced PubMed query syntax
✔ Identifies non-academic authors & company affiliations
✔ Exports results in CSV format
✔ CLI options: debug mode, custom filename, help

🛠 Installation
This project uses Poetry for dependency management.
First, install Poetry (if not installed):

sh
Copy
Edit
pip install poetry
Then, clone the repository and install dependencies:

sh
Copy
Edit
git clone https://github.com/YOUR_GITHUB_USERNAME/pubmed_paper_fetcher.git
cd pubmed_paper_fetcher
poetry install
📌 Usage
Run the command with a search query:

sh
Copy
Edit
poetry run get-papers-list "waste management"
CLI Options
Option	Description
-h or --help	Show usage instructions
-d or --debug	Print debug info
-f <filename> or --file <filename>	Specify output CSV filename
Example:

sh
Copy
Edit
poetry run get-papers-list "cancer treatment" -f results.csv
📁 Output Format (CSV)
The output file contains the following columns:

PubmedID: Unique ID of the paper
Title: Title of the research paper
Publication Date: Date published
Non-academic Author(s): Authors affiliated with companies
Company Affiliation(s): Pharmaceutical/Biotech companies
Corresponding Author Email: Contact email of the corresponding author
⚙️ Project Structure
bash
Copy
Edit
📂 pubmed_paper_fetcher
 ┣ 📜 pubmed_fetcher.py      # Core logic for fetching & filtering papers
 ┣ 📜 cli.py                 # Command-line interface
 ┣ 📜 utils.py               # Helper functions
 ┣ 📜 __init__.py            # Package initializer
 ┣ 📜 pyproject.toml         # Poetry configuration
 ┣ 📜 README.md              # Documentation
 ┣ 📜 results.csv            # Sample output file
🌟 Contributing
Want to improve this project?

Fork the repository
Create a new branch
Make your changes and push
Open a Pull Request
📜 License
MIT License. Feel free to use and modify. 😊