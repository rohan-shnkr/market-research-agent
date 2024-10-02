import re
import os
import pandas as pd
import requests
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from bs4 import BeautifulSoup
from boilerpy3 import extractors
from boilerpy3.exceptions import HTMLExtractionError
from urllib.parse import urljoin, urlparse
import time
from openai import OpenAI
import tiktoken

os.environ["GOOGLE_CLOUD_PROJECT"] = "news-search-project"

# This script has all functions

# Base Data Load

def base_load(file_path):
    base_data = pd.read_csv(file_path, index_col=False)
    return base_data

def return_base_data(path):
    data = base_load(path)
    print("DATA IMPORTED")

    #returning columns needed for content analysis
    data = data[['Organization Name', 'Website']]
    data.rename(columns={'Organization Name': 'Company', 'Website': 'Homepage'}, inplace=True)
    return data

# Google Search Setup

search_engine_id = "33d6ed45db04a4f04"
api_key = "AIzaSyCK1FKINwLGcPe2xmfdqOpTWviQy70Jv7U"

def custom_search(query, cx, api_key):
  """Searches a custom search engine for the given query and returns top 5 URLs.

  Args:
    query: The search query.
    cx: The custom search engine ID.
    api_key: The API key for the custom search engine.

  Returns:
    A list of top 5 URLs.
  """

  url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
  response = requests.get(url)
  results = response.json()
#   print(results)
  if 'items' in results:
      final_list = [item['link'] for item in results['items'][:4]]
  else:
      final_list = []
  return final_list

def return_url_list(company_name):
  search_term = f"Generative ai development news in {company_name}"
  results = custom_search(search_term, search_engine_id, api_key)
  return results

# Web Scraping

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

def clean_content(content):
    if pd.isna(content):
        return ""
    paragraph = content.replace('\n', ' ')
    pattern = re.compile(r'\b\w*[^\x00-\x7F]+\w*\b')

    words = paragraph.split()
    cleaned_words = [word for word in words if not pattern.search(word)]

    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text

# Getting URLs

def get_gsearch_urls(company_name, homepage):
  urls = return_url_list(company_name)

  #populate a list of dictionaries with company and individual url as keys and values
  company_dict_list = []
  for url in urls:
    company_dict_list.append({"Company": company_name, "Homepage": homepage, "URL": url})

  return company_dict_list


# Function to find and scrape all urls
def scrape_urls(base_df):

  #make an initial dictionary
  comp_dict_list = base_df.to_dict(orient="records")
  url_list = []

  # Iterating through companies
  for company in comp_dict_list:
    print(f"Looking at {company['Company']}")
    temp_url_list = get_gsearch_urls(company['Company'], company['Homepage'])
    url_list.extend(temp_url_list)
    time.sleep(3)

  # Creating url dataframe
  url_df = pd.DataFrame(url_list)

  #converting url_df to a dask dataframe and applying the get text from url and clean content function to every row to populate a content column
  dask_url_df = dd.from_pandas(url_df, npartitions=8)

  with ProgressBar():
    dask_url_df['Content'] = dask_url_df['URL'].map_partitions(lambda df: df.apply(lambda url: get_text_from_url(url, 1)), meta=('Content', 'object'))

    dask_url_df['Content'] = dask_url_df['Content'].dropna()
    dask_url_df['Content'] = dask_url_df['Content'].map_partitions(lambda df: df.apply(clean_content), meta=('Content', 'object'))

    #adding two columns for token count and character count of the content
    dask_url_df['token_ct'] = dask_url_df['Content'].map_partitions(lambda df: df.apply(lambda text: len(text.split())), meta=('token_ct', 'int'))
    dask_url_df['char_ct'] = dask_url_df['Content'].map_partitions(lambda df: df.apply(lambda text: len(text)), meta=('char_ct', 'int'))

    dask_url_df = dask_url_df[dask_url_df['token_ct'] > 100]

    result_df = dask_url_df.compute()

  return result_df

# LLM Call

client = OpenAI(api_key = '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')

def adjust_prompt(prompt):
    new_prompt = prompt
    token_limit = 12000

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    prompt_tokens = encoding.encode(prompt)

    if len(prompt_tokens) > token_limit:
        prompt_tokens = prompt_tokens[:token_limit]
        new_prompt = encoding.decode(prompt_tokens)
        print("Truncated the prompt")

    return new_prompt

def send_receive_message(company_name, prompt):
    adj_prompt = adjust_prompt(prompt)
    my_prompt = f"The Company's Name is {company_name} and the following content is taken from a news article about them: {adj_prompt}"
    # print(f'Pushing prompt for {company_name}......')
    print(f"Prompt for {company_name} pushed for evaluation...............")

    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a super-focused market researcher and are researching companies who are building and investing resources in Generative AI tools. You read through content on their websites and make a judgement call in three ways. \
                 First, you can say that the company's interest in Generative AI is 'HIGH', which happens if they have launched AI chatbots or AI Agents, or are providing AI development tools through their platform, or anything involving or supporting generative AI or LLMs (Large Language Models).\
                 Second, you can say that the company's interest in Generative AI is 'MEDIUM', which happens if they talk about their work being impacted by Generative AI and its adoption, and if they hint on developing something but not explicitly.\
                 Lastly, you can say that the company's interest in Generative AI is 'LOW', which happens if you don't see any content which talks about Generative AI or LLMs.\
                 1. Since this is web scraped content, you might get a raw HTML content or JSON content. If the entire content looks like a raw html, just return 'LOW'.\
                 2. Note: If you find multiple instances of HIGH Generative AI-Centric Content, sit will take precedence over the things covered in the examples for Medium and Low categories. You should classify it as HIGH in that case.\
                 3. Very Important thing to always keep in mind: These are news articles about the company so it should be clear that the AI development is tied to the company for you to score it HIGH. There may be other companies mentioned who are doing AI stuff, but if you are unable to tie the Generative AI development to the company that I mention in the beginning of the prompt, you should classify it as LOW.\
                 The user will share with you the content of a particular webspage and the name of the company who's website is used to get this content. Your job is to read the content and classify it as high, medium or low based on the criteria defined above. You don't have to provide any explanation, just a single-word response.\
                 Note that your output has to be one of 'HIGH', 'MEDIUM' or 'LOW' only. It should match every character of one of these responses. Do not change the case of your response or add any punctuation."},
                {"role":"user", "content":my_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def apply_with_delay(row):
    result = send_receive_message(row['Company'], row['Content'])
    time.sleep(3)
    return result

def run_AI_check(main_df):
    # Convert to Dask DataFrame
    ddf = dd.from_pandas(main_df, npartitions=25)

    # Apply the function in parallel
    with ProgressBar():
        ddf['AI_response'] = ddf.map_partitions(lambda df: df.apply(lambda row: apply_with_delay(row), axis=1), meta=('AI_response', 'object'))

        # Compute the result
        result_df = ddf.compute()

    print("AI Responses Received")
    return result_df

# Post Processing

def employee_tier(employees):
  if employees in ['1-10', '11-50', '51-100']:
    return 3
  elif employees in ['101-250', '251-500']:
    return 2
  else:
    return 1

def ai_interest(row):
  if row['emp_tier']==1:
    if row['total_datapoints']>1:
      if row['mean_score'] > 0.6:
        return 'Tier 1'
      elif row['mean_score'] > 0.3:
        return 'Tier 2'
      else:
        return 'Not AI Invested'
    elif row['total_datapoints']==1 and row['mean_score']==1:
      return 'Tier 1'
    else:
      return 'Not AI Invested'
  elif row['emp_tier']==2:
    if row['total_datapoints']>1:
      if row['mean_score'] >= 0.7:
        return 'Tier 1'
      elif row['mean_score'] > 0.4:
        return 'Tier 2'
      elif row['mean_score'] > 0.2:
        return 'Tier 3'
      else:
        return 'Not AI Invested'
    elif row['total_datapoints']==1 and row['mean_score']==1:
      return 'Tier 3'
    else:
      return 'Not AI Invested'
  else:
    if row['total_datapoints']>1:
      if row['mean_score'] >= 0.8:
        return 'Tier 2'
      elif row['mean_score'] > 0.2:
        return 'Tier 3'
      else:
        return 'Not AI Invested'
    elif row['total_datapoints']==1 and row['mean_score']==1:
      return 'Tier 3'
    else:
      return 'Not AI Invested'
    
def store_data_for_post_process(path):
    data = base_load(path)
    data = data[['Organization Name', 'Number of Employees', 'Website', 'LinkedIn', 'Estimated Revenue Range', 'Industries']]
    # print(data.head())

    data = data.rename(columns={'Organization Name': 'Company', 'Number of Employees': 'total_employees', 'Estimated Revenue Range': 'revenue_range', 'Industries': 'industries', 'Website': 'Homepage'})
    # print(data.head())

    data['total_employees'] = data['total_employees'].replace({'Nov-50': '11-50', '10-Jan':'1-10'})
    # print(data.head())

    return data
  
def post_process(data, path):
    #Generating a score column
    score_dict = {'high':1, 'medium':0.25, 'low': 0}
    data_ext = store_data_for_post_process(path)
    data['score'] = data['AI_response'].str.lower().map(score_dict)

    #grouping and storing in a new data
    new_df = data.groupby('Company').agg(mean_score = ('score','mean'), total_datapoints = ('URL','nunique')).reset_index()
    new_df = pd.merge(data_ext, new_df, on='Company', how='left')
    new_df = new_df.dropna(subset=['total_datapoints'])

    #Adding Employee Tiers
    new_df['emp_tier'] = new_df['total_employees'].apply(lambda x: employee_tier(x))

    #Final Tiering Companies
    new_df['Prospect_Tier'] = new_df.apply(lambda row: ai_interest(row), axis=1)

    return new_df
  
# Main Run
if __name__ == "__main__":
    input_path = 'C:/Users/sriva/Personal_Projects/WebScraper/current_input/google_search/input_data/'
    scraped_path = 'C:/Users/sriva/Personal_Projects/WebScraper/current_output/google_search/scraped_output/'
    temp_path = 'C:/Users/sriva/Personal_Projects/WebScraper/current_output/google_search/temp_output/'
    output_path = 'C:/Users/sriva/Personal_Projects/WebScraper/current_output/google_search/final_output/'

    # Assuming 20 input files (modify based on how many input splits you have)
    file_range = 12

    # Assuming this is a fresh run. If you have already few outputs in the output folder, and want to continue from the next input file onwards, then set it to the number of output files currently sitting in the final output folder.
    curr_split = 10

    for i in range(curr_split, file_range):
        print(f'-----------ITERATION-{i+1}-----------------------------------------------------')
        data_path = input_path+f'input_data_{i+1}.csv'
        base_data = return_base_data(data_path)

        if not base_data.empty:
            print("Base Data Ready")
        else:
            print("Base Data Not Ready, Aborting...")
            break
        
        #Initiating Scrape
        scraped_data = scrape_urls(base_data)
        scraped_data.to_csv(scraped_path+f'scraped_data_{i+1}.csv', index=False, escapechar='\\')

        #AI Evaluation
        main_data = run_AI_check(scraped_data)
        main_data.to_csv(temp_path+f'temp_{i+1}.csv', index=False, escapechar='\\')

        #Post Processing
        main_data_post_process = post_process(main_data, data_path)
        main_data_post_process.to_csv(output_path+f'final_output_{i+1}.csv', index=False, escapechar='\\')

        print(f"Final Output of Iteration: {i+1} saved")



