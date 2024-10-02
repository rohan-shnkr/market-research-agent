import requests
from bs4 import BeautifulSoup
from boilerpy3 import extractors
from boilerpy3.exceptions import HTMLExtractionError

def remove_footer(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"Error parsing HTML with 'html.parser': {e}")
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            print(f"Error parsing HTML with 'lxml': {e}")
            try:
                soup = BeautifulSoup(html_content, 'html5lib')
            except Exception as e:
                print(f"Error parsing HTML with 'html5lib': {e}")
                return html_content  # Return the original content if all parsers fail

    footers = soup.find_all('footer')
    for footer in footers:
        footer.decompose()
    footer_identifiers = ['footer', 'site-footer', 'main-footer', 'page-footer']
    for identifier in footer_identifiers:
        tags_by_id = soup.find_all(attrs={"id": identifier})
        for tag in tags_by_id:
            tag.decompose()
        tags_by_class = soup.find_all(attrs={"class": identifier})
        for tag in tags_by_class:
            tag.decompose()
    return str(soup)

def get_html_content(url):
    try:
        response = requests.head(url, timeout=5)
        if 'text/html' in response.headers.get('Content-Type', ''):
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 403:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                }
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    return response.text
                else:
                    return f"Failed to retrieve the content. Status code: {response.status_code}"
            else:
                return f"Failed to retrieve the content. Status code: {response.status_code}"
        else:
            return "The URL does not point to an HTML document."
    except Exception as e:
        return f"An error occurred: {e}"

def get_text_from_url(url, ind):
    print(f"Looking at the following URL: {url}")
    base_response = get_html_content(url)
    if "Failed to retrieve" in base_response or "An error occurred" in base_response or "The URL does not point to an HTML document." in base_response:
        return "Unable to find any content"
    if ind == 0:
        try:
            extractor = extractors.ArticleExtractor()
            single_paragraph = extractor.get_content(base_response)
            return single_paragraph
        except HTMLExtractionError as e:
            print(f"Error parsing HTML content for URL {url}: {e}")
            return "Nothing Found"
        except IndexError:
            return "Nothing Found"
    else:
        try:
            cleaned_html = remove_footer(base_response)
            extractor = extractors.ArticleExtractor()
            single_paragraph = extractor.get_content(cleaned_html)
            return single_paragraph
        except HTMLExtractionError as e:
            print(f"Error parsing cleaned HTML content for URL {url}: {e}")
            return "No Content Here"
        except IndexError:
            return "No Content Here"