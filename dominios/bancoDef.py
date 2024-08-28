import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

dotenv_path='.env'
load_dotenv(dotenv_path=dotenv_path)
flaskSecret = os.getenv('FLASK_KEY')

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


def connectorSQL():
    try:
        connection = mysql.connector.connect(
            database = DB_NAME,
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASSWORD
        )
        if connection.is_connected():
            return connection
        else:
            return None
        
    except Error as e:
        raise ValueError(f"Ocorreu um erro: {e}")
    

def executeQuery(query,params=None):
    db = connectorSQL()
    if db:
        cursor = db.cursor()
        try:
            if params:
                #os parametros a serem executados deve ser uma lista ou tupla
                if not isinstance(params,(list,tuple)):
                    params = (params,)
                cursor.execute(query,params)
            else:
                cursor.execute(query)
            
            #Caso seja um select e tenha que retorna algum valor
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
            else:
                #marca o fim da transacao caso nao seja select
                db.commit()
                if query.strip().lower().startswith("insert"):
                    result = cursor.lastrowid
                else:
                    result = None

            return result

        except Error as e:
            raise ValueError(f"Erro ao executar query: {e}")
        
        finally:
            if cursor:
                cursor.close()

            if db.is_connected():
                db.close()
    else:
        #Caso ocorra algum erro ao connectar no banco
        return None