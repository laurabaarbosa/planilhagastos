import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
import random
import io



st.title("📊 Análise de Despesas Pessoais")


def gerar_dados_teste():
    categorias = ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", "Outros"]
    descricoes = ["Compra", "Viagem", "Cinema", "Remédio", "Restaurante", "Uber", "Livros"]
    data_inicial = datetime(2024, 1, 1)
    dados = []

    for _ in range(100):
        data = data_inicial + timedelta(days=random.randint(0, 150))
        valor = round(random.uniform(10, 500), 2)
        categoria = random.choice(categorias)
        descricao = random.choice(descricoes)
        dados.append([data.strftime("%Y-%m-%d"), valor, categoria, descricao])

    df = pd.DataFrame(dados, columns=["Data", "Valor", "Categoria", "Descrição"])
    return df


st.sidebar.header("📁 Carregar Dados")
usar_teste = st.sidebar.checkbox("Usar arquivo de teste")

if usar_teste:
    df = gerar_dados_teste()
else:
    arquivo = st.sidebar.file_uploader("Envie seu arquivo CSV", type=["csv"])
    if arquivo:
        df = pd.read_csv(arquivo)
    else:
        st.warning("Faça o upload de um arquivo CSV ou marque a opção de teste.")
        st.stop()


df['Data'] = pd.to_datetime(df['Data'])
df['Ano-Mes'] = df['Data'].dt.to_period('M')
df['Semana'] = df['Data'].dt.isocalendar().week

st.subheader("📄 Primeiras linhas dos dados")
st.dataframe(df.head())


st.subheader("📌 Total gasto por categoria")
gastos_categoria = df.groupby("Categoria")["Valor"].sum().sort_values(ascending=False)
st.dataframe(gastos_categoria)


st.subheader("💸 Maior gasto individual")
maior_gasto = df.loc[df["Valor"].idxmax()]
st.write(f"Data: {maior_gasto['Data'].date()}")
st.write(f"Valor: R$ {maior_gasto['Valor']:.2f}")
st.write(f"Categoria: {maior_gasto['Categoria']}")
st.write(f"Descrição: {maior_gasto['Descrição']}")


st.subheader("📅 Média mensal de gastos")
media_mensal = df.groupby("Ano-Mes")["Valor"].sum().mean()
st.write(f"Média mensal: R$ {media_mensal:.2f}")


st.subheader("⚠️ Comparação com limite de gasto")
limite = st.number_input("Defina um valor-limite (R$):", min_value=0.0, value=300.0)

alertas = df[df["Valor"] > limite]
st.write(f"Encontrados {len(alertas)} gastos acima do limite definido.")
st.dataframe(alertas)


st.subheader("📊 Gráfico de Pizza: Gastos por Categoria")
fig1, ax1 = plt.subplots()
ax1.pie(gastos_categoria, labels=gastos_categoria.index, autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
st.pyplot(fig1)


st.subheader("📈 Gráfico de Barras: Gastos Semanais")
gastos_semanais = df.groupby("Semana")["Valor"].sum()
fig2, ax2 = plt.subplots()
gastos_semanais.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Semana")
ax2.set_ylabel("Valor (R$)")
st.pyplot(fig2)
