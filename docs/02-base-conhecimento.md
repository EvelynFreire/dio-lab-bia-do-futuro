# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Para que serve na Nina |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores e dar continuidade ao atendimento |
| `perfil_investidor.json` | JSON | Definir o perfil do investido e personalizar recomendações |
| `produtos_financeiros.json` | JSON | Conhecer os produtos recomendados para o tipo de perfil financeiro para que eles possam ser ensinados ao cliente. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didática. |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Como o objetivo é definir o perfil de investimento do cliente, a informação anterior foi removida da base de dados. Em seu lugar, foram incluídos os diferentes tipos de perfis de investidores, bem como os critérios utilizados para classificá-los. 

Essa adaptação permite que o agente identifique o perfil do usuário de forma estruturada, com base em características comportamentais, tolerância ao risco e horizonte de investimento.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades: inserir os dados diretamente no prompt (copiando e colando) ou carregar os arquivos por meio de código, conforme demonstrado no exemplo abaixo.

```
import pandas as pd
import json

transacoes = pd.read_csv('./data/transacoes.csv')

historico = pd.read_csv('./data/historico_atendimento.csv')

with open('./data/perfil_investidor.json', encoding='utf-8') as f:
    perfil = json.load(f)

with open('./data/produtos_financeiros.json', encoding='utf-8') as f:
    produtos = json.load(f)
```

### Como os dados são usados no prompt?

Para simplificar, podemos “injetar” os dados diretamente no prompt, garantindo que o agente tenha o máximo de contexto disponível. No entanto, em soluções mais robustas, o ideal é que essas informações sejam carregadas dinamicamente, como demonstrado anteriormente, permitindo maior flexibilidade, escalabilidade e facilidade de atualização do sistema.

```
DADOS DO CLIENTE E TIPOS DE PERFIS FINANCEIROS (data/perfil_investidor.json):
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}

{
  "Perfis de Investidores": [
    {
      "perfil": "Conservador",
      "caracteristicas": [
        "Prioriza segurança e preservação do capital",
        "Baixa tolerância a oscilações",
        "Prefere previsibilidade",
        "Foco em estabilidade"
      ],
      "comportamento": [
        "Desconforto com qualquer perda",
        "Tendência a resgatar investimento ao perceber queda"
      ],
      "horizonte_investimento": [
        "Curto a médio prazo",
        "Até 2 anos"
      ]
    },
    {
      "perfil": "Moderado",
      "caracteristicas": [
        "Busca equilíbrio entre segurança e rentabilidade",
        "Aceita oscilações moderadas",
        "Entende que risco pode gerar maior retorno"
      ],
      "comportamento": [
        "Tolera quedas moderadas",
        "Mantém investimento se acreditar no longo prazo"
      ],
      "horizonte_investimento": [
        "Médio a longo prazo",
        "De 2 a 5 anos"
      ]
    },
    {
    "Peril": "Arrojado",
    "caracteristicas": [
      "Alta tolerância ao risco",
      "Foco em crescimento patrimonial",
      "Confortável com volatilidade",
      "Visão de longo prazo"
    ],
    "comportamento": [
      "Entende quedas como parte do processo",
      "Mantém estratégia mesmo com oscilações"
    ],
    "horizonte_investimento": [
      "Longo prazo",
      "Mais de 5 anos"
    ]
    }
  ]
}

TRANSACOES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

PRODUTOS DISPONIVEIS PARA ENSINO (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]
```


---

## Exemplo de Contexto Montado

O exemplo de contexto apresentado abaixo baseia-se nos dados originais da base de conhecimento, mas os sintetiza, mantendo apenas as informações mais relevantes e, assim, otimizando o consumo de tokens.

Entretanto, é importante destacar que, mais do que economizar tokens, o fundamental é garantir que todas as informações realmente relevantes estejam disponíveis no contexto.

```
Dados do Cliente:
- Nome: João Silva
- Aceita riscos: False
- Objetivo: Completar a reserva de emergência e Juntar a entrada do apartamento,
- Reserva atual: R$ 15.000 (meta: R$ 50.000)

Últimas transações:
- Moradia: R$ 1.380
- Alimentação: R$ 570
- Transporte: R$ 295
- Saúde: R$ 188
- Lazer: R$ 55,90
- Total de saídas: R$ 2.488,90

Perfis de Investidores:
- "Conservador: Baixa tolerância ao risco
- Moderado: Médio tolerância ao risco
- Arrojado: Alta tolerância ao risco

Produtos disponíveis para sugerir e explicar:
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Multimercado (risco médio)
- Fundo de Ações (risco alto)
