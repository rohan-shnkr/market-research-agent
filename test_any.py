import requests
from bs4 import BeautifulSoup
from googlesearch import search

# Function to perform a Google search and get the top 5 URLs
def get_top_5_search_results(query):
    top_5_urls = []
    for url in search(query, num_results=5):
        top_5_urls.append(url)
    return top_5_urls

# Function to scrape content from a given URL
def scrape_url_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return None

# Main script
if __name__ == "__main__":
    query = "adidas generative AI news"
    
    # Get the top 5 search results
    top_5_urls = get_top_5_search_results(query)
    
    # Dictionary to store the scraped content
    scraped_content = {}
    success_count = 0

    # Scrape content from each URL
    for idx, url in enumerate(top_5_urls):
        print(f"Scraping URL {idx + 1}: {url}")
        content = scrape_url_content(url)
        if content:
            scraped_content[url] = content
            success_count += 1

    # Print the number of successfully scraped links
    print(f"Number of links successfully scraped: {success_count}")