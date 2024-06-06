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
    comp_url = st.text_input("Add URL", placeholder="Type or add URL of company", key='inputcompURL')
    # seo = st.text_input("SEO keywords", placeholder="Enter SEO keywords to optimize blog to", key='seoinp')
    # instruc = st.text_input("Instructions:", placeholder="Give some instructions", key='inst')
    #cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    submit_button = st.form_submit_button(label='Enter ➤')

if submit_button:
    
    llm1  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=4096)
    comp_info = scrape_from_url([f"{comp_url}"])
    comp_info = comp_info[0]
    system_template = f"""You are a social media strategist at a top digital marketing agency who creates comprehensive social media plans for clients.
    Rava AI should provide a similar social media plan that is relevant to this business. The social media plan should follow this structure:
        - Overview of client goals
        - Scope of work with Rava AI
        - Target audiences
        - Platform strategies (objectives, tactics, content plan for each platform) that are relevant to this target audience. The strategies could include Blog, Social Media, Emails, Webinars etc.
        - Measurement/KPIs
        - Build a table with a sample of initiatiaves, description, strategies to solve for this initiative, goals, metrics to measure success. 
        - Deliverables every month could include brand guidelines, Blog posts every week optimized for SEO, Social Media posts, Content Calendar
        - Outline all the digital marketing assets that might be relevant for this business along with a detailed description. This includes creating content assets like case studies, thought leadership pieces, and educational resources to showcase its expertise. Engaging website content, informative social media posts, and lead-generating webinars can attract potential customers.  Success stories, partnership announcements, and downloadable resources like ebooks and white papers can further solidify Rava's credibility and value proposition.
        - Scope of Work and Deliverables table that have 3 columns: Phase, its description along with the deliverables. More information on the format below:
                Discovery - through a process of scraping your website, copilot asking relevant questions, the platform will gather all the information we need to have the best understanding of your business and goals. Deliverables could be company brief and brand guidelines. 
                Architecture - just like a building, social media content and design needs a solid blueprint. The platform will determine the best way to organize your marketing strategy and sketch out a rough outline. Deliverables could be business analysis. 
                Content - with a solid blueprint in place it will be your job to collect, organize, edit, and deliver to us content for each of our social media pieces as needed. The platform will work and train on the specific content you need.Deliverables could be content strategy and individual content pieces.
                Design - at the same time you are working on content our team will be creating comprehensive layouts showing possible design directions. Deliverables could be individual content pieces. 
                Launch - with all the necessary architecture, content, and design elements in hand we'll get started with creating your social media accounts and publishing your content.Deliverables could be fully mapped out content calendar.
        """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="{question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt= ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain_info = LLMChain(llm=llm1, prompt=chat_prompt)
    res_web = chain_info.invoke({"question": f"""Website scrap: {comp_info}

    Use the scraped company information to write a social media plan for this client that follows the structure above. Include goals, scope, target audiences, platform strategies, and measurement. Write it professionally as if presenting to the client."""})
   
    st.write(f"# Company info: \n\n{res_web['text']}")

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
    Context: {con}

    \n
    Output format:
    1. *List Post*
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
    res = chain1.invoke({"con": ques_out['text']})
    five_sim = res['text']
    st.header("Suggested blog titles:")
    st.write(five_sim)


   