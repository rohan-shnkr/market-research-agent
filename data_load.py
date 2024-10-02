# from newscraper import get_text_from_url
from scraper2 import get_text_from_url
from relevant_url import get_relevant_urls
import pandas as pd
import re

def base_load(file_path):
    base_data = pd.read_csv(file_path, index_col=False)
    return base_data

def clean_content(content):
    print(content)
    paragraph = content.replace('\n', ' ')
    pattern = re.compile(r'\b\w*[^\x00-\x7F]+\w*\b')

    words = paragraph.split()
    cleaned_words = [word for word in words if not pattern.search(word)]

    cleaned_text = ' '.join(cleaned_words)
    # print("HERE IS THE NEW CONTENT")

    # print(cleaned_text)
    return cleaned_text

def scrape_all(base_df):
    # base_df = base_load(file_path)
    # print("DATA IMPORTED")

    base_dict = base_df.to_dict(orient="records")
    # print(base_dict)
    url_list = []
    temp_url_list = []
    for company in base_dict:
        print(f"Looking at {company['Company']}")
        temp_url_list = get_relevant_urls(company['Company'], company['Homepage'])
        url_list.append(temp_url_list)
        temp_url_list = []

    print("URL LIST IS COMPLETE")

    flat_list = [item for sublist in url_list for item in sublist]
    print("FLAT LIST OF url DICTIONARIES HAS BEEN CREATED")

    url_df = pd.DataFrame(flat_list)

    print("BEGINNING SCRAPPING WEBSITES")
    url_df['Content'] = url_df.apply(lambda row: get_text_from_url(row['url'], 1), axis=1)
    url_df['Content'] = url_df['Content'].apply(clean_content)
    url_df['token_ct'] = url_df['Content'].apply(lambda text: len(text.split()))
    url_df['char_ct'] = url_df['Content'].apply(lambda text: len(text))
    url_df = url_df.drop(url_df[url_df['token_ct']<100].index)

    return url_df