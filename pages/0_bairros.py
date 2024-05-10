import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go


def conectar_banco_de_dados():
    # Conectar ao banco de dados MySQL
    conn_mysql = mysql.connector.connect(
        host="189.17.195.66",
        port=41306,
        user="app",
        password="AppP3squIs@",
        database="app"
    )
    cursor_mysql = conn_mysql.cursor()

    # Recuperar dados da pesquisa
    cursor_mysql.execute("SELECT * FROM pesquisa")
    dados = cursor_mysql.fetchall()

    # Fechar conexão
    conn_mysql.close()

    return dados


def grafico_bairros(dados, candidatos_selecionados, figsize=(12, 5)):
    df = pd.DataFrame(dados)
    df_selected = df[df[12].isin(candidatos_selecionados)]
    bairros_counts = df_selected[4].value_counts().sort_index()

    # Criar um DataFrame com os dados dos bairros e o número de votos de cada candidato
    bairros_info = pd.DataFrame(index=bairros_counts.index)
    for candidato in candidatos_selecionados:
        bairros_info[candidato] = df_selected[df_selected[12] == candidato][4].value_counts()

    # Criar lista de barras para o gráfico Plotly
    bar_data = []
    for candidato in candidatos_selecionados:
        bar_data.append(go.Bar(
            x=bairros_info.index,
            y=bairros_info[candidato],
            name=candidato,
            hoverinfo='y+name'
        ))

    # Layout do gráfico
    layout = go.Layout(
        title='Distribuição por Bairros',
        xaxis=dict(title='Bairros'),
        yaxis=dict(title='Número de Participantes'),
        barmode='stack'
    )

    # Criar figura Plotly
    fig = go.Figure(data=bar_data, layout=layout)

    return fig


def main():
    # se houver conexão com o banco mostra os graficos se nao houver mostra a mensagem sem conexão
    if not conectar_banco_de_dados():
        st.error('Sem conexão com o banco de dados.')
        return
    else:
        st.set_page_config(
            page_title="Análise da Pesquisa de Intenção de Votos",
            page_icon=":bar_chart:",
            layout="wide",  # Layout amplo para usar todo o espaço horizontal
            initial_sidebar_state="expanded"  # Barra lateral inicialmente expandida
        )
        st.title('Análise da Pesquisa de Intenção de Votos')
        # tamanho da fonte do title
        st.markdown("""<style>.title {font-size:16px;}</style>""", unsafe_allow_html=True)

        # Conectar ao banco de dados e recuperar os dados da pesquisa
        dados = conectar_banco_de_dados()

        # Opções de candidatos
        candidatos = ['Luciana e Kadu', 'Dr. Paulo e Guará', 'Dr. Rafael e Juninho', 'Dr. Márcio e Magali']

        # # Filtro na barra lateral para selecionar os candidatos
        candidatos_selecionados = st.sidebar.multiselect('Selecione os Candidatos:', candidatos, default=candidatos)

        # Filtro na barra lateral para selecionar o total de participantes titulo em negrito e fonte maior
        st.sidebar.markdown('**Total Apurado:**', unsafe_allow_html=True)

        # Filtro na barra lateral para selecionar o total de participantes
        if len(candidatos_selecionados) > 0:
            total_participantes = 0
            for candidato in candidatos_selecionados:
                num_votos = len([dado for dado in dados if dado[12] == candidato])
                st.sidebar.write(f'**{candidato}= {num_votos}**', )
                # st.sidebar.write(f'**Total de Votos:** {num_votos}')
                total_participantes += num_votos

            st.sidebar.write(f'**Total de Participantes:** {total_participantes}')

        # Criar gráfico de bairros interativo com Plotly
        fig_bairros = grafico_bairros(dados, candidatos_selecionados)
        st.plotly_chart(fig_bairros)


if __name__ == "__main__":
    main()
