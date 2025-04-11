import streamlit as st
import psycopg2

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

# Função para registrar um aluno
def register_student():
    st.title("Cadastro de Aluno")

    # Formulário de entrada
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    endereco = st.text_area("Endereço")
    data_nascimento = st.date_input("Data de Nascimento")
    altura = st.number_input("Altura (cm)", min_value=0)
    peso = st.number_input("Peso (kg)", min_value=0)
    sexo = st.selectbox("Sexo", ["M", "F"])
    grau_instrucao = st.text_input("Grau de Instrução (opcional)")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")

    if st.button("Cadastrar"):
        if nome and cpf and endereco and data_nascimento and altura and peso and sexo:
            # Inserir dados no banco de dados
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Dim_Aluno (nome, cpf, endereco, data_nascimento, altura, peso, sexo, grau_instrucao, telefone, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, cpf, endereco, data_nascimento, altura, peso, sexo, grau_instrucao, telefone, email))
            conn.commit()
            st.success("Aluno cadastrado com sucesso!")
            cur.close()
            conn.close()
        else:
            st.error("Todos os campos obrigatórios devem ser preenchidos.")

# Função principal para o Streamlit
def main():
    register_student()

if __name__ == '__main__':
    main()
