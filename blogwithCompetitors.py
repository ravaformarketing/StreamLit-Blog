import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
import os
import sys

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(
    page_title="Competitor Titles",
    page_icon="🖋️"
)
def scrape_from_url(urls): 
    loader = SeleniumURLLoader(urls= urls)
    documents = loader.load()
    return documents
st.title("Competitor Titles📝")
with st.form(key='my_form2'):
    #blog_title = st.text_input("Blog title", placeholder="Enter Blog title", key='inputtitle')
    comp_url = st.text_input("Add competitor URL", placeholder="Type or add URL of company", key='inputcompURL')
    # seok = st.text_input("SEO keywords", value = words, key='seoInp')
    # cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    # instruct = st.text_input("Instructions:", placeholder="Give some instructions", key='instr')
    submit_button2 = st.form_submit_button(label='Enter ➤')

if submit_button2 and comp_url:
    comp_info = scrape_from_url([f"{comp_url}"])
    comp_info = comp_info[0]
    llm2  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens = 4096)
    system_template = f"""You are an expert at extracting blog titles. 
    Given a web page scrap, extract all the blog titles present. Output in a python list of strings on only."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="{question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt= ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain_info = LLMChain(llm=llm2, prompt=chat_prompt)
    res = chain_info.invoke({"question": f"""Website scrap: {comp_info}

    # From the above information, extract all the blog titles and output them only in a python list of strings."""})
   
    st.write(f"# Blog titles scraped: \n\n{res['text']}")
    template1 = """Blog title: {idea}
    Suggest few blog titles based on the above titles in a way the chances of it ranking on google are very high.
    Make sure when you rewrite , even the author of the blog will not be able to guess if the blog was inpired from that. 
    Take into consideration only titles and topics that are relevant to your business and target audience. 
    """
        
    prompt1 = ChatPromptTemplate.from_template(template1)
    chain1 = LLMChain(llm=llm2, prompt=prompt1)
    st.write(f"# Classification:\n\n")
    for i in eval(res['text']):
        res2 = chain1.invoke({"idea":i})
        st.write(f"*\n\n{res2['text']}\n")