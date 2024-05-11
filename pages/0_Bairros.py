import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go

# Definir cores para cada candidato
cores = {'Luciana e Kadu': 'green',
         'Dr. Paulo e Guará': 'blue',
         'Dr. Rafael e Juninho': 'red',
         'Dr. Márcio e Magali': 'orange'}


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

    # Lista completa de todos os bairros
    todos_bairros = [
        'Aterrado', 'Bairro da Saúde', 'Banqueta', 'Barra do Peixe', 'Beira Rio', 'Bela Vista', 'Boiadeiro',
        'Campo Alegre', 'Centro', 'Esplanada', 'Fernando Lobo', 'Gauchão', 'Gironda', 'Goiabal',
        'Granja 3 de Outubro', 'Grota', 'Ilha Gama Cerqueira', 'Ilha Recreio', 'Ilha do Lazareto', 'Jaqueira',
        'Jardim Paraíso', 'Jardim Santa Rosa', 'Marinópolis', 'Matadouro', 'Morro do Cipó', 'Morro Trindade',
        'Morro São Sebastião', 'Morro São Geraldo', 'Morro dos Cabritos', 'Morro da Conceição', 'Parada Breves',
        'Porto Velho', 'Porto Novo', 'Praça da Bandeira', 'Remanso', 'São Geraldo', 'Santa Marta I', 'Santa Marta II',
        'Santa Rita', 'Sítio Branco', 'Terra do Santo', 'Terreirão', 'Timbira', 'Torrentes', 'Vila Laroca'
    ]

    # Criar um DataFrame vazio com todos os bairros como índices
    bairros_info = pd.DataFrame(index=todos_bairros)

    # Preencher o DataFrame com os votos de cada candidato
    for candidato in candidatos_selecionados:
        votos_por_bairro = df_selected[df_selected[12] == candidato][4].value_counts()
        bairros_info[candidato] = votos_por_bairro

    # Preencher os valores NaN (bairros sem votos) com zero
    bairros_info.fillna(0, inplace=True)

    # Criar lista de barras para o gráfico Plotly
    bar_data = []
    for candidato in candidatos_selecionados:
        bar_data.append(
            go.Bar(
                x=bairros_info.index,  # Usar a lista completa de todos os bairros
                y=bairros_info[candidato],
                name=candidato,
                hoverinfo='x+y+name',  # Informações exibidas ao passar o mouse
                hovertemplate='%{x}: %{y}',  # Template de exibição ao passar o mouse
                marker=dict(color=cores[candidato])  # Usar a cor correspondente ao candidato
                )
            )

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

def criar_dataframe_votos(dados):
    # Criar DataFrame vazio com os bairros como índice e os candidatos como colunas
    bairros = [
        'Aterrado', 'Bairro da Saúde', 'Banqueta', 'Barra do Peixe', 'Beira Rio', 'Bela Vista', 'Boiadeiro',
        'Campo Alegre', 'Centro', 'Esplanada', 'Fernando Lobo', 'Gauchão', 'Gironda', 'Goiabal',
        'Granja 3 de Outubro', 'Grota', 'Ilha Gama Cerqueira', 'Ilha Recreio', 'Ilha do Lazareto', 'Jaqueira',
        'Jardim Paraíso', 'Jardim Santa Rosa', 'Marinópolis', 'Matadouro', 'Morro do Cipó', 'Morro Trindade',
        'Morro São Sebastião', 'Morro São Geraldo', 'Morro dos Cabritos', 'Morro da Conceição', 'Parada Breves',
        'Porto Velho', 'Porto Novo', 'Praça da Bandeira', 'Remanso', 'São Geraldo', 'Santa Marta I', 'Santa Marta II',
        'Santa Rita', 'Sítio Branco', 'Terra do Santo', 'Terreirão', 'Timbira', 'Torrentes', 'Vila Laroca'
    ]  # Adicione todos os bairros
    candidatos = ['Luciana e Kadu', 'Dr. Paulo e Guará', 'Dr. Rafael e Juninho', 'Dr. Márcio e Magali']
    df = pd.DataFrame(index=bairros, columns=candidatos)

    # Preencher o DataFrame com o número de votos de cada candidato em cada bairro
    for bairro in bairros:
        for candidato in candidatos:
            num_votos = len([dado for dado in dados if dado[4] == bairro and dado[12] == candidato])
            df.at[bairro, candidato] = num_votos

    return df
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
                st.sidebar.write(f'**{candidato}= {num_votos}**',)
                # st.sidebar.write(f'**Total de Votos:** {num_votos}')
                total_participantes += num_votos

            st.sidebar.write(f'**Total de Participantes:** {total_participantes}')

        # Criar gráfico de bairros interativo com Plotly
        fig_bairros_df = grafico_bairros(dados, candidatos_selecionados)
        # selecionar as cores dos candidatos

        st.plotly_chart(fig_bairros_df)

        df_votos=criar_dataframe_votos(dados)
        st.write(df_votos)

        # Mostrar DataFrame
        print(df_votos)


if __name__ == "__main__":
    main()
