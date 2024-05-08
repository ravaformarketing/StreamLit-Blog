import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
st.set_page_config(
    page_title="Blog Builder",
    page_icon="🖋️"
)
st.title("Blog Builder📝")
words = ""
# Accepting text input from the user
with st.form(key='my_form'):
    user_input = st.text_input("Blog idea", placeholder="Describe", key='input')
    seo = st.text_input("SEO keywords", placeholder="Enter SEO keywords to optimize blog to", key='seoinp')
    instruc = st.text_input("Instructions:", placeholder="Give some instructions", key='inst')
    
    #cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    submit_button = st.form_submit_button(label='Enter ➤')

if submit_button and user_input:
    
    llm1  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=4096)
    template_search= """Blog idea: {idea}
    {seo}\n
    {ins}\n
    Based on the given blog idea and context, what additional information do you require to generate a blog serving B2B? 
    Consider who this blog is for. What is the blog about? Is the topic relevant to them? What do they want to know about? 
    What will resonate with them? What are ways to draw them away from well-established competition?
    Generate 5 questions asking for the requirements in a chronological order. Output in a python list.
    \n 
    Output format:
    ["","","","",""]
    """
    prompt_search = ChatPromptTemplate.from_template(template_search)
    chain_search = LLMChain(llm=llm1, prompt=prompt_search)
    res_search = chain_search.invoke({"idea": user_input, "seo":seo, "ins":instruc})
    ques = eval(res_search['text'])

    template_answer= """Answer the following question comprehensively by your own knowledge. Give a real world answer. Include as many bullet points wherever necessary.
    Question: {ques}
    Answer:
    """
    prompt_answer = ChatPromptTemplate.from_template(template_answer)
    chain_answer = LLMChain(llm=llm1, prompt=prompt_answer)
    answers = ""
    for i in ques:
        res_answer = chain_answer.invoke({"ques": i})
        st.write(f"{i}\n\nAnswer: {res_answer['text']}\n\n")
        answers+=(f"{i}\n\nAnswer: {res_answer['text']}\n\n")

    template = """You are an expert Blog Writer. Your expertise spans across various industries. 
    Given a topic, consider all the variations, sub topics, keywords, questions that people search for related to this topic. 
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
        -{ins}
     

    Also, suggest a few, very short SEO keywords for the blog idea. 

    Blog idea: {idea}
    Context: {infos}

    \n
    Output format:
    1. **List Post**
        -
        -
        -
        -
        -
    2. **How-To Post**
        -
        -
        -
        -
        -
    3. **Problem/Solution Post**
        -
        -
        -
        -
        -
    4. **Checklist Post**
        -
        -
        -
        -
        -
    5. **The Ultimate Guide Post**
        -
        -
        -
        -
        -
    6. **Definition Post**
        -
        -
        -
        -
        -
    7. **Pillar Post**
        -
        -
        -
        -
        -
    8. **Tips Post**
        -
        -
        -
        -
        -
    9. **SAQ Post**
        -
        -
        -
        -
        -
    10. **Tools Post**
        -
        -
        -
        -
        -
    11. **Question Post**
        -
        -
        -
        -
        -
    12. **Case Study Post**
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
    
    if seo:
        template = """You are an expert Blog Writer. You will be given a blog idea and some SEO keywords.\n
        Given below are 12 types of blogs:

        1. List Post: A curated list of resources, books, tools and any other things that your audience will find useful.
        2. How-To Post: A step-by-step guide on how to complete a task.
        3. Problem/Solution Post: Identifies a problem and presents a solution.
        4. Checklist Post: A list of steps to complete a task.
        5. The Ultimate Guide Post: An in-depth and comprehensive guide on a topic.
        6. Definition Post: Explains a complex term or concept.
        7. Pillar Post: Serves as the foundation for other blog posts on a core topic.
        8. Tips Post: Offers practical advice or suggestions.
        9. SAQ Post: Asks a question your audience might not consider but should.
        10. Tools Post: Lists and reviews tools helpful to your audience.
        11. Question Post: Curate and answer questions your audience asks in social media, onforums, or in the comments section of your blog.
        12. Case Study Post: Analyzes a project or event to showcase results.

        Read through the given blog idea and suggest 5 creative, engaging titles that would draw readers in and accurately represent the idea.
        Generate 5 blog titles for each type of blog from the given idea including the given SEO keywords (hence, there will 60 titles in total). Keep the titles short and punchy. They should create curiosity.
        Based on the provided SEO keywords, suggest a few, very short more related but different SEO keywords.
        STRICTLY follow these rules while generating the titles:\n
            -Highlight only a FEW words (NOT THE WHOLE TITLE) in the title in quotations. Every title has to have a word which is in quotes.\n
            Example titles:\n
            One 'logical lie' that is talked about in almost every free blog post about 'Promoted Posts' that you absolutely DO NOT want to do\n
            The six step 'Cheat Sheet' that virtually guarantees your success\n

            In the above examples, I want the same format as 'logical lie' and 'Cheat Sheet' have been quoted.
            But only highlight the main words, not everytime. Certain titles might not even need highlighting.
            
            -Use numbers wherever necessary.\n
            Example title:\n
            How to turn $15 into 88,000 views with one simple mouse click\n

            -Capitalise certain words in the titles.

            -{ins}
        \n
        Blog title: {idea}
        SEO keywords: {seo}
        Context: {infos}
        \n
        Output format:
        1. **List Post**
            -
            -
            -
            -
            -
        2. **How-To Post**
            -
            -
            -
            -
            -
        3. **Problem/Solution Post**
            -
            -
            -
            -
            -
        4. **Checklist Post**
            -
            -
            -
            -
            -
        5. **The Ultimate Guide Post**
            -
            -
            -
            -
            -
        6. **Definition Post**
            -
            -
            -
            -
            -
        7. **Pillar Post**
            -
            -
            -
            -
            -
        8. **Tips Post**
            -
            -
            -
            -
            -
        9. **SAQ Post**
            -
            -
            -
            -
            -
        10. **Tools Post**
            -
            -
            -
            -
            -
        11. **Question Post**
            -
            -
            -
            -
            -
        12. **Case Study Post**
            -
            -
            -
            -
            -

        \n
        ## Suggested SEO keywords:
        -
        -
        -
        -
        -
        -
        -
        -

        Don't print blog idea and SEO keywords.
        """
        # st.write(f"""You are an expert Blog Writer. You will be given a blog idea and some SEO keywords.\n
        # Given below are 12 types of blogs:

        # 1. List Post: A curated list of resources, books, tools and any other things that your audience will find useful.
        # 2. How-To Post: A step-by-step guide on how to complete a task.
        # 3. Problem/Solution Post: Identifies a problem and presents a solution.
        # 4. Checklist Post: A list of steps to complete a task.
        # 5. The Ultimate Guide Post: An in-depth and comprehensive guide on a topic.
        # 6. Definition Post: Explains a complex term or concept.
        # 7. Pillar Post: Serves as the foundation for other blog posts on a core topic.
        # 8. Tips Post: Offers practical advice or suggestions.
        # 9. SAQ Post: Asks a question your audience might not consider but should.
        # 10. Tools Post: Lists and reviews tools helpful to your audience.
        # 11. Question Post: Curate and answer questions your audience asks in social media, onforums, or in the comments section of your blog.
        # 12. Case Study Post: Analyzes a project or event to showcase results.

        # Generate 5 blog titles for each type of blog from the given idea including the given SEO keywords (hence, there will 60 titles in total). Keep the titles succinct.
        # Based on the provided SEO keywords, suggest a few, very short more related but different SEO keywords.
        # Generate 5 blog titles for each type of blog from the given idea (hence, there will be 60 titles in total). Keep the titles succinct and professional.
        # STRICTLY follow these rules while generating the titles:\n
        #     -Highlight only a FEW words (NOT THE WHOLE TITLE) in the title in quotations. Every title has to have a word which is in quotes.\n
        #     Example titles:\n
        #     One 'logical lie' that is talked about in almost every free blog post about 'Promoted Posts' that you absolutely DO NOT want to do\n
        #     The six step 'Cheat Sheet' that virtually guarantees your success\n

        #     In the above examples, I want the same format as 'logical lie' and 'Cheat Sheet' have been quoted.
        #     But only highlight the main words, not everytime. Certain titles might not even need highlighting.
            
        #     -Use numbers wherever necessary.\n
        #     Example title:\n
        #     How to turn $15 into 88,000 views with one simple mouse click\n

        #     -Capitalise certain words in the titles.

        #     -{instruc}
        # \n
        # Blog title: {user_input}
        # SEO keywords: {seo}
        # \n
        # Output format:
        # 1. **List Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 2. **How-To Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 3. **Problem/Solution Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 4. **Checklist Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 5. **The Ultimate Guide Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 6. **Definition Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 7. **Pillar Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 8. **Tips Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 9. **SAQ Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 10. **Tools Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 11. **Question Post**
        #     -
        #     -
        #     -
        #     -
        #     -
        # 12. **Case Study Post**
        #     -
        #     -
        #     -
        #     -
        #     -

        # \n
        # ## Suggested SEO keywords:
        # -
        # -
        # -
        # -
        # -
        # -
        # -
        # -

        # Don't print blog idea and SEO keywords.
        # """)
    # else:
    #     st.write(f"""You are an expert Blog Writer. You will be given a blog idea.\n
    #     Given below are 12 types of blogs:

    #     1. List Post: A curated list of resources, books, tools and any other things that your audience will find useful.
    #     2. How-To Post: A step-by-step guide on how to complete a task.
    #     3. Problem/Solution Post: Identifies a problem and presents a solution.
    #     4. Checklist Post: A list of steps to complete a task.
    #     5. The Ultimate Guide Post: An in-depth and comprehensive guide on a topic.
    #     6. Definition Post: Explains a complex term or concept.
    #     7. Pillar Post: Serves as the foundation for other blog posts on a core topic.
    #     8. Tips Post: Offers practical advice or suggestions.
    #     9. SAQ Post: Asks a question your audience might not consider but should.
    #     10. Tools Post: Lists and reviews tools helpful to your audience.
    #     11. Question Post: Curate and answer questions youraudience asks in social media, onforums, or in the comments section of your blog.
    #     12. Case Study Post: Analyzes a project or event to showcase results.

    #     Generate 5 blog titles for each type of blog from the given idea (hence, there will be 60 titles in total). Keep the titles succinct and professional.
    #     STRICTLY follow these rules while generating the titles:\n
    #         -Highlight only one or two words (NOT THE WHOLE TITLE) in the title in quotations.\n
    #         Example titles:\n
    #         One 'logical lie' that is talked about in almost every free blog post about 'Promoted Posts' that you absolutely DO NOT want to do\n
    #         The six step 'Cheat Sheet' that virtually guarantees your success\n

    #         In the above examples, I want the same format as 'logical lie' and 'Cheat Sheet' have been quoted.
    #         But only highlight the main words, not everytime. Certain titles might not even need highlighting.
            
    #         -Use numbers wherever necessary.\n
    #         Example title:\n
    #         How to turn $15 into 88,000 views with one simple mouse click\n

    #         -Capitalise certain words in the titles.

    #         -{instruc}
        

    #     Also, suggest a few, very short SEO keywords for the blog idea. 

    #     Blog idea: {user_input}

    #     \n
    #     Output format:
    #     1. **List Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     2. **How-To Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     3. **Problem/Solution Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     4. **Checklist Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     5. **The Ultimate Guide Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     6. **Definition Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     7. **Pillar Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     8. **Tips Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     9. **SAQ Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     10. **Tools Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     11. **Question Post**
    #         -
    #         -
    #         -
    #         -
    #         -
    #     12. **Case Study Post**
    #         -
    #         -
    #         -
    #         -
    #         -

    #     \n
    #     ## SEO keywords:
    #     -
    #     -
    #     -
    #     -
    #     -
    #     -

    #     Don't print blog idea.
    #     """)
    prompt = ChatPromptTemplate.from_template(template)
    chain1 = LLMChain(llm=llm1, prompt=prompt)
    if seo:
        res = chain1.invoke({"idea": user_input, "seo": seo, "ins": instruc, "infos": answers})
    else:
        res = chain1.invoke({"idea": user_input, "ins": instruc, "infos": answers})
    five_sim = res['text']
    words = seo
    st.header("Suggested blog titles:")
    st.write(five_sim)

with st.form(key='my_form2'):
    blog_title = st.text_input("Blog title", placeholder="Enter Blog title", key='inputtitle')
    seok = st.text_input("SEO keywords", value = words, key='seoInp')
    cta = st.text_input("CTA", placeholder="What do you want the customer to do after reading your post?", key='ctainp')
    instruct = st.text_input("Instructions:", placeholder="Give some instructions", key='instr')
    brand = st.text_input("Brand voice:", placeholder="Describe brand voice", key="br")
    submit_button2 = st.form_submit_button(label='Enter ➤')

if submit_button2 and blog_title:
    llm2  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens = 4096)
    template_search= """Blog title: {idea}
    {seo}\n
    {ins}\n

    Based on the given blog title and context, what additional information do you require to generate a blog? Generate 5 questions asking for the requirements in a chronological order. Output in a python list.
    \n
    Output format:
    ["","","","",""]
    """
    prompt_search = ChatPromptTemplate.from_template(template_search)
    chain_search = LLMChain(llm=llm2, prompt=prompt_search)
    res_search = chain_search.invoke({"idea": blog_title, "seo":seok, "ins":instruct})
    ques = eval(res_search['text'])

    template_answer= """Answer the following question by our own knowledge. Give a real world answer. Include bullet points wherever necessary.
    Question: {ques}
    Answer:
    """
    prompt_answer = ChatPromptTemplate.from_template(template_answer)
    chain_answer = LLMChain(llm=llm2, prompt=prompt_answer)
    answers = ""
    for i in ques:
        res_answer = chain_answer.invoke({"ques": i})
        st.write(f"{i}\n\nAnswer: {res_answer['text']}\n\n")
        answers+=(f"{i}\n\nAnswer: {res_answer['text']}\n\n")
    
    template0 = """You are an expert Blog Writer. 
    Based on the given blog title and context about the title, suggest 5 alternate but similar blog titles.
    
    Blog title: {blog}
    Additional information: {infos}

    Output format:
    ## Alternate blog titles:
    1.
    2.
    3.
    4.
    5.
    """
    prompt0 = ChatPromptTemplate.from_template(template0)
    chain0 = LLMChain(llm=llm2, prompt=prompt0)
    alt = chain0.invoke({"blog":blog_title, "infos": answers})
    st.write(alt['text'])

    template_seo = """You are an expert Blog Writer. 
    Based on the given blog title, suggest 10 relevant SEO keywords.
    
    Blog title: {blog}
    Additional information: {infos}

    Output format:
    ## SEO keywords:
    "","","","","","","","","",""
    """
    prompt_seo = ChatPromptTemplate.from_template(template_seo)
    chain_seo = LLMChain(llm=llm2, prompt=prompt_seo)
    alt_seo = chain_seo.invoke({"blog":blog_title, "infos": answers})
    st.write(alt_seo['text'])
    template_cta = """You are an expert Blog Writer. 
    Based on the given blog title, suggest 5 relevant strategies for call to action.
    
    Blog title: {blog}
    Additional information: {infos}

    Output format:
    ## Suggested CTAs:
    -
    -
    -
    -
    -

    """
    prompt_cta = ChatPromptTemplate.from_template(template_cta)
    chain_cta = LLMChain(llm=llm2, prompt=prompt_cta)
    alt_cta = chain_cta.invoke({"blog":blog_title, "infos": answers})
    st.write(alt_cta['text'])
    if seok and cta:
        
        template2 = """You are an expert Blog Writer. 
        Determine a specific blog writer role (Food blog writer for obese people, Travel blog writer for Mountain lovers, etc.) based on the provided blog title, some SEO keywords and a call to action (CTA). 
        Assuming the role, create a 5-bullet outline based on the provided blog title, some SEO keywords and a call to action (CTA). 
        Each bullet point should be short and crisp (without explanation) represent a key subtopic or section that could be covered in the blog post. 
        Ensure that the outline is well-structured and outlines the main points of the blog post effectively.
        There should not be any sub-bullets in the outline. Only 5 main bullets.
        
        Blog title: {blog}
        SEO keywords: {seok}
        CTA (Call to action): {cta}
        Additional information: {infos}
        Output format:
        Role:

        ## Outline:
        1.
        2.
        3.
        4.
        5.
        """
        prompt2 = ChatPromptTemplate.from_template(template2)
        chain2 = LLMChain(llm=llm2, prompt=prompt2)
        outline = chain2.invoke({"blog":blog_title, "seok":seok, "cta":cta, "infos": answers})
        #st.write(outline['text'])
    elif seok:
        
        template2 = """You are an expert Blog Writer. 
        Determine a specific blog writer role (Food blog writer for obese people, Travel blog writer for Mountain lovers, etc.) based on the provided blog title and some SEO keywords.  
        Assuming the role, create a 5-bullet outline based on the provided blog title and some SEO keywords.
        Each bullet point should be short and crisp (without explanation) represent a key subtopic or section that could be covered in the blog post. 
        Ensure that the outline is well-structured and outlines the main points of the blog post effectively.
        There should not be any sub-bullets in the outline. Only 5 main bullets.

        Blog title: {blog}
        SEO keywords: {seok}
        Additional information: {infos}
        Output format:
        Role:

        ## Outline:
        1.
        2.
        3.
        4.
        5.
        """
        prompt2 = ChatPromptTemplate.from_template(template2)
        chain2 = LLMChain(llm=llm2, prompt=prompt2)
        outline = chain2.invoke({"blog":blog_title, "seok":seok, "infos": answers})
        #st.write(outline['text'])
    elif cta:
        
        template2 = """You are an expert Blog Writer. 
        Determine a specific blog writer role (Food blog writer for obese people, Travel blog writer for Mountain lovers, etc.) based on the provided blog title and a call to action (CTA). 
        Assuming the role, create a 5-bullet outline based on the provided blog title and a call to action (CTA). 
        Each bullet point should be short and crisp (without explanation) and represent a key subtopic or section that could be covered in the blog post. 
        Ensure that the outline is well-structured and outlines the main points of the blog post effectively.
        There should not be any sub-bullets in the outline. Only 5 main bullets.

        Blog title: {blog}
        CTA (Call to action): {cta}
        Additional information: {infos}
        Output format:
        Role:

        ## Outline:
        1.
        2.
        3.
        4.
        5.
        """
        prompt2 = ChatPromptTemplate.from_template(template2)
        chain2 = LLMChain(llm=llm2, prompt=prompt2)
        outline = chain2.invoke({"blog":blog_title,"cta":cta, "infos": answers})
        #st.write(outline['text'])
    else:
        
        template2 = """You are an expert Blog Writer. 
        Determine a specific blog writer role (Food blog writer for obese people, Travel blog writer for Mountain lovers, etc.) based on the provided blog title. 
        Assuming the role, create a 5-bullet outline based on the provided blog title.
        Each bullet point should be short and crisp (without explanation) and represent a key subtopic or section that could be covered in the blog post. 
        Ensure that the outline is well-structured and outlines the main points of the blog post effectively.
        There should not be any sub-bullets in the outline. Only 5 main bullets.

        Blog title: {blog}
        Additional information: {infos}
        Output format:
        Role:

        ## Outline:
        1.
        2.
        3.
        4.
        5.
        """
        prompt2 = ChatPromptTemplate.from_template(template2)
        chain2 = LLMChain(llm=llm2, prompt=prompt2)
        outline = chain2.invoke({"blog":blog_title, "infos": answers})
        #st.write(outline['text'])
    #st.subheader("Detailed outline")
    template3 = """You are an expert Blog Writer. 
    You will be given a blog title and it's outline along with additional context.
    Give me 5 relevant sub-topics under each point in the given outline. The outline has 5 points.
    Each subtopic should represent a key point that could be covered in the blog post. 
    Ensure that the sub-topics are well-structured and well-connected.

    Blog title: {blg}
    Outline: {out}
    Additional Context: {infos}
    Output format:
    1.
        -
        -
        -
        -
        -

    2.
        -
        -
        -
        -
        -
        
    3.
        -
        -
        -
        -
        -
        
    4.
        -
        -
        -
        -
        -
       
    5.
        -
        -
        -
        -
        -
        
    """
    prompt3 = ChatPromptTemplate.from_template(template3)
    chain3 = LLMChain(llm=llm2, prompt=prompt3)
    dets = chain3.invoke({"blg": blog_title,"out":outline['text'], "infos": answers})
    #st.write(dets['text'])
    # Find the index of the first occurrence of '\n'
    index_of_newline = outline['text'].find('\n')

    # Extract the substring from the beginning to the index of '\n'
    role = outline['text'][:index_of_newline]

    template_struct = """Given below are 12 types of blogs:
    1. List Post: A curated list of resources, books, tools and any other things that your audience will find useful.
    2. How-To Post: A step-by-step guide on how to complete a task.
    3. Problem/Solution Post: Identifies a problem and presents a solution.
    4. Checklist Post: A list of steps to complete a task.
    5. The Ultimate Guide Post: An in-depth and comprehensive guide on a topic.
    6. Definition Post: Explains a complex term or concept.
    7. Pillar Post: Serves as the foundation for other blog posts on a core topic.
    8. Tips Post: Offers practical advice or suggestions.
    9. SAQ Post: Asks a question your audience might not consider but should.
    10. Tools Post: Lists and reviews tools helpful to your audience.
    11. Question Post: Curate and answer questions youraudience asks in social media, onforums, or in the comments section of your blog.
    12. Case Study Post: Analyzes a project or event to showcase results.

    You are an expert blog writer. Classify the following blog title as one of the 12 above blog types and give a template needed to write that type of blog post of 10-15 sections on the given title. Don't number any bullets.\n
    
    Blog Title: {blog}\n

    Output format:
    
    Blog Type: 
    
    Template:
    
    """
    prompt_struct = ChatPromptTemplate.from_template(template_struct)
    chain_struct = LLMChain(llm=llm2, prompt=prompt_struct)
    blog_type = chain_struct.invoke({"blog": blog_title})
    system_template = f"""{role}\n
    Write a blog post based on the title: {blog_title}. 
    Your blog post should be informative, engaging, and well-structured. Provide valuable insights, examples, and any necessary research to support your points. 
   
    """
    st.write(f"### System prompt:\n{system_template}")
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template="{question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain4 = LLMChain(llm=llm2, prompt=chat_prompt)
    human_message = f"""
    \n\nBlog title: {blog_title}\n
    
    {blog_type['text']}\n

    Points to be covered: \n{dets['text']}\n\n

    Write a blog post in 10-15 sections following the steps mentioned above. 
    Use ### for headings.
    Your goal is to captivate readers with compelling content that offers unique perspectives, practical tips, and perhaps even personal anecdotes. 
    Dive deep into the topic, exploring different angles and providing actionable insights. 
    Keep the tone conversational yet informative, aiming to engage your audience throughout the entire piece. 
    Feel free to infuse your own voice and creativity into the writing.
    """
    
    if instruct:
        human_message = human_message + f"\nUse the following instructions to write the blog: {instruct}"
    if brand:
        human_message = human_message + f"\nWrite the blog in a brand voice whose characteristics are: {brand}"
    st.write(f"### Human Prompt:\n{human_message}")
    
    final_res = chain4.invoke({"question": human_message})
    st.header(blog_title)
    st.write(final_res['text'])