import pandas as pd
import braintrust
from openai import OpenAI
from autoevals import Levenshtein
import asyncio
import time

braintrust.login(api_key = 'OPENAI_API_KEY')

client = braintrust.wrap_openai(OpenAI(api_key = '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'))



def return_bt_data(path):
    df = pd.read_csv(path)
    df = df[['Company', 'Content', 'expected_response']]

    new_dict = df.to_dict(orient="records")
    prompt_list = [
        {
        "input": f"The Company's Name is {new_dict[i]['Company']} and the following content is taken from their website: {new_dict[i]['Content']}",
        "expected": new_dict[i]['expected_response']
         }
        for i in range(len(new_dict))
    ]
    return prompt_list

MODEL = "gpt-4o"
SEED = 123

@braintrust.traced
def classify_article(input):
    time.sleep(1)
    messages = [
        {
            "role": "system", 
            "content": "You are a super-focused market researcher and are researching companies who are building and investing resources in Generative AI tools. You read through content on their websites and make a judgement call in three ways. \
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
             Few Examples of larger texts that are closer to your actual inputs (with classifications):\
             1. 'We are building battery recycling technologies that enable greater automation, competitiveness, and sustainability. We work with manufacturers, cathode producers, battery recyclers, battery collectors, and more to build advanced technologies that help our partners find greater efficiencies in their supply chains.'\
                 Classification: LOW\
             2. 'Our Smart Battery Sorting solutions automate battery identification and separation using artificial intelligence and a suite of robust measurement techniques. These systems are capable of separating batteries by specific chemistry with greater accuracy, higher speeds, and lower cost than traditional methods. Recycling Our innovative direct recycling process isolates the various components from spent lithium-ion batteries and regenerates them into commercial-grade battery materials for reuse'\
                  This novel recycling method is more cost effective and sustainable than others. Learn more Learn More Creating a truly circular economy Our technology solutions focus on finding greater efficiencies in the current battery recycling supply chain. We are able to drive meaningful cost savings while also ushering in\
                  a new era of environmental sustainability. A tech-first, automated approach to battery recycling We embrace the newest technologies to automate traditionally manual processes, resulting in lower costs, greater accuracy, and increased predictability over the supply chain.'\
                  Classification: LOW\
             2. 'The platform enables you to control and secure API keys, OAuth apps, service accounts and other NHIs, protecting your business and engineering environments from unauthorized access. THE PROBLEM The biggest identity blindspot: 10,000 non-human identities for every 1,000 employees While 49%% of breaches involve stolen credentials, 90%% of credentials are not protected by existing IAM solutions. Service accounts, API keys, OAuth apps, SSH keys and other NHIs hold privileged access to enterprise environments and remain under the radar.'\
                 Classification: LOW\
             3. 'Trusted by industry leaders Figma was built on the browser. As a cloud-native company, we work tirelessly to ensure that all of our software is secure and stable for our global users. Astrix bolsters our security promise by effectively monitoring risk from SaaS integrations.â€. Devdatta Akhawe,Head of Security â€œWith the rise in automation and new API-based integrations, ongoing monitoring and threat detection of what is accessing our environments became a key capability in our arsenal.â€ Yaron Slutzky,CISO â€œAstrix helps us to deal with a growing challenge â€“ tracking the lifecycle and the behavior of a token, especially when provided to a third-party.\
                  Astrix creates unprecedented visibility and changes the game for us.â€œ CISO â€œAPI keys, OAuth tokens, and service accounts are powerful credentials and should be protected as vigorously as user passwords. Astrix has helped us to take control over the app-to-app access layer for the first time.â€\
                  Gilad Solomon,Head of IT & Information Security â€œAstrix helps us to continuously reduce third-party risks by maintaining visibility and governance over thousands of non-human identities across the entire organization, from the corporate to the production environments.â€ CISO Thanks to behavioral analysis, we get alerts about suspicious connections in real-time and can immediately respond to incidents of stolen or abused tokens. Hannu Visti,Director of Information Security THE ASTRIX PLATFORM Take control over the non-human identity layer\
                  Our agentless solution enables you to inventory and manage NHIs across environments, allowing you to prioritize and remediate risks that expose you to supply chain attacks and data breaches. Inventory & posture Discover shadow NHIs and their business context. Get a prioritized list of their associated risks: over-privileged & sensitive access, untrusted vendors, etc. Threat detection Detect and respond to abuse of access tokens and suspicious NHI activity in real-time using behavior analysis.\
                  Remediation Automatically remediate NHI risks using out-of-the-box policies & workflows integrated to your security stack. Lifecycle management Easily manage the lifecycle of every non-human identity â€“ from creation to expiration and rotation. We secure NHIs across SaaS, IaaS and PaaS environments From Salesforce and Office 365 to GitHub, AWS, Azure and BigQuery, we ensure your environments are protected from NHI risks.\
                  Watch to learn more Safely unleash the power of connectivity, automation and GenAI To increase productivity and streamline processes, engineering, IT and business units need the freedom to connect third-party apps, internal services and machines to enterprise environments. Astrix allows you to make the most of your interconnected cloud, without compromising security. Identity and Access Management (IAM) Machine credentials outnumber user credentials, and are more privileged.\
                  Extend IAM programs to non-human identities from discovery and risk prioritization to threat detection and response. Learn more GenAI security 71 percent of employees use GenAI at work.* Astrix allows you to discover and secure GenAI services connected to your IaaS and SaaS environments. Learn more Third-party risk Existing TPRM programs assess only a fraction of your digital supply chain.'\
                  Classification: LOW\
             4. 'Solution: A modern Augmented Analytics platform Eltropy embedded Intelligent Search into their customer admin portal, which was used for reporting on customer success metrics. CSMs could now easily leverage search-driven analytics and actionable insights through a natural search experience, in addition to their custom reporting. Now, CSMs and their clients can make the most informed decisions using real time data. \
                 MachEye automatically analyzes new data in Redshift and updates existing reports, giving executives and users a 360 degree view of customer success interactions. In addition to understanding happened in the past, users get deeper insight into usage metrics changed and to act based on data. Designed for developers Powerful and easy-to-use APIs for data consumption Break free from the limitations of charts! \
                 It's easy to share your data insights with internal or external customers and transform their decision intelligence. Our APIs and SDKs simplify the integration of intelligent search into JavaScript, Java, and Python-based applications. Embed Search Box'\
                 'Classification: MEDIUM'\
             5. 'Analytics tools have found applications across industries and address use cases in various business functions including marketing , retail , customer success , or revenue operations . Users can interact with, discover, and consume insights on demand and at the point of decision-making. Thanks to artificial intelligence, insights are now more personalized and actionable than ever before, leading to optimized efficiency and costs for a data-literate organization. Key Highlights of a Self-Service Analytics Platform While evaluating self-service analytics platforms, here are some capabilities that you must consider. 1. Intuitive Search This is the most fundamental capability of a self-service analytics platform. Is the search readily available, intuitive, powerful, and easy to use? Is the search intelligent enough to understand a natural language and parse it to extract contextual answers? Users should be able to ask queries such as with highest sales this and get relevant answers instantly.\
                  2. Decision Intelligence Today, decision makers want to know beyond what happened, to understand why it happened, and how they can make better decisions. Self-service analytics platforms must provide such decision intelligence in the form of actionable insights, personalized recommendations, and real-time automated insights. 3. Interactive Visualizations Gone are the days when decision makers would spend hours and hours peering into lengthy reports and static dashboards, trying to make sense of the numbers. Self-service analytics platforms must make insights more consumable by offering interactive visualizations, engaging audio-visual data stories, audio narrations, and text summaries. 4. Data Security and Governance The importance of security and proper governance in data cannot be underlined enough in highly connected digital world.\
                  Self-service analytics platforms must open access for users to interact with data, and at the same time, apply granular policies to ensure that the right people have access to the right data. 5. Embedded Analytics When insights are embedded in a business workflow, users have to switch between applications and can benefit from readily available insights at the point of decision-making. Self-service analytics platforms must offer embedded analytics capabilities such as embedded search, insights, dashboards, and visualizations to reduce friction, provide a seamless experience, and boost data-driven decision-making. Benefits of Using Self-Service Analytics Organizations across industries have been seeing the benefits of self-service analytics tools . Here are some of the most important benefits. 1. Greater Data Accessibility Self-service analytics tools are a requirement for data literacy. Data democratization initiatives must provide a friendly interface for all users to consume insights easily, without requiring extensive training or technical knowledge.\
                  In order to successfully create a data literate workforce, users need tools that help them dive deep into data and generate deep insights that aid decision-making. Here, taking advantage of AI-Powered Analytics boosts the usability of data by augmenting decisions with personalized, timely insights. 2. Data Resource Optimization By reducing dependency on IT, self-service analytics frees up valuable human resources, such as Data Scientists, to focus on larger projects that require manual effort. Their expertise can be put towards complex challenges such as revenue forecasting models, competitive intelligence, and predicting market trends. On the other hand, business users can quickly automate less complex activities, such as data visualization, exploration, and periodic reporting. 3. Greater Data Accuracy Self-service analytics encourages a single source of truth as all consumers receive data from a centralized data source updated in real time.\
                  Today, ad hoc analysis is often done offline in Excel sheets or static reports, resulting in data silos and outdated insights. Self-service instant insights break through the data silos that may hamper accuracy. 4. Improved Decision-making In addition to basing business decisions on live data, self-service analytics further improves data-driven decision-making by expediting data access. Business users no longer have to wait for input from IT or data analysts, and can immediately tap into personalized insights to gather actionable recommendations . Organizations can now become insight-driven, instead of simply data-driven. 5. Cost Efficiency Advanced self-service analytics tools make businesses cost-efficient by saving manpower, streamlining access to data, and helping users make the right decisions at the right time.\
                  In addition, high user adoption means better scalability across the organization and faster time-to-insight for new employees. Many companies are also turning to modern cloud analytics for rapid onboarding and deployment across multiple business units. Implementing Self-Service Analytics in Your Organization 1. Prioritize business workflows that require data-driven insights Start by separating vanity metrics from the actual business metrics that are most important for your business. Prioritize the business workflows that are complex, time-consuming, recurrent, and need the latest data. Consider implementing self-service analytics for such processes to expedite actions, minimize risk, and reduce delays. Review the outcomes and apply the learnings from these workflows to further apply self-service analytics to other business workflows gradually. 2. Identify data sources for business workflows Different departments use different stacks for collecting and storing data.\
                  Decisions made based on incomplete and outdated data can lead to incorrect actions and disastrous outcomes. Perform a thorough inventory of all structured data sources. This provides clear visibility of available data and uncovers silos for consolidating all data. Look for direct data connector capabilities in self-service analytics tools that offer better data integration and prevent data duplication. 3. Opt for low-prep/no-prep onboarding of high-quality data Automating data processes can save significant time and efforts otherwise spent in manually cleaning and preparing data. Modern data analytics tools that offer automated data cataloging, entity relationship building, and metadata enrichment can ensure low-prep/no-prep onboarding. Once data is integrated, check for any missing or incomplete values, inconsistencies, and errors.\
                  If the data itself is incorrect, has duplicate or missing values, and is not consistent in nature, it loses its credibility to provide accurate insights. So verifying the quality of data is a must to get accurate insights. 4. Democratize access to data and insights restrict data-driven decision-making abilities only to high-level executives. Consider enabling it for the larger frontline workforce too such as account associates, sales representatives, marketing teams, customer success teams, or retail store managers. This ensures better decisions and actions at all levels within an organization. \
                  Classification: MEDIUM\
             6. 'Your money, in one place Holistic net worth tracking Origin gives you the full picture of where money's coming in and where it's going out â€” so you can navigate with clarity and confidence. Smart recommendations to help you hit your goals Origin automatically reviews and evaluates transactions to give actionable recommendations for budgeting and saving. Guidance built around you Get real-time answers to money questions with Sidekick, your AI-powered planner, or in-depth financial planning support from our CERTIFIED FINANCIAL PLANNERSâ„¢. Put your money to work Origin Invest offers automated investing with no advisory fees. You don't have to solve money questions solo.\
                 Classification: LOW\
             Few Things to Note before you start:\
             1. The examples above are not exhaustive, you have to read through the content and take a judgement call based on the use case. At the very basic level what you are looking for is applications or development of Generative Artificial Intelligence (AI)\
             2. For Healthcare related company: If the company talks about using AI in drug development or genetics or anything which resembles a biological science application and not a text/audio/video application of AI, just flag it as LOW\
             3. Note for Cybersecurity Companies: Content that talks about using AI for fraud/threat detection, should be classified as HIGH if and only if it explicitly states the company's own AI agents or AI assistants. If you think these companies are spinning off machine learning or big data analytics as AI, then flag it as LOW\
             4. For content around Internet of Things (IoT), be careful not to assume it as Generative AI development or application unless it explicitly says so. IoT is aggregation of data from different sources and is helpful in analytics but is not synonymous withGenerative AI development at all. SO rate it LOW unless you see explicit Generative AI applications being built.\
             5. The Company Name is provided at the beginning of every prompt. It is possible that the company cites another company doing Generative AI development but is not doing anything by itself. You need to flag conmtent as LOW if that is the case.\
             Note: If you find multiple instances of HIGH Generative AI-Centric Content, it will take precedence over the things covered in the examples for Medium and Low categories. You should classify it as HIGH in that case\
             The user will share with you the content of a particular webspage and the name of the company who's website is used to get this content. Your job is to read the content and classify it as high, medium or low based on the criteria defined above. You don't have to provide any explanation, just a single-word response.\
             Note that your output has to be one of 'HIGH', 'MEDIUM' or 'LOW' only. It should match every character of one of these responses. Do not change the case of your response or add any punctuation."
        },
        {
            "role":"user", 
            "content":input
        }
    ]
    result = client.chat.completions.create(
        model = MODEL,
        messages = messages,
        seed = SEED
    )
    category = result.choices[0].message.content
    return category

async def evaluate(dataset):
    await braintrust.Eval(
        "Classify Web Content to AI Interest Experiment",
        data=dataset,
        task=classify_article,
        scores=[Levenshtein]
    )

if __name__ == "__main__":
    path = "C:/Users/sriva/Personal_Projects/WebScraper/imp_examples.csv"
    dataset = return_bt_data(path)

    asyncio.run(evaluate(dataset))   

    # test_classify = classify_article(my_prompt)
    # print("Classified as: ", test_classify)
    # print("Score: ", 1 if test_classify == test_article['expected_response'] else 0)