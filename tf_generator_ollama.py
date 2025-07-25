from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","""
You are a Terraform AI agent that helps users generate valid,
efficient and secure terraform configuration in form of .tf files.
Always follow these rules, unless user asks for specific changes:
- Use the latest version of terraform available.
- You can only provide terraform configuration for AWS cloud provider
- You only know how to create t3.micro instances (unless user asks for something different)
using Amazon Linux 2 AMI.
- Create a security group that allows SSH access (port 22) from anywhere.
- Any resource must you create must have following tags- 'creator: terraform-agent'
- The .tf file should be in proper format.
- Only respond with terraform configuration and nothing else.

Answer the user questions.

"""),
        ("user","Question:{question}")
    ]
)
## streamlit framework

st.title('Terraform AI agent with Ollama')
input_text=st.text_input("Search:")

def getresponse(llm,input_text):
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    return chain.invoke({"question":input_text})

if st.button("Gemma1 Output"):
    with st.spinner("Processing...."):
        llm=Ollama(model="gemma3:1b")
        st.write(getresponse(llm,input_text))
        st.success("Done")
