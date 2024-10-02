import requests
from bs4 import BeautifulSoup
from boilerpy3 import extractors

def remove_footer(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Debug: Print out the footer elements found
    footers = soup.find_all('footer')
    for footer in footers:
        footer.decompose()

    # Optionally, remove other elements commonly used in footers by ID or class
    footer_identifiers = ['footer', 'site-footer', 'main-footer', 'page-footer']
    for identifier in footer_identifiers:
        # Debug: Print out the elements found by ID
        tags_by_id = soup.find_all(attrs={"id": identifier})
        for tag in tags_by_id:
            tag.decompose()

        # Debug: Print out the elements found by class
        tags_by_class = soup.find_all(attrs={"class": identifier})
        for tag in tags_by_class:
            tag.decompose()

    return str(soup)

def get_html_content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=5)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return str(soup)
        elif response.status_code == 403:
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            return str(soup)
        else:
            return f"Failed to retrieve the content. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"
    

def get_text_from_url(url, ind):
    print(f"Looking at the following URL: {url}")
    base_response = get_html_content(url)
    if ("Failed to retrieve" in base_response) or ("An error occured:" in base_response):
        return "Unable to find any content"
    if ind == 0:
        try:
            extractor = extractors.ArticleExtractor()
            single_paragraph = extractor.get_content(base_response)

            return single_paragraph
        except IndexError:
            return "Nothing Found"
    else:
        try:
            cleaned_html = remove_footer(base_response)
            extractor = extractors.ArticleExtractor()
            single_paragraph = extractor.get_content(cleaned_html)

            return single_paragraph
        except IndexError:
            return "No Content Here"
        
# print(get_text_from_url("https://www.infinera.com/why-infinera/", 0))