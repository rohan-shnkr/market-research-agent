# AI Market Research Automation Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Dependencies](#dependencies)
7. [Configuration](#configuration)
8. [Output](#output)
9. [Limitations and Future Improvements](#limitations-and-future-improvements)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview

This project automates the process of conducting market research for AI observability tools, targeting potential B2B customers. It leverages web scraping, natural language processing, and GPT-3.5 to analyze companies' involvement in generative AI initiatives and score their potential as customers.

The primary goal is to identify and rank companies based on their attractiveness for AI observability tool sales, streamlining the lead generation and qualification process.

## Features

1. **Crunchbase Data Input**: Process company data from a Crunchbase Excel export.
2. **Relevant URL Scraping**: Automatically scrape company websites for pages related to analytics, AI, machine learning, and natural language processing.
3. **Content Extraction**: Extract and process content from identified URLs to understand key AI initiatives within each company.
4. **AI-Powered Analysis**: Utilize GPT-3.5 to analyze extracted content and score companies based on their potential for generative AI applications.
5. **Scoring System**: Score individual web pages and calculate aggregate scores for each company.
6. **Ranking**: Identify and rank top companies of interest based on aggregate metrics.
7. **Excel Output**: Generate an Excel file with company rankings and scores.

## System Architecture

1. **Data Input Module**: Handles input of Crunchbase company data from Excel files.
2. **Web Scraping Engine**: Crawls company websites and identifies relevant URLs.
3. **Content Extractor**: Processes and cleans content from scraped web pages.
4. **NLP Processor**: Analyzes extracted content to identify key AI initiatives.
5. **GPT-3.5 Integration**: Scores company attractiveness based on processed content.
6. **Scoring Module**: Calculates individual URL scores and aggregate company scores.
7. **Ranking Engine**: Sorts and ranks companies based on their aggregate scores.
8. **Excel Output Generator**: Creates a formatted Excel file with results.

## Installation

```bash
git clone https://github.com/yourusername/ai-market-research-automation.git
cd ai-market-research-automation
pip install -r requirements.txt
```

## Usage

1. Prepare an Excel file with company data exported from Crunchbase.
2. Run the main script:

```bash
python main.py --input crunchbase_companies.xlsx --output ai_market_research_results.xlsx
```

3. View the results in the generated `ai_market_research_results.xlsx` file.

## Dependencies

- Python 3.8+
- BeautifulSoup4
- Requests
- NLTK
- OpenAI GPT-3.5 API
- Pandas
- Openpyxl
- (Add any other specific libraries used in the project)

## Configuration

1. Create a `.env` file in the project root directory.
2. Add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

3. Adjust scraping parameters in `config.yaml`:

```yaml
scraping:
  max_pages_per_company: 10
  relevant_keywords:
    - analytics
    - artificial intelligence
    - machine learning
    - natural language processing
```

## Output

The project generates an Excel file containing:

- Company name and website
- Scraped URLs and their individual scores
- Aggregate company score
- Ranking among all analyzed companies

Example output structure:

| Rank | Company Name | Website | Aggregate Score | Top URL | Top URL Score |
|------|--------------|---------|-----------------|---------|---------------|
| 1    | AI Corp      | aicorp.com | 0.92 | aicorp.com/ai-solutions | 0.95 |
| 2    | TechGiant    | techgiant.com | 0.88 | techgiant.com/ml-products | 0.90 |
| 3    | DataDriven   | datadriven.io | 0.85 | datadriven.io/nlp-services | 0.87 |

Additional sheets in the Excel file may provide more detailed information about each company's analyzed URLs and scores.

## Limitations and Future Improvements

- Currently limited to English-language websites
- Scraping speed may be affected by website structures and anti-scraping measures
- Consider implementing multi-threading for faster processing
- Explore integration with additional data sources beyond Crunchbase
- Implement a user interface for easier data input and result visualization
- Add functionality to update existing Excel files with new data

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
