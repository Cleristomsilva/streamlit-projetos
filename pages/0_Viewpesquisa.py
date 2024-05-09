import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt


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


def grafico_idade_e_genero(dados, candidatos_selecionados, figsize=(12, 5), bins=15):
    df = pd.DataFrame(dados)
    pd.set_option('display.max_rows', None)
    df_selected = df[df[12].isin(candidatos_selecionados)]
    idades = df_selected[1]

    fig, axs = plt.subplots(1, 2, figsize=figsize)
    axs[0].hist(idades, bins=bins)
    axs[0].set_xlabel('Idade')
    axs[0].set_ylabel('Número de Participantes')
    axs[0].set_title('Distribuição por Faixa de Idade', fontweight='bold', fontsize=18, pad=20)

    # Gráfico de Gênero
    sexos = df_selected[2]
    masculino_count = (sexos == 'Masculino').sum()
    feminino_count = (sexos == 'Feminino').sum()
    counts = [masculino_count, feminino_count]
    labels = ['Masculino', 'Feminino']

    if all(count == 0 for count in counts):
        axs[1].text(
            0.5, 0.5, 'Nenhum dado disponível', horizontalalignment='center', verticalalignment='center',
            fontsize=12
        )
        axs[1].axis('off')
    else:
        axs[1].pie(counts, labels=labels, autopct='%1.1f%%')
        axs[1].set_title('Distribuição por Sexo', fontweight='bold', fontsize=18, pad=20)

    plt.tight_layout()
    return fig



def grafico_escolaridade_e_renda(dados, candidatos_selecionados, figsize=(12, 5)):
    df = pd.DataFrame(dados)
    pd.set_option('display.max_rows', None)
    df_selected = df[df[12].isin(candidatos_selecionados)]

    # Gráfico de Escolaridade
    escolaridades = df_selected[3].value_counts().sort_index()
    escolaridades = escolaridades.reindex(
        ['Ensino fundamental incompleto', 'Ensino fundamental completo', 'Ensino médio incompleto',
         'Ensino médio completo', 'Ensino superior incompleto', 'Ensino superior completo'],
        fill_value=0
    )

    # Gráfico de Renda
    rendas = df_selected[5].value_counts().sort_index()
    rendas = rendas.reindex(
        ['Até R$1.400', 'de R$1.400 a R$2.800', 'de R$2.800 a R$4.200', 'de R$4.200 a R$5.600',
         'Acima de R$5.600'],
        fill_value=0
    )

    fig, axs = plt.subplots(1, 2, figsize=figsize)

    axs[0].barh(escolaridades.index, escolaridades.values)
    axs[0].set_xlabel('Número de Participantes')
    axs[0].set_ylabel('')
    axs[0].set_title('Distribuição por Nível de Escolaridade', fontweight='bold', fontsize=18, pad=20)

    axs[1].barh(rendas.index, rendas.values)
    axs[1].set_xlabel('Número de Participantes')
    axs[1].set_ylabel('')
    axs[1].set_title('Distribuição por Renda', fontweight='bold', fontsize=18, pad=20)

    plt.tight_layout()
    return fig


def grafico_bairros(dados,candidatos_selecionados,figsize=(12,5),bins=7):
    df=pd.DataFrame(dados)
    df_selected=df[df[12].isin(candidatos_selecionados)]

    bairros=df_selected[4].value_counts().sort_index()
    bairros=bairros.reindex(
        ['Aterrado','Bairro da Saúde','Banqueta','Barra do Peixe','Beira Rio','Bela Vista','Boiadeiro','Campo Alegre',
         'Centro','Esplanada','Fernando Lobo','Gauchão','Gironda','Goiabal','Granja 3 de Outubro','Grota','Ilha Gama Cerqueira',
         'Ilha Recreio','Ilha do Lazareto','Jaqueira','Jardim Paraíso','Jardim Santa Rosa','Marinópolis','Matadouro',
         'Morro do Cipó','Morro Trindade','Morro São Sebastião','Morro São Geraldo','Morro dos Cabritos',
         'Morro da Conceição','Parada Breves','Porto Velho','Porto Novo','Praça da Bandeira','Remanso','São Geraldo','Santa Marta I',
         'Santa Marta II','Santa Rita','Sítio Branco','Terra do Santo','Terreirão','Timbira','Torrentes','Vila Laroca']
    )

    fig,ax=plt.subplots(figsize=figsize)
    bairros.plot(kind='bar',ax=ax)

    ax.set_ylabel('Número de Participantes')
    ax.set_title('Distribuição por Bairros',fontweight='bold', fontsize=18, pad=20)
    ax.set_xlabel('')
    ax.set_xticklabels(bairros.index,rotation=40,ha='right')

    plt.tight_layout()
    return fig


def main():
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

    # Verificar se há dados disponíveis
    if len(dados) == 0:
        st.warning('Não há dados disponíveis no banco de dados.')
        return

    # Opções de candidatos
    candidatos = ['Luciana e Kadu', 'Dr. Paulo e Guará', 'Dr. Rafael e Juninho', 'Dr. Márcio e Magali']

    # Filtro na barra lateral para selecionar os candidatos
    candidatos_selecionados = st.sidebar.multiselect('Selecione os Candidatos:', candidatos, default=candidatos)

    # Verificar se há dados correspondentes aos candidatos selecionados
    dados_selecionados = [dado for dado in dados if dado[12] in candidatos_selecionados]
    if len(dados_selecionados) == 0:
        st.warning('Não há dados correspondentes aos candidatos selecionados.')
        return

    # Criar gráficos para cada pergunta da pesquisa, com base nos candidatos selecionados
    fig_idade_genero = grafico_idade_e_genero(dados, candidatos_selecionados)
    st.pyplot(fig_idade_genero)

    fig_escolaridade_renda = grafico_escolaridade_e_renda(dados, candidatos_selecionados)
    st.pyplot(fig_escolaridade_renda)

    fig_bairros = grafico_bairros(dados, candidatos_selecionados)
    st.pyplot(fig_bairros)

if __name__ == "__main__":
    main()

