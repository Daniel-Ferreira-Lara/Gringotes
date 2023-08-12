# Gringotes
Repositório destinado ao sistema de match automático com chat bot de atendimento

## Contexto
Os chatbots inseridos no contexto de atendimento são ferramentas utilizadas com o intuito de acelerar e automatizar respostas a requisições feitas pelos clientes ou usuários. Eles podem ser envolvidos em diferentes contextos, como  plataformas de prestação de serviço, comércio, bancário e inúmeras outras situações em que as solicitações são constantes. Contudo, um problema vital nesse nicho é que o atendimento muitas vezes não é humanizado e não possui capacidade de generalização, ou seja, o chat se perde quando a solicitação foge do escopo que está programado a fazer.

## Objetivo
Nesse contexto, propomos o desenvolvimento de uma solução para atendimento bancário, no qual temos uma atendente capaz de receber requisições de usuários e identificar com precisão sua demanda para seguir com um script de atendimento captando e exibindo informações de maneira segura(em um contexto bancário é necessário levar em conta a sensibilidade das informações). Enquanto tudo isso ocorre, a atendente desenvolve o diálogo utilizando lingaugem natural.

## Tecnologias utilizaddas
- OpenAI API : precisávamos de um modelo de LLM para realizar o processamento de linguagem natural, optamos pelo próprio GPT pela praticidade e para que conseguíssemos nos concentrar na aplicação. Contudo o uso de um modelo open-source é com certeza um objetivo para trabalhos futuros.
- Python : pela praticidade e diversidade de recursos dispoíveis para integrações de ferramentas, foi a linguagem base do modelo.
- Hugging Face : utilizamos o modelo pré-treinado BERT-Banking77 para garantir acertividade no match automático. O modelo de classificação de texto utiliza os dados do banco Banking77 que apresenta 10k solicitações de usuários e suas respectivas classificações.
- Google Cloud Translate : Utilizamos a API pois os recursos que utlizamos (modelo e banco) estão em inglês e precisávamos de uma tradução precisa para pré e pós processamento de inputs e outputs.
- Langchain: Ferramenta que propõe a solução de algumas das limitações do GPT, ou melhor dizendo, acrescenta funcionalidades extras como a possibilidade de busca em um database específico, templates que oferecem contexto para o modelo atuar, ferramentas de buscas online, entre outras funcionalidades incríveis.
- biblioteca transformers : biblioteca proviniente da Pytorch é resposável pela integração do modelo com o nosso classificador.
- SQL: o Langchain oferece suporte para consultas SQL inteligentes no qual usamos para gerenciar os dados do banco, além disso com ela podemos definir o que vai ou não vai passar pelos servidores da OpenAI.
- Streamlit: é uma ferramenta prática para desenvolvimento rápido de interfaces voltadas para chatbots.
  
## Installação

#### 1. Clone the repository

```bash
git clone https://github.com/iRyanRib/Gringotes.git
```

#### 2. Criando ambiente Python

Python 3.10 ou acima usando `venv` :

``` bash
cd Gringotes
python3 -m venv env
source env/bin/activate
```
#### 3. Intallando as dependências
``` bash
pip install -r requirements.txt
```

#### 4. Set up the keys in a .env file

Crie `.env` no diretório principal do projeto. Dentro do arquivo, adcione sua OpenAI API key:

```makefile
OPENAI_API_KEY="your_api_key_here"
```
###5. configurando arquivo JSON google cloud
Vá para google cloud console :https://console.cloud.google.com/
selecione seu projeto, vá para:
"APIs & Services" > "Credentials".
clique em  "Create credentials" e selecione "Service Account Key".
preencha as informações necessárias e crie a chave no formato JSON.

tenha certeza que ela contém os campos necessários:
type, project_id, private_key_id, private_key, client_email, client_id, auth_uri, token_uri, auth_provider_x509_cert_url, client_x509_cert_url.

Em seu código, verifique se você está fornecendo o caminho correto para o arquivo de chave JSON.  O caminho deve ser absoluto ou relativo ao local do script.  Verifique novamente o caminho para se certificar de que é preciso.
por exemplo:
```python
#iniciando o  Google Cloud Translation API client
client = translate.Client.from_service_account_json('quick-discovery-395419-3351469312d3.json')
```
Depois de confirmar que seu arquivo de chave JSON tem os campos obrigatórios e o caminho está correto, tente executar o código novamente usando a chave JSON válida.

salve e feche o arquivo. No seu terminal rode o código principal:
```python
python3 Alice.py
```
obs: Alice no momento desse lançamento está habilitada para atender as solicitações de problemas envolvendo "chegada de cartão", ou seja, "quando meu cartão chega", "meu cartão ainda não veio", "a entrega do meu cartão está atrasada". Planejamos em trabalhos futuros cobrir as 77 classes disponíveis no banco.
