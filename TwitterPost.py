import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(
    page_title="Twitter Post Builder",
    page_icon="🖋️"
)
def scrape_from_url(urls): 
    loader = SeleniumURLLoader(urls= urls)
    documents = loader.load()
    return documents
st.title("Tweet builder📝")
words = ""

# Accepting text input from the user
with st.form(key='my_form'):
    comp_url = st.text_input("Add URL", placeholder="Type or add URL of company", key='inputcompURL')
    # seo = st.text_input("SEO keywords", placeholder="Enter SEO keywords to optimize blog to", key='seoinp')
    # instruc = st.text_input("Instructions:", placeholder="Give some instructions", key='inst')
    #cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    submit_button = st.form_submit_button(label='Enter ➤')

if submit_button:
    
    llm1  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=4096)
    comp_info = scrape_from_url([f"{comp_url}"])
    comp_info = comp_info[0]
    system_template = f"""You are an expert at quickly extracting key details about a business from a large block of text and using those details to generate an in-depth, compelling business summary. 
    Write the summary STRICTLY in the following format, elaborating on each section with supporting details and explanations. 
    
    Output format:
                                                                      
    Company Overview:
        - Company Name: Name of the company
        - Brief description of the business: Provide company overview along with the nitty-gritty details of the business.  Include also what makes this company unique. If there is a mission statement or purpose of the company, include this in this overview.
 
    Target Audience:
    Provide all target customer segments along any specific personas, customer demographics and pscyographics available in this section. 


    Problem Statement:                                                             
       -  Problem the product/service solves
            1. Problem 1
            2. Problem 2
            3. Problem 3
            ...                                                         
            n. Problem n
                                                                                                                                                                                                      
       - Pain points for target audience
            1. Pain point 1
            2. Pain point 2
            3. Pain point 3
            ...                                                         
            n. Pain point n
                                                                      
    Solution:
    Describe the product and service and how it solves the target audience's pain points. 
       -  How the product/service addresses the problem:
            1.
            2.
            3.
            ...
            n.                                                             

       - Key features and benefits
            1. Feature 1
            2. Feature 2
            3. Feature 3
            ...                                                         
            n. Feature n                                                                                                                                                                            
                                                                                                                             
        """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="{question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt= ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain_info = LLMChain(llm=llm1, prompt=chat_prompt)
    res_web = chain_info.invoke({"question": f"""Website scrap: {comp_info}

    From the above information, extract the brief description of the business and existing and probable problems in the product."""})
   
    st.write(f"# Company info: \n\n{res_web['text']}")
   
    template_ques = """Context: {con}\n
    Based on the above context, answer the following questions.
    Output format:
    Question: Who will be primary reader of your Tweets keeping in mind its about staying in trend on Twitter? \n
    Answer:
    Question: What are the different trends in this space? \n
    Answer: 
    Question: What are the different topics, pain points that influencers are posting about in this industry? \n
    Answer: 
    """
    prompt_ques = ChatPromptTemplate.from_template(template_ques)
    chain_ques = LLMChain(llm=llm1, prompt=prompt_ques)
    ques_out = chain_ques.invoke({"con": res_web['text']})
    st.info(ques_out["text"])

    template = """You are a social media manager who is skilled at crafting compelling tweets that resonate with a target audience and maximizing engagement.
Use the company information, target audience, pain points, and proposed solution to generate a variety of creative tweet ideas that would appeal to the target audience.
Your tweets follow this general structure:
    - Short, attention grabbing
    - Focused on trends, pain points, or solutions
    - Relatable to the target audience
    - Includes relevant hashtags


Tweet samples:
- "Feeling stressed and overwhelmed? Take a break and try our new Lavender Sleep Mist for a peaceful night's sleep." #selfcare #wellness\n
- "Is your phone battery dying by noon every day? Our new Ultra Battery Pack keeps you powered up for 24 hours!" #charger #techaccessories\n


Additional tips:
Suggest originality ("underrated", “ignored”, “underappreciated”, “lesser known”)
No titles, No subheadings.
Please do not use buzz words or fluff words such as "Unlock, unveil, crack the code, guesswork"
Don't start the post with "Hey"
Directly start every post with a hook 
Keep it under 280 characters
Include emojis and hashtags

    Context: {con}

    \n
    Output format:
    *Titles*
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
    """
    #st.header("Prompt")
    
        
    prompt = ChatPromptTemplate.from_template(template)
    chain1 = LLMChain(llm=llm1, prompt=prompt)
    res = chain1.invoke({ "con": ques_out['text']})
    five_sim = res['text']
    st.header("Suggested Tweets:")
    st.write(five_sim)