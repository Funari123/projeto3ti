import psycopg2
from faker import Faker
import random
from datetime import datetime

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

# Função para gerar e inserir múltiplos alunos no banco de dados
def insert_students(num_students):
    fake = Faker('pt_BR')  # Usando o provedor brasileiro do Faker
    
    conn = connect_db()
    cur = conn.cursor()

    for _ in range(num_students):
        nome = fake.name()
        cpf = fake.cpf()  # Agora estamos usando o método correto para gerar CPF
        endereco = fake.address()
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=60)
        altura = round(random.uniform(1.50, 2.00), 2)  # Altura entre 1.50m e 2.00m
        peso = round(random.uniform(50, 100), 2)  # Peso entre 50kg e 100kg
        sexo = random.choice(["M", "F"])
        grau_instrucao = random.choice(["Ensino Médio", "Ensino Superior", "Pós-graduação", "Mestrado", "Doutorado", "Nenhum"])
        telefone = fake.phone_number()
        email = fake.email()

        # Inserir dados do aluno na tabela Dim_Aluno
        cur.execute("""
            INSERT INTO Dim_Aluno (nome, cpf, endereco, data_nascimento, altura, peso, sexo, grau_instrucao, telefone, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, cpf, endereco, data_nascimento, altura, peso, sexo, grau_instrucao, telefone, email))

    conn.commit()
    cur.close()
    conn.close()

    print(f"{num_students} alunos inseridos com sucesso!")

# Definindo o número de alunos a serem gerados
num_students = 100  # Por exemplo, insira 100 alunos

# Inserir os alunos
insert_students(num_students)
