import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go


def conectar_banco_de_dados():
    # Conectar ao banco de dados MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="pesquisa"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pesquisa")
        dados = cursor.fetchall()
        return dados
    except mysql.connector.Error as error:
        print("Erro ao conectar ao banco de dados: {}".format(error))


def criar_grafico_barras(dados, candidatos_selecionados):
    df = pd.DataFrame(dados)
    df_selected = df[df[12].isin(candidatos_selecionados)]
    bairros = df_selected[4].value_counts().sort_index()

    fig = go.Figure(data=[go.Bar(x=bairros.index, y=bairros.values, text=bairros.values, textposition='auto')])
    fig.update_layout(
        title='Distribuição por Bairros',
        xaxis_title='Bairros',
        yaxis_title='Número de Participantes',
    )

    return fig


def main():
    st.set_page_config(
        page_title="Análise da Pesquisa de Intenção de Votos",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title('Análise da Pesquisa de Intenção de Votos')

    dados = conectar_banco_de_dados()

    candidatos = ['Luciana e Kadu', 'Dr. Paulo e Guará', 'Dr. Rafael e Juninho', 'Dr. Márcio e Magali']
    candidatos_selecionados = st.sidebar.multiselect('Selecione os Candidatos:', candidatos, default=candidatos)

    if not dados:
        st.error('Sem conexão com o banco de dados.')
        return

    total_participantes = 0
    for candidato in candidatos_selecionados:
        num_votos = len([dado for dado in dados if dado[12] == candidato])
        st.sidebar.write(f'**{candidato}= {num_votos}**',)
        total_participantes += num_votos

    st.sidebar.write(f'**Total de Participantes:** {total_participantes}')

    fig_bairros = criar_grafico_barras(dados, candidatos_selecionados)
    st.plotly_chart(fig_bairros)


if __name__ == "__main__":
    main()
