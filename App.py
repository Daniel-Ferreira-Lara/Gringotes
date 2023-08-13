
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from re import sub
from typing import Dict, List, Any
from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from time import sleep
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from google.cloud import translate_v2 as translate


from Alice import Alice_service, analyzer
from Integration import *
from Streamlit_UI import Chat


def main():
    init_session_state()

    chat = Chat()
    alice = Alice_service()

    chat.conversa()

    #Verificação para Alice iniciar a conversação
    if  stsst.estado == "":
        stsst.estado = "apresentação"
        integrate(alice,chat,"")

main()