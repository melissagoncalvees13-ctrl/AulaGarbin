
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Saúde — Dengue",
    layout="wide"
)

# Título e descrição
st.title("Dashboard de Saúde Pública: Dengue no Brasil")

st.write(
    "Este dashboard analisa a evolução dos casos prováveis "
    "de dengue no Brasil entre 2000 e 2023, usando uma série "
    "histórica do Ministério da Saúde."
)

st.caption(
    "Fonte: Ministério da Saúde — Série histórica de casos "
    "prováveis de dengue (2000–2023)."
)

# Carrega o CSV automaticamente
try:
    df = pd.read_csv("dengue_brasil_2000_2023-1.csv")
except FileNotFoundError:
    st.error(
        "O arquivo dengue_brasil_2000_2023.csv não foi encontrado. "
        "Coloque-o na mesma pasta do dashboard.py."
    )
    st.stop()

# Confere as colunas necessárias
necessarias = {"ano", "casos_provaveis"}

if not necessarias.issubset(df.columns):
    st.error(
        "O CSV precisa conter as colunas "
        "'ano' e 'casos_provaveis'."
    )
    st.stop()

# Limpeza dos dados
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
df["casos_provaveis"] = pd.to_numeric(
    df["casos_provaveis"], errors="coerce"
)

df = df.dropna(
    subset=["ano", "casos_provaveis"]
).copy()

df = df[
    (df["ano"] > 0) &
    (df["casos_provaveis"] >= 0)
]

df["ano"] = df["ano"].astype(int)
df = df.drop_duplicates()
df = df.sort_values("ano")

if df.empty:
    st.warning("Não há dados válidos para mostrar.")
    st.stop()

# Indicadores gerais
total = int(df["casos_provaveis"].sum())

indice_pico = df["casos_provaveis"].idxmax()
ano_pico = int(df.loc[indice_pico, "ano"])
maior_valor = int(df.loc[indice_pico, "casos_provaveis"])

st.subheader("Indicadores gerais")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total somado no período",
    f"{total:,}".replace(",", ".")
)

c2.metric(
    "Ano com mais casos",
    str(ano_pico)
)

c3.metric(
    "Maior número anual",
    f"{maior_valor:,}".replace(",", ".")
)

# Gráfico de linhas
st.subheader(
    "1. Como os casos prováveis mudaram ao longo dos anos?"
)

fig_linha = px.line(
    df,
    x="ano",
    y="casos_provaveis",
    markers=True,
    title="Casos prováveis de dengue por ano",
    labels={
        "ano": "Ano",
        "casos_provaveis": "Casos prováveis"
    }
)

st.plotly_chart(
    fig_linha,
    use_container_width=True
)

st.write(
    "O gráfico de linhas permite observar os anos de aumento "
    "e diminuição dos casos. Ele mostra a evolução dos registros, "
    "mas não explica sozinho as causas dessas mudanças."
)

# Gráfico de barras
st.subheader(
    "2. Quais anos tiveram os maiores números de casos?"
)

top_anos = df.nlargest(
    min(10, len(df)),
    "casos_provaveis"
).sort_values("casos_provaveis")

fig_barras = px.bar(
    top_anos,
    x="casos_provaveis",
    y="ano",
    orientation="h",
    title="Até 10 anos com mais casos prováveis",
    labels={
        "ano": "Ano",
        "casos_provaveis": "Casos prováveis"
    }
)

st.plotly_chart(
    fig_barras,
    use_container_width=True
)

st.write(
    f"Na base utilizada, o maior valor anual foi de "
    f"{maior_valor:,} casos prováveis, registrado em {ano_pico}."
    .replace(",", ".")
)

# Tabela dos dados
st.subheader("Dados utilizados")

st.dataframe(
    df,
    use_container_width=True
)
