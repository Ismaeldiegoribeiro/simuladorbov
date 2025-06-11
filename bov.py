import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial
st.set_page_config(page_title="Simulador de Engorda de Bovinos", layout="wide")
# Carregar e exibir a logo
logo = Image.open("Logo_faz.png")  # ou o nome do seu arquivo
st.image(logo, width=100)  # ajuste a largura conforme desejar
st.title("🐂 Simulador Completo de Engorda de Bovinos")

# Sidebar com entradas
with st.sidebar:
    logo = Image.open("Logo_faz.png")
    st.image(logo, width=75)

    st.header("🔧 Parâmetros da Simulação")

    raca = st.selectbox("Raça", ["Nelore", "Angus", "Cruzado"])
    fase = st.radio("Fase de Produção", ["Pasto", "Confinamento"])

    quantidade_animais = st.number_input("Quantidade de Animais no Lote", min_value=1, value=30, step=1)
    preco_animal = st.number_input("Custo Inicial por Animal (R$)", 500.0, 5000.0, 1800.0, step=100.0)

    peso_inicial = st.number_input("Peso Inicial (kg)", min_value=100.0, max_value=500.0, value=180.0)
    gmd = st.number_input("Ganho Médio Diário (kg/dia)", min_value=0.3, max_value=2.0, value=0.6, step=0.1)
    dias = st.slider("Dias em Engorda", 30, 730, 270, step=30)

    tipo_suplemento = st.selectbox("Tipo de Suplemento", ["Sal mineral", "Proteinado", "Ração"])
    custo_suplemento_kg = st.number_input("Custo do Suplemento (R$/kg)", 0.0, 10.0, 2.0)
    consumo_suplemento_dia = st.number_input("Consumo Diário de Suplemento (kg)", 0.1, 10.0, 0.6)

    custo_diario_fixo = st.number_input("Custo Diário Fixo (R$/animal/dia)", 1.0, 50.0, 2.0)
    mortalidade = st.slider("Taxa de Mortalidade (%)", 0.0, 20.0, 5.0, step=0.1)
    preco_arroba = st.number_input("Preço da Arroba (R$/@)", 150.0, 400.0, 270.0)
    area_por_animal = st.number_input("Área Ocupada por Animal (ha)", 0.1, 5.0, 1.0)

# Cálculos por animal
peso_final = peso_inicial + gmd * dias
ganho_total = peso_final - peso_inicial
peso_em_arrobas = peso_final / 30

custo_suplemento_total = consumo_suplemento_dia * custo_suplemento_kg * dias
custo_manejo = custo_diario_fixo * dias
custo_total_por_animal = custo_suplemento_total + custo_manejo + preco_animal

receita_bruta = peso_em_arrobas * preco_arroba
lucro = receita_bruta - custo_total_por_animal
roi = (lucro / custo_total_por_animal) * 100 if custo_total_por_animal > 0 else 0
roi_mensalizado = ((1 + (roi / 100))**(1/(dias / 30)) - 1) * 100

# Ajuste para mortalidade
fator_mortalidade = (1 - (mortalidade / 100))
animais_vivos = quantidade_animais * fator_mortalidade

# Cálculos globais
receita_total = receita_bruta * animais_vivos
custo_total_lote = custo_total_por_animal * quantidade_animais
lucro_total = receita_total - custo_total_lote

# Resultados
st.subheader("📊 Resultados por Animal")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Peso Final", f"{peso_final:.1f} kg")
    st.metric("Arrobas", f"{peso_em_arrobas:.1f} @")
    st.metric("Ganho Total", f"{ganho_total:.1f} kg")
    
with col2:
    st.metric("Receita Bruta", f"R$ {receita_bruta:,.2f}")
    st.metric("Lucro Bruto", f"R$ {lucro:,.2f}")
    st.metric("ROI", f"{roi:.1f} %")

with col3:
    st.metric("Mortalidade Estimada", f"{mortalidade:.1f} %")
    st.metric("Custo Total/Animal", f"R$ {custo_total_por_animal:,.2f}")
    st.metric("ROI MÊS", f"{roi_mensalizado:.1f} %")
# st.metric("Área Total", f"{quantidade_animais * area_por_animal:.1f} ha")

st.divider()
st.subheader("📦 Resultados do Lote")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Animais Vivos", f"{animais_vivos:.1f}")
with col5:
    st.metric("Receita Total", f"R$ {receita_total:,.2f}")
with col6:
    st.metric("Lucro Total", f"R$ {lucro_total:,.2f}")

# Gráfico de peso
pesos = [peso_inicial + gmd * i for i in range(dias + 1)]
dias_lista = list(range(dias + 1))

fig, ax = plt.subplots()
ax.plot(dias_lista, pesos, label="Peso (kg)", color="green")
ax.set_title("Evolução do Peso do Animal")
ax.set_xlabel("Dias")
ax.set_ylabel("Peso (kg)")
ax.grid(True)
st.pyplot(fig)

# Rodapé
st.markdown("---")
st.caption("📘 Este simulador é uma ferramenta de apoio à decisão. Consulte um zootecnista ou veterinário para avaliação técnica.")
