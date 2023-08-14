import streamlit as st
stsst = st.session_state
#langchain bibliotecas
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
#biblioteca transformers do Pytorch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
#biblioteca de tradução do google cloud
from google.cloud import translate_v2 as translate

from Alice import translate_english_to_portuguese, analyzer

def init_session_state():
    #elementos Alice_service
    if "orientacao" not in stsst:
        stsst.orientacao = ""
    if "history" not in stsst:
        stsst.history = []
    if "user_input" not in stsst:
        stsst.user_input = ""
    if "alice_output" not in stsst:
        stsst.alice_output = ""
    if "contaUsuario" not in stsst:
        stsst.contaUsuario = None
    if "codRast" not in stsst:
        stsst.codRast = ""
    
    #elementos Chat
    if "mensagens" not in stsst:
        stsst.mensagens = []
    if "carregado" not in stsst:
        stsst.carregado = False
    if "disable" not in stsst:
        stsst.disable = False

    #elementos integrate
    if "var" not in stsst:
        stsst.var = 0
    if "estado" not in stsst:
        stsst.estado = ""
    if "label" not in stsst:
        stsst.label = ""

    
def integrate(alice, chat, prompt:str):
    stsst.user_input = prompt
    if prompt != "":
        alice.human_step(prompt)
    if stsst.estado != "apresentação":
        alice_output = alice.exit(prompt)
        if alice_output != "CONTINUAR":
            stsst.estado = "fim"
            integrate(alice,chat,"")
            return ""
    
    match stsst.estado:
        
        case "apresentação":
            #chat.escreve_resposta(str(stsst.var))
            if stsst.var == 0:
                orientacao = estagios_geral[stsst.estado][0]
                stsst.var = 1
            else:
                orientacao = estagios_geral[stsst.estado][1]

            alice_output = alice.atendimento(prompt,orientacao)
            alice.alice_step(alice_output)
            chat.escreve_resposta(alice_output)
            stsst.estado = "introdução"
            return ""

        case "introdução":
            label = analyzer(prompt)
            stsst.label = label
            if label is None:
                orientacao = estagios_geral[stsst.estado]
                alice_output = alice.atendimento(prompt,orientacao)
                alice.alice_step(alice_output)
                stsst.estado = "introdução"
                return alice_output
            else:
                if label == "card_arrival":
                    stsst.estado = "card_arrival"
                else:
                    stsst.estado = "other"
                stsst.var = -1
                integrate(alice,chat,"")
                return ""
            
        case "repeat":
            if prompt != "":
                alice_output = alice.exit(prompt)
                if alice_output == "CONTINUAR":
                    stsst.estado = "apresentação"
                    stsst.var = 1
                    integrate(alice,chat,"")
                    return ""
                else:
                    stsst.estado = "fim"
                    
                integrate(alice,chat,"")
                return ""
            else:
                orientacao = estagios_geral[stsst.estado]
                alice_output = alice.atendimento(prompt,orientacao)
                alice.alice_step(alice_output)
                chat.escreve_resposta(alice_output)
                return ""
        case "card_arrival":
            #chat.escreve_resposta("Var = {}".format(var))
            if stsst.var == -1:
                orientacao = estagios_geral[stsst.estado]
                alice_output = alice.atendimento(prompt,orientacao)
                alice.alice_step(alice_output)
                chat.escreve_resposta(alice_output)
                stsst.var = 0
                return ""
            else:
                orientacao,stsst.var = alice.select_card_arrival(prompt,stsst.var)
                alice_output = alice.atendimento(prompt,orientacao)
                alice.alice_step(alice_output)
                if stsst.var == 2:
                    chat.escreve_resposta(alice_output)
                    integrate(alice,chat,"")
                elif stsst.var == 3:
                    alice_output = alice_output.replace("[CÓDIGO DE RASTREIO]", alice.codRast)
                    chat.escreve_resposta(alice_output)
                    stsst.estado = "fim"
                    integrate(alice,chat,"")
                else:
                    chat.escreve_resposta(alice_output)
                return ""

        case "other":
            orientacao = estagios_geral[stsst.estado]
            alice_output = alice.atendimento(translate_english_to_portuguese(stsst.label),orientacao)
            alice.alice_step(alice_output)
            chat.escreve_resposta(alice_output)
            stsst.estado = "repeat" 
            integrate(alice,chat,"")
            return ""
        
        case "fim":
            
            orientacao = estagios_geral[stsst.estado]
            alice_output = alice.atendimento(prompt,orientacao)
            alice.alice_step(alice_output)
            stsst.alice_output = alice_output
            chat.escreve_resposta(alice_output)
            stsst.disable = True
            st.experimental_rerun()

estagios_geral: dict = {
    'apresentação': ["Apresente-se e pergunte como pode ajudar o cliente", "Apenas pergunte em qual assunto pode ajudar o cliente novamente"],
    'introdução': "Diga que não entendeu, e peça mais detalhes",
    'card_arrival': "responda ao {input} pedindo o número da conta do cliente no final.",
    'repeat': "Pergunte se pode ajudar o usuário em mais algum assunto",
    'other': "Diga somente que você sabe que o assunto é {input}, mas você ainda não pode solucionar o problema sozinha ainda, diga para entrar em contato pessoalmente no banco. Diga somente isso",
    'fim': "Dispeça e diga que o Banco Gringottes agradece pelo contato. Não diga mais nada além disso!"
}