import streamlit as st
from streamlit_lottie import st_lottie_spinner
from Integration import *
import requests
import time
from Alice import load_model_bank, load_model_gpt, load_bd, load_model_translate
def load_backend():
    load_model_bank()
    load_model_gpt()
    load_bd()
    load_model_translate()

def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

stsst = st.session_state


class Chat:
    def __init__(self):
        self.img_usuario = "https://raw.githubusercontent.com/Daniel-Ferreira-Lara/deploy_testing/master/static/usuario.png"
        self.img_alice = "https://raw.githubusercontent.com/Daniel-Ferreira-Lara/deploy_testing/master/static/alice.png"
        self.animation = load_lottieurl("https://lottie.host/a445a333-0671-41c0-9645-dfd7ac740bc9/tFEbhUzgo3.json")
        self.configura()
        self.chat = st.container()
        
    def configura(self):
        if not stsst.carregado:
            stsst.carregado = True
            with st_lottie_spinner(self.animation):
                load_backend()
                time.sleep(2)

        st.title("Assistente do Banco Gringotts")
        st.text("Conduzindo a Magia das Finanças, com Lucros Além da Imaginação")

    def escreve_resposta(self,input):
        if input != "":
            stsst.mensagens.append({"papel": "assistente", "conteudo": input})

            with st.chat_message("assistente",avatar=self.img_alice):
                message_placeholder = st.empty()
                respota = ""
                resposta_assistente = input
                for palavra in resposta_assistente.split():
                    respota += palavra + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(respota + "▌")
                message_placeholder.markdown(respota)

    def conversa(self):
        with self.chat:
            for msg in stsst.mensagens:
                imagem = self.img_usuario if(msg["papel"] == "usuario") else self.img_alice
                st.chat_message(msg["papel"],avatar = imagem).write(msg["conteudo"])

        if prompt:= self.chat.chat_input("Sua mensagem ",max_chars=2000,disabled=stsst.disable):
            stsst.mensagens.append({"papel": "usuario", "conteudo": prompt})
            self.chat.chat_message("usuario",avatar=self.img_usuario).markdown(prompt)           
            resposta_assistente = integrate(self,prompt)
            self.escreve_resposta(resposta_assistente)
