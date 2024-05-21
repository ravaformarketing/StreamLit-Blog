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
    user_input = st.text_input("Blog idea", placeholder="Describe", key='input')
    comp_url = st.text_input("Add URL", placeholder="Type or add URL of company", key='inputcompURL')
    # seo = st.text_input("SEO keywords", placeholder="Enter SEO keywords to optimize blog to", key='seoinp')
    # instruc = st.text_input("Instructions:", placeholder="Give some instructions", key='inst')
    #cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    submit_button = st.form_submit_button(label='Enter ➤')

if submit_button and user_input:
    
    llm1  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=4096)
    comp_info = scrape_from_url([f"{comp_url}"])
    comp_info = comp_info[0]
    system_template = f"""You are an expert at quickly extracting key details about a business from a large block of text and using those details to generate an in-depth, compelling business summary. 
    Write the summary STRICTLY in the following format, elaborating on each section with supporting details and explanations. 
    
    Output format:
                                                                      
    Introduction:

        - Company name:
        - Tagline:
        - Brief description of the business:

    Problem Statement:
                                                                      
        Problem the product/service solves
            1. Problem 1
            2. Problem 2
            3. Problem 3
            ...                                                         
            n. Problem n
                                                                                                                                                                                                      
        Pain points for target audience
            1. Pain point 1
            2. Pain point 2
            3. Pain point 3
            ...                                                         
            n. Pain point n
                                                                      
    Solution:

        How the product/service addresses the problem:
            1.
            2.
            3.
            ...
            n.                                                             

        Key features
            1. Feature 1
            2. Feature 2
            3. Feature 3
            ...                                                         
            n. Feature n                                                                                                                                                                            
                                                                      
        Benefits
            1. Benefit 1
            2. Benefit 2
            3. Benefit 3
            ...                                                         
            n. Benefit n                                                               

    Target Audience:

        Customer segments
            1.
            2.
            3.
            ...
            n.   
                                                                                                                                                                                                                                                                                                         
        Buyer personas
            1.
            2.
            3.
            ...
            n. 
                                                                      
        Customer demographics and psychographics
            1.
            2.
            3.
            ...
            n. 
                                                                      
        How the product meets their needs
            1.
            2.
            3.
            ...
            n. 
        """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="{question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt= ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain_info = LLMChain(llm=llm1, prompt=chat_prompt)
    res_web = chain_info.invoke({"question": f"""Website scrap: {comp_info}

    From the above information, extract the brief description of the business and existing and probable problems in the product."""})
   
    st.write(f"# Company info: \n\n{res_web['text']}")
   
    
    # template_search= """Blog idea: {idea}
    # {seo}\n
    # {ins}\n

    # Based on the given context, what additional information do you require to generate a blog serving B2B? 
    # Consider who this blog is for. What is the blog about? Is the topic relevant to them? What do they want to know about? 
    # What will resonate with them? What are ways to draw them away from well-established competition?
    # Generate 5 questions asking for the requirements in a chronological order. Output in a python list.
    # \n 
    # Output format:
    # ["","","","",""]
    # """
    # prompt_search = ChatPromptTemplate.from_template(template_search)
    # chain_search = LLMChain(llm=llm2, prompt=prompt_search)
    # res_search = chain_search.invoke({"idea": blog_title, "seo":seo, "ins":instruct})
    # ques = eval(res_search['text'])

    # template_answer= """Answer the following question comprehensively by your own knowledge. Give a real world answer. Include as many bullet points wherever necessary.
    # Question: {ques}
    # Answer:
    # """
    # prompt_answer = ChatPromptTemplate.from_template(template_answer)
    # chain_answer = LLMChain(llm=llm2, prompt=prompt_answer)
    # answers = ""
    # for i in ques:
    #     res_answer = chain_answer.invoke({"ques": i})
    #     answers+=(f"{i}\n\nAnswer: {res_answer['text']}\n\n")
    # st.write(answers)
    template_ques = """Context: {con}\n
    Based on the above context, answer the following questions.
    Output format:
    Question: Who will be primary reader (subscriber) of your blog? 
    \nAnswer:
    Question: What do you want to tell him or her? (What’s your story?)
    \nAnswer: 
    Question: Do you understand the key informational needs of that person? 
    \nAnswer: 
    Question: What are customers pain points? 
    \nAnswer: 
    Question: Where your customers hanging out online?
    \nAnswer: 
    Question: What is the target hit list of blogs or sites that your customers frequent online? 
    \nAnswer: 
    Question: Who are the competitors in the space? 
    \nAnswer: 
    Question: What types of keywords are customers searching for? (See Google’s Keyword Tool.)
    \nAnswer:  
    Question: Are there other relevant keywords on Google Alerts or Twitter your customers are following? (Do so to find the influencers in your market.) 
    \nAnswer: 
    Question: What is your ultimate goal in starting a blog?
    \nAnswer: 
    Question: One year after you start blogging, how will the business be different? 
    \nAnswer: 
    Question: How will the execution process work within your company and how will you market the blog? 
    \nAnswer: 
    Question: How will you integrate the blog with the rest of your marketing? 
    \nAnswer: 
    Question: How can the blog make everything else you are doing better?
    \nAnswer: 
    """
    prompt_ques = ChatPromptTemplate.from_template(template_ques)
    chain_ques = LLMChain(llm=llm1, prompt=prompt_ques)
    ques_out = chain_ques.invoke({"con": res_web['text']})
    st.info(ques_out["text"])
    # template_search= """Blog idea: {idea}
    
    # What is the relevant information present in the above given blog idea which can be used to suggest blog titles?
    # What additional information do you require to generate blog titles? Ask as many questions as needed (atleast 3-5). Keep the requirements short and to the point. Give 3 probable answers for the requirements from your own knowledge.
    # \n
    # Output format (give as many points under each heading as it is necessary):
    # ### Information present:
    # 1.
    # 2.
    # 3.
    # ...
    # n.

    # ### Additional information required:
    # 1.
    # \nProbable answers:
    # -
    # -
    # -

    # 2.
    # \nProbable answers:
    # -
    # -
    # -
    
    # 3.
    # \nProbable answers:
    # -
    # -
    # -

    # 4.
    # \nProbable answers:
    # -
    # -
    # -
    # ...

    # n.
    # \nProbable answers:
    # -
    # -
    # -
    # """
    # prompt_search = ChatPromptTemplate.from_template(template_search)
    # chain_search = LLMChain(llm=llm1, prompt=prompt_search)
    # res_search = chain_search.invoke({"idea": user_input, "seo":seo, "ins":instruc})
    # st.write(res_search['text'])
    template = """You are an expert Blog Writer. Your expertise spans across various industries. 
    Given a topic and a context, consider all the variations, sub topics, keywords, questions that people search for related to this topic. 
    Generate a list of 40 keywords closely related to the topic without duplicating any words. 
    Provide a list of potential long-tail keywords for the topic that could be used to optimize SEO.
    Consider emotional, technical, psychological aspects related to the topic.
    Iterate on sub topics to find unique and interesting variations. 
    Do not use buzz words. Ban generic words such as "unveil, unlock, unleash, understand". 
    Do not use the actual topic name itself in every variation.


    Your goal is to grab reader's attention, generate curiosity, generate interest in the solution, evoke desire for its benefits, and prompt action just with the title of the blog. 
    Use all the variations, keywords, long tail keywords to create 5 creative titles under each of the following categories to draw readers into the topic without duplicating the primary topic name:
    Keep the titles punchy, curious, engaging, short and distinctly unique.
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
    

    Also, suggest a few, very short SEO keywords for the blog idea. 

    Blog idea: {idea}
    Context: {con}

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
    12. *Case Study Post*
        -
        -
        -
        -
        -

    \n
    ## SEO keywords:
    -
    -
    -
    -
    -
    -

    Don't print blog idea.
    """
    #st.header("Prompt")
    
        
    prompt = ChatPromptTemplate.from_template(template)
    chain1 = LLMChain(llm=llm1, prompt=prompt)
    res = chain1.invoke({"idea": user_input, "con": ques_out['text']})
    five_sim = res['text']
    st.header("Suggested blog titles:")
    st.write(five_sim)