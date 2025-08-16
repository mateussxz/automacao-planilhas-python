import streamlit as st
import pandas as pd

st.set_page_config(page_title="Automação de Planilhas", layout="wide")
st.title("Automação de Planilhas - Remover Duplicatas")

st.markdown("""
Este app permite processar planilhas Excel, identificando contas duplicadas e mantendo apenas uma
            Algumas informações sensíveis devem ser censuradas antes de compartilhar.
""")

# Upload da planilha
uploaded_file = st.file_uploader("Escolha sua planilha Excel", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Planilha carregada com sucesso!")

        # Exibir quantidade de dados antes
        st.write(f"Numero de células antes do processamento: {df.size}")

        # Conta quantas vezes cada conta aparece
        df['count'] = df.groupby('Conta')['Conta'].transform('count')

        # Mantém apenas uma ocorrência de cada conta
        df_result = df.drop_duplicates(
            subset=['Conta']).drop(columns=['count'])

        # Exibir quantidade de dados depois
        st.write(f"Número de células após o processamento: {df_result.size}")

        st.write("Planilha processada com sucesso!")
        st.dataframe(df_result.head(10))  # Mostra as primeiras linhas

        # Botão para baixar resultado
        output_file = "planilha_processada.xlsx"
        df_result.to_excel(output_file, index=False)
        with open(output_file, "rb") as file:
            st.download_button(
                label="Baixar planilha processada",
                data=file,
                file_name=output_file,
                mine="application/vnd.openxlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a planilha: {e}")
