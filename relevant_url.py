import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd

# Function to get all links from the homepage
def get_all_links_from_homepage(homepage_url):
    try:
        response = requests.get(homepage_url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(homepage_url, href)
                links.add(full_url)
            return links
        elif response.status_code == 403:
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
            response = requests.get(homepage_url, headers=headers, timeout=5)
            if response == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = set()
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    full_url = urljoin(homepage_url, href)
                    links.add(full_url)
                return links
            else:
                print(f"Failed to retrieve content from {homepage_url}. Status code: {response.status_code}")
                return set()
        else:
            print(f"Failed to retrieve content from {homepage_url}. Status code: {response.status_code}")
            return set()
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

# Function to filter links based on keywords
def filter_links_by_keywords(links, keywords):
    filtered_links = set()
    for link in links:
        if any(keyword.lower() in urlparse(link).path.lower() for keyword in keywords):
            filtered_links.add(link)
    return filtered_links

#function to remove any non-sublinks
def filter_sublinks(homepage, links):
    def is_sublink(homepage, link):
        homepage_netloc = urlparse(homepage).netloc
        link_netloc = urlparse(link).netloc
        return homepage_netloc == link_netloc

    return [link for link in links if is_sublink(homepage, link['url'])]

def get_relevant_urls(company_name, homepage_url):
    general_keywords = ["blog", "resources", "news", "press", "insights", "updates", "product", "solutions", "how-it-works", "what-we-do", "latest-news", "Why"]
    primary_keywords = ["artificial-intelligence", "ai-", "-ai", "-ai-", "ai-assistant", "copilot", "co-pilot", "artificial", "chatbot", "ai-powered", "assistant", "pilot", "generative AI", "Gen-AI", "intelligence", "generative-ai", "language-model"]
    
    # Step 1: Get all links from the homepage
    all_links = get_all_links_from_homepage(homepage_url)
    
    # Step 2: Filter links based on keywords
    primary_links = filter_links_by_keywords(all_links, primary_keywords)
    general_links = filter_links_by_keywords(all_links, general_keywords)
    
    # Print filtered links
    url_list = []
    first_row = {'Company': company_name, 'url': homepage_url, 'url_type': "Home Page"}
    url_list.append(first_row)
    
    for link in primary_links:
        row_val = {'Company': company_name, 'url': link, 'url_type': "AI Specific Match"}
        url_list.append(row_val)

    for link in general_links:
        row_val = {'Company': company_name, 'url': link, 'url_type': "Generic Match"}
        url_list.append(row_val)

    url_list = [link for link in url_list if isinstance(link['url'], str) and pd.notna(link['url'])]

    final_list = filter_sublinks(homepage_url, url_list)

    return final_list[:20]