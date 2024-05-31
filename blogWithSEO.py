import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(
    page_title="Blog Builder",
    page_icon="🖋️"
)
def scrape_from_url(urls): 
    loader = SeleniumURLLoader(urls= urls)
    documents = loader.load()
    return documents
st.title("Blog Builder📝")
words = ""

# Accepting text input from the user
with st.form(key='my_form'):
    seo = st.text_input("SEO Keywords", placeholder="Provide SEO keywords", key='input')

    # instruc = st.text_input("Instructions:", placeholder="Give some instructions", key='inst')
    #cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    submit_button = st.form_submit_button(label='Enter ➤')

if submit_button:
    
    llm1  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=4096)
    template = """You are an expert Blog Writer that can write blog titles given a list of SEO keywords. 
    Your goal is to grab reader's attention, generate curiosity, generate interest in the solution, evoke desire for its benefits, and prompt action just with the title of the blog. 
    
    Given a list of keywords, provide a list of potential long-tail keywords.
    Consider emotional, technical, psychological aspects related to the keyword.
    Do not use buzz words. Ban generic words such as "unveil, unlock, unleash, understand".

    Use all keyword variations, long tail keywords to create 5 creative titles under each of the following categories.
    Keep the titles punchy, curious, engaging, short and distinctly unique. Please do not repeat titles and keep each title unique and distinct. 
    1. List Post: A curated list of resources, books, tools and any other things related to this topic. 
    2. How-To Post: A step-by-step guide on how to complete a task. Each task is a unique task pertaining to the topic or sub topic or use cases around this topic. 
    3. Problem/Solution Post: Identifies a problem and presents a solution. Think of all the problems, pain points, challenges faced by customers in regards to the topic. 
    4. Checklist Post: A list of steps to complete a task. The task can vary based on different use cases around this topic. 
    5. The Ultimate Guide Post: An in-depth and comprehensive guide with topics ranging from usage, definition, use cases
    6. Definition Post: Explains a complex term or concepts related to the topic. 
    7. Pillar Post: Serves as the foundation for other blog posts on a core topic.
    8. Tips Post: Offers practical advice or suggestions while handling different use cases around this topic. 
    9. SAQ Post: Asks a question your audience might not consider but should be asking in relation to the topic?
    10. Tools Post: Lists and reviews tools helpful to your audience while tackling different use cases around this topic. 
    11. Question Post: Curate and answer questions your audience asks in social media, on forums, or in the comments section of your blog related to this topic.
    12. Case Study Post: Analyzes a project or event to showcase results of audiences tackling different use cases around your topic.

    -Use numbers wherever necessary.\n
    -Capitalise certain words in the titles.\n
    Good Example titles:\n
    How to turn $15 into 88,000 views with one simple mouse click… \n
    The six types of posts you absolutely MUST use to maximize user engagement\n
    How to build ultra-responsive BUYERS lists primed and ready to buy whatever you’re selling…\n
    One logical lie that is talked about in almost every free blog post that you absolutely DO NOT want to do… \n
    What kind of landing pages to send your visitors to for maximum results \n
    How to use Google to keep tabs on Facebook and track your clicks \n
    The six step "Cheat Sheet" that virtually guarantees your success…\n
     
    SEO keywords: {con}

    \n
    Output format:
    1. *List Post*
        -
        -
        -
        -
        -
    2. *How-To Post*
        -
        -
        -
        -
        -
    3. *Problem/Solution Post*
        -
        -
        -
        -
        -
    4. *Checklist Post*
        -
        -
        -
        -
        -
    5. *The Ultimate Guide Post*
        -
        -
        -
        -
        -
    6. *Definition Post*
        -
        -
        -
        -
        -
    7. *Pillar Post*
        -
        -
        -
        -
        -
    8. *Tips Post*
        -
        -
        -
        -
        -
    9. *SAQ Post*
        -
        -
        -
        -
        -
    10. *Tools Post*
        -
        -
        -
        -
        -
    11. *Question Post*
        -
        -
        -
        -
        -

    \n

    """
    #st.header("Prompt")
    
        
    prompt = ChatPromptTemplate.from_template(template)
    chain1 = LLMChain(llm=llm1, prompt=prompt)
    res = chain1.invoke({"con":seo})

    five_sim = res['text']
    st.header("Suggested blog titles:")
    st.write(five_sim)