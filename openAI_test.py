
import tiktoken
import pandas as pd
import time
from openai import OpenAI
from urllib.parse import urlparse, urlunparse, urljoin
from data_load import scrape_all

client = OpenAI(api_key = 'OPENAI_API_KEY')

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
    my_prompt = f"The Company's Name is {company_name} and the following content is taken from their website: {adj_prompt}"
    # print(f'Pushing prompt for {company_name}......')
    print(f"Prompt for {company_name} pushed for evaluation...............")

    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a super-focused market researcher and are researching companies who are building and investing resources in Generative AI tools. You read through content on their websites and make a judgement call in three ways. \
                 First, you can say that the company's interest in Generative AI is 'HIGH', which happens if they have launched AI chatbots or AI Agents, or are providing AI development tools through their platform, or anything involving or supporting generative AI or LLMs (Large Language Models).\
                 Second, you can say that the company's interest in Generative AI is 'MEDIUM', which happens if they talk about their work being impacted by Generative AI and its adoption, and if they hint on doing something to address it.\
                 Lastly, you can say that the company's interest in Generative AI is 'LOW', which happens if you don't see any content which talks about Generative AI or LLMs.\
                 Below are some examples of good classification (The prompts in these examples are pieces of content that you should look for to classify accurately, and they are followed by the right classification):\
                 1. Mentioned in Prompt: 'We are introducing Generative AI to Automate our Workflows' Classification: HIGH\
                 2. Mentioned in Prompt: 'Threat Detection' Classification: MEDIUM\
                 3. Mentioned in Prompt: 'Our platform has embedded Generative AI' Classification: HIGH\
                 4. Mentioned in Prompt: 'Contact Us. Schedule a call with Us' Classification: LOW\
                 5. Mentioned in Prompt: 'Fill out this form. Schedule a Demo.' Classification: LOW\
                 6. Mentioned in Prompt: 'Check out our new AI Assistant' Classification: HIGH\
                 7. Mentioned in Prompt: 'Introducing Co Pilot' Classification: HIGH\
                 8. Note for Healthcare related company: If the company talks about using AI in drug development or genetics or anything which resembles a biological science application and not a text/audio/video application of AI, just flag it as LOW\
                 9. Note for Cybersecurity Companies: Content that talks about using AI for fraud/threat detection, should be classified as HIGH if and only if it explicitly states the company's own AI agents or AI assistants. If you think these companies are spinning off machine learning or big data analytics as AI, then flag it as LOW\
                 10. Since this is web scraped content, you might get a raw HTML content or JSON content. If the entire content looks like a raw html, just return 'LOW'.\
                 11s. Note: If you find multiple instances of HIGH Generative AI-Centric Content, sit will take precedence over the things covered in the examples for Medium and Low categories. You should classify it as HIGH in that case\
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

def run_AI_check(data, i, scrape_ind):

    if scrape_ind:
        main_df = scrape_all(data)

        #Saving scraped data
        main_df.to_csv(f'C:/Users/sriva/Personal_Projects/WebScraper/current_output/scraped_output/scraped_data_{i+1}.csv', index=False)
    else:
        main_df = pd.read_csv(f'C:/Users/sriva/Personal_Projects/WebScraper/current_output/scraped_output/scraped_data_{i+1}.csv', index_col=False)
    
    main_df['AI_response'] = main_df.apply(lambda row: apply_with_delay(row), axis=1)
    print("AI Responses Received")

    return main_df