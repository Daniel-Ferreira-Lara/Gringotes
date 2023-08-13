import streamlit as st
stsst = st.session_state
#langchain bibliotecas
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
#biblioteca transformers do Pytorch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


#Funções para manter recursos e dados a aplicação em cache
@st.cache_resource(show_spinner=False)
def load_model_bank():
    model_id = 'philschmid/BERT-Banking77'
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id)
    classifier = pipeline('text-classification', tokenizer=tokenizer, model=model)
    return classifier

@st.cache_resource(show_spinner=False)
def load_model_gpt():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

@st.cache_resource(show_spinner=False)
def load_bd():
    db = SQLDatabase.from_uri("sqlite:///Database/Bank.db")
    llm = OpenAI(temperature=0, verbose=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    db_chainDirect = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=True) #Returns the query without passing through the LLM
    return db_chain, db_chainDirect


# Convertendo secrets do deploy na Key do google Cloud API
from google.cloud import translate_v2 as translate
@st.cache_resource(show_spinner=False)
def googleSecret():
    json_data = {
    "type": st.secrets.google.type,
    "project_id": st.secrets.google.project_id,
    "private_key_id": st.secrets.google.private_key_id,
    "private_key": st.secrets.google.private_key,
    "client_email": st.secrets.google.client_email,
    "client_id": st.secrets.google.client_id,
    "auth_uri": st.secrets.google.auth_uri,
    "token_uri": st.secrets.google.token_uri,
    "auth_provider_x509_cert_url": st.secrets.google.auth_provider_x509_cert_url,
    "client_x509_cert_url": st.secrets.google.client_x509_cert_url,
    "universe_domain": st.secrets.google.universe_domain
    }
    return translate.Client.from_service_account_info(json_data)