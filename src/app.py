import json
import streamlit as st
import pandas as pd
import requests

# ====== Configuração ======
OLLAMA_URL = "http://localhostxxxxx/api/generate" #colocar o número da porta
MODELO = 'gemma2:2b'

# ===== Carregando dados ========

transacoes = pd.read_csv('./data/transacoes.csv')

historico = pd.read_csv('./data/historico_atendimento.csv')

with open('./data/perfil_investidor.json', encoding='utf-8') as f:
    perfil = json.load(f)

with open('./data/produtos_financeiros.json', encoding='utf-8') as f:
    produtos = json.load(f)

# ====== Montar contexto ======

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍNEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ====== System Prompt ======
SYSTEM_PROMPT = """Você é a Nina, uma analista de perfil do investidor e educadora financeiro amigável e didático.

OBJETIVO:
Definir o perfil do investidor, indicar os investimentos mais adequados de acordo com o perfil identificado e ensinar conceitos de finanças pessoais de forma simples, utilizando os dados do cliente como exemplos práticos.

REGRAS:
- Sempre baseie suas respostas nos dados fornecidos
- Nunca invente informações financeiras
- Se não souber algo, admita e ofereça alternativas
- Não faça recomendações diretas de investimento.
- Não garanta rentabilidade ou resultados futuros.
- Não realize previsões de mercado.
- Sempre incentive o usuário a estudar antes de investir.
- Não substitua orientação profissional certificada.
- Seja paciente, imparcial e não julgadora.
- Faça perguntas quando necessário para definir o perfil.
- Responda apenas sobre temas relacionados a educação financeira.
- Caso o usuário peça análise de um ativo específico (ex: 'Devo comprar ação X?'), explique que não realiza recomendações individuais.
- Responda de forma concisa e direta, em no máximo 3 parágrafos.
"""

# ====== Chamar Ollama =====
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    if r.status_code != 200:
        return f"Erro na requisição: {r.status_code} - {r.text}"
    
    response_data = r.json()
    if 'response' in response_data:
        return response_data['response']
    elif 'error' in response_data:
        return f"Erro do Ollama: {response_data['error']}"
    else:
        return f"Resposta inesperada: {response_data}"

# ====== Interface ======
st.title("Nina, sua analista de perfil de investidor e educadora financeiro ;)")

if pergunta := st.chat_input("Sua dúvida sobre finanças"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))

