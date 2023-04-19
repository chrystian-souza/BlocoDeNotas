import sqlite3

from model.bloco_de_notas import Bloco_De_Notas

class DataBase:

    def __init__(self, nome='system.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_conection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_notas(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS NOTAS(
            NOME_DA_NOTA TEXT,
            DATA TEXT,
            TEXTO TEXT,
            
            ID INTEGER PRIMARY KEY AUTOINCREMENT
            );
            
            """)
        self.close_conection()

    def registar_notas(self, nota ):
        self.connect()
        cursor = self.connection.cursor()
        campos_nota = ('NOME_DA_NOTA', 'DATA', 'TEXTO')

        valores = f"'{nota.nome_da_nota}','{nota.data}', '{nota.texto}'"

        try:
            cursor.execute(f""" INSERT INTO NOTAS {campos_nota} VALUES ({valores})""")
            self.connection.commit()
            return 'ok'
        except sqlite3.Error as e:
            return str(e)
        finally:
            self.close_conection()

    def consultar_notas(self, id):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" SELECT * FROM NOTAS WHERE ID = '{id}' """)
            return cursor.fetchone()
        except sqlite3.Error as e:
            return None
        finally:
            self.close_conection()

    def consultar_todas_notas(self):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM NOTAS")
            notas = cursor.fetchall()
            return notas
        except sqlite3.Error as e:
            print(f'Erro {e}')
            return None
        finally:
            self.close_conection()

    def deletar_notas(self, id):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" DELETE FROM NOTAS WHERE ID = '{id}'""")
            self.connection.commit()
            return 'ok'
        except sqlite3.Error as e:
            return  e
        finally:
            self.close_conection()

    def atualizar_notas(self, nota=Bloco_De_Notas ):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""UPDATE NOTAS SET 
                           NOME_DA_NOTA = '{nota.nome_da_nota}',
                           DATA = '{nota.data}',
                           TEXTO = '{nota.texto}',
                           WHERE ID = '{nota.id}'  """)
            self.connection.commit()
            return 'ok'
        except sqlite3.Error as e:
            return e
        finally:
            self.close_conection()







