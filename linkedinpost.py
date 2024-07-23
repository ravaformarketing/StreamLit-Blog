import random
import re
import json
import csv

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
llm1  = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, max_tokens=4096)

def generate_linkedin_prompt(topic, viral_posts):
    prompt = f"""Create a LinkedIn post that challenges a common misconception about {topic}. The post should:

1. Start with a bold, attention-grabbing statement that contradicts conventional wisdom about {topic}.
2. Use data or statistics to support your argument.
3. Share a personal anecdote or experience related to {topic}.
4. Provide actionable advice or insights for readers about {topic}.
5. End with a thought-provoking question to encourage engagement.
6. Include relevant hashtags to increase visibility.
7. Use formatting techniques like bullet points, emojis, and line breaks to improve readability.
8. Keep the initial visible portion of the post (before 'See more') intriguing to encourage expansion.

Include elements that often contribute to virality, such as:
- Emotional triggers (e.g., surprise, curiosity, inspiration)
- Relatable content that resonates with a wide audience
- Timely or trending aspects of {topic}
- Controversial or debate-sparking ideas about {topic}
- Valuable insights or 'insider' information about {topic}
- Storytelling techniques
- Calls-to-action that encourage sharing or commenting

Aim for a post length of 1300-1500 characters, which is optimal for LinkedIn engagement. 
Some sample viral posts for reference are here: {viral_posts}
Craft the post in a way that showcases authenticity and expertise in {topic}."""
    
    return prompt


# Load viral posts from a CSV file
def load_viral_posts_from_csv(filename):
    posts = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            posts.append(row[2])
    return posts

# Example usage
if __name__ == "__main__":
    topic = "artificial intelligence"
    try:
        viral_posts = load_viral_posts_from_csv('LinkedInPosts.csv')
    except FileNotFoundError:
        print("Error: viral_posts.csv file not found. Please create this file with your viral posts.")
        exit(1)

    template = generate_linkedin_prompt(topic, viral_posts)
    prompt = ChatPromptTemplate.from_template(template)
   
    chain1 = LLMChain(llm=llm1, prompt=prompt)
    linkedinpost = chain1.invoke(prompt)
    st.header("Suggested LinkedIn post:")
    st.write(linkedinpost)