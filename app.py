import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data or initialize an empty DataFrame
try:
    dados = pd.read_csv("compras.csv")
except FileNotFoundError:
    dados = pd.DataFrame({"PRODUTO": [], "PRECO": []})
    dados.to_csv("compras.csv", index=False)

# Streamlit app title
st.title("Controle de Gastos")

# Input for budget
orcamento = st.number_input("Orçamento:", min_value=0.0, format="%.2f")

# Calculate total spent
total = dados["PRECO"].sum() if not dados.empty else 0.0

# Form for adding a new purchase
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0, format="%.2f")
    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"PRODUTO": [produto], "PRECO": [preco]})
            dados = pd.concat([dados, nova_linha], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
            total = dados["PRECO"].sum()
        else:
            st.error("Sem orçamento suficiente!")

# Display budget breakdown if budget > 0
if orcamento > 0:
    # Donut chart
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["PRODUTO"].tolist()
        valores = dados["PRECO"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        plt.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        # Add center circle to create donut chart
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)
        plt.title(f"Orçamento: {orcamento}€")
    st.pyplot(fig)

# Display the data and summary
st.dataframe(dados)
st.write(f"Total gasto: {total:.2f}€")
st.write(f"Resta: {orcamento - total:.2f}€")
