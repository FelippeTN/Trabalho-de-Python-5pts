import psycopg2

class AppBD:
    def __init__(self):
        print('Método Construtor')
    
    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres", password="1234",
                                                host="127.0.0.1",port="5433",
                                                database="postgres")
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)

