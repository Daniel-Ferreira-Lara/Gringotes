from Alice import *
from Integration import *

def main():
    global var
    var = 0

    #inicializa a classe Alice_service
    alice = Alice_service()
    flag = False
    while True:
        user_input = " "
        #intrdução do atendimento     
        if var == 0:
            orientacao = "Apresente-se e pergunte como pode ajudar o cliente"
        #não identificação do usuário
        elif var == 1984:
            orientacao = "Diga que não entendeu, e peça mais detalhes"
            var = 0
        #retorno
        else:
            orientacao = "pergunte se pode ajudar o usuário em mais alguma coisa?"
            flag = True

        #turno da alice receber o input e orientacao para seguir
        alice_output = alice.atendimento(user_input,orientacao)
        print("\n alice turn =>",alice_output) 
        alice.alice_step(alice_output)

        user_input = input("\nUser Input  => ")
        
        if var!=0:
            orientacao = "Voce perguntou se o usuario quer mais ajuda.verifique se a resposta dele:{input} ele quer mais ajuda ou não.Se sim diga apenas sim. Se não diga apenas não"
            alice_output = alice.atendimento(user_input,orientacao)
            alice.alice_step(alice_output)
            if alice_output == "não":
                orientacao = "dispeça e diga que o Banco Gringottes agradece pelo contato. Não diga mais nada além disso!"
                alice_output = alice.atendimento(user_input,orientacao)
                print("\n alice turn =>",alice_output) 
                break
        if flag == False:
            alice.exit(user_input)
        flag = False
        label = analyzer(user_input)

        #entramos no ciclo de atendimento
        if label == "card_arrival":
            #1
            orientacao = "responda ao {input} pedindo o número da conta do cliente no final "
            #SCRIPT 1
            while True:           
                #sinaliza fim do turno humano e guarda no historico
                alice.human_step(user_input)
                
                #turno da alice receber o input e orientacao para seguir
                alice_output = alice.atendimento(user_input,orientacao)
                if var ==3:
                    #subsitui o código de rastreio da string pelo código real que não poderia ter sido passado para o servidor da OpenAI
                    alice_output = alice_output.replace("[CÓDIGO DE RASTREIO]", alice.codRast)
                    var = var + 1
                #sinaliza fim do turno da atendente e guarda no historico
                alice.alice_step(alice_output)
                print("\n alice turn =>",alice_output)           
                #turno humano
                if var == 0 or var == 1:
                    user_input = input("\nUser Input => ")
                    alice.exit(user_input)
                if var == 4:
                    break                                     
                orientacao,var = alice.select_card_arrival(user_input,var)                    
        else:
            orientacao = "Diga somente que você sabe que o assunto é {input}, mas você ainda não pode solucionar o problema. Diga somente isso"
            alice_output = alice.atendimento(label,orientacao)
            print("\n alice turn =>",alice_output)

main()