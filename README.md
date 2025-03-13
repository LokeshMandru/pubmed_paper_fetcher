📚 PubMed Paper Fetcher  

## 🚀 Overview  
This project is a command-line tool that fetches research papers from the **PubMed API** based on a user-specified query. The program identifies papers with at least one author affiliated with a pharmaceutical or biotech company and exports the results as a CSV file.  

## 📜 Features  
✅ Fetch research papers using the **PubMed API**  
✅ Supports **full PubMed query syntax**  
✅ Filters authors affiliated with **non-academic institutions**  
✅ Saves results in **CSV format**  
✅ Provides **command-line options** for flexibility  

## 📂 Output Format (CSV)  
The output file contains the following columns:  

| PubMed ID | Title | Publication Date | Non-Academic Authors | Company Affiliations | Corresponding Author Email |
|-----------|-------|------------------|----------------------|----------------------|---------------------------|

## 🛠️ Installation  

### **1️⃣ Clone the Repository**  

git clone https://github.com/LokeshMandru/pubmed_paper_fetcher.git
cd pubmed_paper_fetcher
2️⃣ Install Poetry
Ensure you have Poetry installed for dependency management.


pip install poetry
3️⃣ Install Dependencies

poetry install
⚡ Usage
Run the following command to fetch research papers:


poetry run get-papers-list --query "waste management"
Command-Line Options
Option	Description
-h, --help	Display usage instructions
-d, --debug	Print debug information during execution
-f, --file	Specify the filename to save the results (default: console output)
Example:


poetry run get-papers-list --query "biotech industry" --file output.csv
🔧 Configuration
Make sure your PubMed API Key is set in the environment variables for better performance:


export PUBMED_API_KEY="your_api_key_here"
🛠️ External Tools & Dependencies
1️⃣ PubMed API
Purpose: Fetches research papers based on user queries.
Docs: NCBI PubMed API
2️⃣ Poetry
Purpose: Dependency management and packaging.
Install:

pip install poetry
Docs: Poetry Official Docs
3️⃣ Git & GitHub
Purpose: Version control and repository hosting.
Install: Download Git
GitHub Repo: LokeshMandru/pubmed_paper_fetcher
4️⃣ Pandas
Purpose: Data processing and CSV file generation.
Install:

poetry add pandas
Docs: Pandas Official Docs
5️⃣ Requests
Purpose: Making HTTP requests to fetch data from PubMed API.
Install:

poetry add requests
Docs: Requests Library
📜 Project Structure
bash
Copy
Edit
📁 pubmed_paper_fetcher
│── 📄 pubmed_fetcher.py        # Core module to fetch papers
│── 📄 cli.py                   # CLI interface for running the script
│── 📄 utils.py                 # Helper functions for data processing
│── 📄 pyproject.toml           # Poetry configuration file
│── 📄 README.md                # Project documentation
│── 📄 requirements.txt         # Dependencies list (for non-Poetry users)
│── 📂 tests/                   # Unit tests for validation
🤝 Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

📜 License
This project is licensed under the MIT License.

✅ Next Steps
1️⃣ Replace your README.md with this updated version.
2️⃣ Commit & push the changes to GitHub:


git add README.md
git commit -m "Updated README with project details"
git push origin main
3️⃣ Confirm once done! 🚀
