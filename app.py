
import streamlit as st
from ping_utils import testar_ping, salvar_em_csv_e_excel, gerar_grafico, criar_pasta_resultados
from datetime import datetime
import pandas as pd
import os
import time

# Configurações da página
st.set_page_config(page_title="Monitor de Ping", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #007ACC;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📡 Monitor de Ping com Python")
st.markdown("Monitore conexões de rede e visualize resultados de forma prática e interativa.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    destinos_default = ["google.com", "cloudflare.com", "github.com", "8.8.8.8"]
    destinos_input = st.text_area("Destinos (um por linha):", "\n".join(destinos_default))
    destinos = [d.strip() for d in destinos_input.splitlines() if d.strip() != ""]
    pacotes = st.slider("Quantidade de pacotes", 1, 10, 4)
    iniciar = st.button("🚀 Iniciar Testes")

if iniciar:
    st.info("Iniciando testes de ping...")
    resultados = []
    pasta = criar_pasta_resultados()
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    progress_bar = st.progress(0)
    progresso = 0

    for i, destino in enumerate(destinos):
        resultado = testar_ping(destino, pacotes)
        if resultado:
            resultados.append(resultado)
            st.success(f"✅ {destino} — Média: {resultado['avg']} ms | Perda: {resultado['perda']}%")
        else:
            st.warning(f"❌ {destino} — falha na resposta")
        progresso = int((i + 1) / len(destinos) * 100)
        progress_bar.progress(progresso)
        time.sleep(0.3)

    if resultados:
        df = pd.DataFrame(resultados)
        st.subheader("📄 Tabela de Resultados")
        st.dataframe(df)

        csv, excel = salvar_em_csv_e_excel(resultados, pasta, data_hora)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Baixar CSV", data=open(csv, "rb"), file_name=os.path.basename(csv))
        with col2:
            st.download_button("⬇️ Baixar Excel", data=open(excel, "rb"), file_name=os.path.basename(excel))

        st.subheader("📊 Gráfico de Tempo Médio")
        grafico_path = gerar_grafico(resultados, pasta, data_hora)
        st.image(grafico_path, use_column_width=True)

    else:
        st.error("Nenhum resultado gerado.")
