############################################################################################################################
################  AGENTE.IA Coder - Desenvolvido durante o curso de Desenvolvimento de IA da DSA   #########################
############################################################################################################################
# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="AGENTE.AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "AGENTE.IA Coder", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    # Define o título da barra lateral
    st.title("🤖 AGENTE.IA Coder")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em programação Python para ajudar iniciantes.")
    
    # Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )
    st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <p>AGENTE.IA Coder - Desenvolvido durante o curso de Desenvolvimento de IA da DSA. ®Tailan</p>
        <p>Minhas redes sociais abaixo<p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
    )
    col_vazia_esq, col_central, col_vazia_dir = st.columns((1, 3, 1))
    with col_central:
        st.link_button("🐙 GitHub", "https://github.com/tailann", use_container_width=True)
        st.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/tailan-silva-2b2b79207/", use_container_width=True)
# Título principal do app
st.title("AGENTE.IA Coder")
title_alignment = """
<style>
/* O seletor h1 atua em st.title() */
h1 {
    text-align: center;
}
</style>
"""
st.markdown(title_alignment, unsafe_allow_html=True)

st.title("Assistente Pessoal de Programação Python 🐍")


st.markdown(
    "<p style='text-align: center; color: grey;'>Faça sua pergunta sobre a Linguagem Python e obtenha código, explicações e referências.</p>", 
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


client = None

if groq_api_key:
    
    try:
        
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                st.markdown(dsa_ai_resposta)
                
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>AGENTE.IA Coder - Desenvolvido durante o curso de Desenvolvimento de IA da DSA. ® Tailan</p>
    </div>
    """,
    unsafe_allow_html=True
)





