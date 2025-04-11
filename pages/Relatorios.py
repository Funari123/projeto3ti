import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# Função para conectar ao banco de dados PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres.svjmajyagopydrjfyxmx", 
        password="jrc0KX5CnOSKSV3O", 
        host="aws-0-us-east-1.pooler.supabase.com", 
        port="6543"
    )
    return conn

# Função para exibir o relatório
def display_report():
    st.title("📊 Relatórios de Cadastro de Alunos")

    conn = connect_db()
    cur = conn.cursor()

    # Consulta para número de alunos por unidade
    cur.execute("""
        SELECT u.nome_unidade, COUNT(a.aluno_id) AS total_alunos
        FROM Fato_Cadastro_Aluno f
        JOIN Dim_Aluno a ON f.aluno_id = a.aluno_id
        JOIN Dim_Unidade u ON f.unidade_id = u.unidade_id
        GROUP BY u.nome_unidade;
    """)
    unidades = cur.fetchall()
    df_unidades = pd.DataFrame(unidades, columns=["Unidade", "Total de Alunos"])

    st.subheader("📍 Alunos por Unidade")
    fig_unidades = px.bar(df_unidades, x="Unidade", y="Total de Alunos", color="Unidade",
                          title="Distribuição de Alunos por Unidade",
                          labels={"Total de Alunos": "Quantidade"},
                          text_auto=True)
    st.plotly_chart(fig_unidades)

    # Consulta para distribuição de idades
    cur.execute("""
        SELECT EXTRACT(YEAR FROM AGE(a.data_nascimento)) AS idade, COUNT(*) AS total
        FROM Dim_Aluno a
        GROUP BY idade
        ORDER BY idade;
    """)
    idades = cur.fetchall()
    df_idades = pd.DataFrame(idades, columns=["Idade", "Total de Alunos"])

    st.subheader("🎂 Distribuição de Idades")
    fig_idade = px.histogram(df_idades, x="Idade", y="Total de Alunos", nbins=20,
                             title="Histograma de Idades dos Alunos",
                             labels={"Total de Alunos": "Quantidade", "Idade": "Idade"},
                             text_auto=True)
    st.plotly_chart(fig_idade)

    # Consulta para distribuição por sexo
    cur.execute("""
        SELECT a.sexo, COUNT(*) AS total
        FROM Dim_Aluno a
        GROUP BY a.sexo;
    """)
    sexos = cur.fetchall()
    df_sexos = pd.DataFrame(sexos, columns=["Sexo", "Total de Alunos"])

    st.subheader("🚻 Distribuição por Sexo")
    fig_sexo = px.pie(df_sexos, values="Total de Alunos", names="Sexo",
                      title="Distribuição de Alunos por Sexo",
                      color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_sexo)

    cur.close()
    conn.close()

# Função principal para o Streamlit
def main():
    display_report()

if __name__ == '__main__':
    main()
