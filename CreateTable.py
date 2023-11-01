import psycopg2

#CREATE

conn = psycopg2.connect(database="postgres",user="postgres",password="1234",port="5433")
print("Conexão com o Banco de Dados aberta com sucesso!")

comando = conn.cursor()
comando.execute(""" CREATE TABLE Users
                (id SERIAL PRIMARY KEY,
                Nome TEXT NOT NULL,
                Cpf CHAR(11))
                """)

comando.execute(""" CREATE TABLE Products
                (id SERIAL PRIMARY KEY,
                NomeProd TEXT NOT NULL,
                PrecoAV NUMERIC,
                PrecoCC NUMERIC)
                """)

conn.commit()
print("Tabela criada com sucesso no BD!")

