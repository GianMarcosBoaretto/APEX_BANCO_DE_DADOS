import mysql.connector
from mysql.connector import Error
import configparser

def conectar():
    config = configparser.ConfigParser()
    config.read('bd.ini')

    try:
        conexao = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            database=config['mysql']['database']
        )

        if conexao.is_connected():
            return conexao

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None
