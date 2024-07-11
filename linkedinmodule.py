import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(
    page_title="LinkedIn Builder",
    page_icon="🖋️"
)
def scrape_from_url(urls): 
    loader = SeleniumURLLoader(urls= urls)
    documents = loader.load()
    return documents
st.title("LinkedIn builder📝")
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
        - Summarize key details about the company's industry, number of employees, size, financials, offersings and major competitors if available.

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

        - Benefits
            1. Benefit 1
            2. Benefit 2
            3. Benefit 3
            ...                                                         
            n. Benefit n         

       Quick Summary:
        - Summarize any other details available from the scrape here.                                                                                                                                                                   
                                                                                                                             
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
    Question: Who will be primary reader of your LinkedIn posts keeping in mind that all the audience on LinkedIn are professionals? \n
    Answer:
    Question: What do you want to tell him or her to inspire and engage the audience? (What’s your story?)
    \nAnswer: 
    Question: Do you understand the key informational needs of the audience? 
    \nAnswer: 
    Question: What are customers pain points? 
    \nAnswer: 
    Question: Who are the social media influencers in the space? \n
    Answer: 
    Question: What are the different trends in this industry? \n
    Answer: 
    Question: What are the different topics, pain points that influencers are posting about in this industry? \n
    Answer: 
    """
    prompt_ques = ChatPromptTemplate.from_template(template_ques)
    chain_ques = LLMChain(llm=llm1, prompt=prompt_ques)
    ques_out = chain_ques.invoke({"con": res_web['text']})
    st.info(ques_out["text"])

    template = """
    
    Text-only posts ↓
Single-image posts ↓
Multi-image posts ↓
Native videos ↓
Image carousels ↓
Video carousels ↓
Articles ↓
Newsletters ↓

    Act like a social media manager and copywriter. You are skilled in copywriting, human psychology, and writing bringing as much attention as possible to your social media posts. Jot down 25 can't-resist LinkedIn hooks that appeal to the target audience. The post can be either a text post, carousel, polls, quizzes, summary or books/talks relevant to the topic or tips. Choose topics related to customer pain points, trends in the relevant industry such as things you can teach about the topic, best practices, mistakes, things audience wishes they knew.

Each linkedin post starts with  A hook is the first line of a caption that makes people stop their scrolling on Linkedin and keep it under 20 words. It is so good and catchy, that people must feel something, a strong emotion, that makes them curious about the rest of the post. The hook is BY FAR the most important part of a post: it's 80% of the work.
Here are great hook examples that you MUST understand, analyze, master & get inspired from the following examples:
- You're chasing the wrong thing \n
- Harsh truth about ghostwriting:\n
- High-performers are burning out.\n
- Your business success is one plan away.\n
- Business ideas are a dime a dozen.\n
- I don't care about squeezing every last drop of revenue out of my business.\n
- Right now is the greatest era of self-promotion in history.\n
- Your "obvious knowledge" could be someone else's breakthrough.\n
- Strongly held belief: You'll never work for a better company than the one you build.\n

Additional tips:
Use numbers in the Hook when posible. 
Emphasize the benefit (“how to achieve X…”) or pain point ("…without having to Y."). 
Suggest originality ("underrated", “ignored”, “underappreciated”, “lesser known”)
No titles, No subheadings.
Please do not use buzz words or fluff words such as "Unlock, unveil, crack the code, guesswork"
Don't start the post with "Hey LinkedIn Fam"
Directly start every post with a hook 
Keep it under 700 words
Include emojis and hashtags

    Context: {con}

    \n
    Output format:
    1. *Titles*
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
    st.header("Suggested LinkedIn titles:")
    st.write(five_sim)