import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

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
    st.title("Relatórios de Cadastro de Alunos")

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

    st.write(df_unidades)

    # Consulta para distribuição de idades
    cur.execute("""
        SELECT EXTRACT(YEAR FROM AGE(a.data_nascimento)) AS idade, COUNT(*) AS total
        FROM Dim_Aluno a
        GROUP BY idade
        ORDER BY idade;
    """)
    idades = cur.fetchall()
    df_idades = pd.DataFrame(idades, columns=["Idade", "Total de Alunos"])

    st.subheader('Distribuição de Idades')
    st.bar_chart(df_idades.set_index('Idade')['Total de Alunos'])

    # Consulta para distribuição por sexo
    cur.execute("""
        SELECT a.sexo, COUNT(*) AS total
        FROM Dim_Aluno a
        GROUP BY a.sexo;
    """)
    sexos = cur.fetchall()
    df_sexos = pd.DataFrame(sexos, columns=["Sexo", "Total de Alunos"])

    st.subheader('Distribuição por Sexo')
    st.bar_chart(df_sexos.set_index('Sexo')['Total de Alunos'])

    cur.close()
    conn.close()

# Função principal para o Streamlit
def main():
    display_report()

if __name__ == '__main__':
    main()
