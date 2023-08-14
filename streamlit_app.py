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