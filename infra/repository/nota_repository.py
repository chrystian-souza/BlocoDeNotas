from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota

class NotaRepository:


# Método para realizar a consulta de todas as notas
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

# Método para realizar a consulta das notas por id
    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).filter(Nota.id == id).first()
            return data

#Método para inserir nota no banco de dados
    def insert(self,nota):
        with DBConnectionHandler() as db:
            try:
                db.session.add(nota)
                db.session.commit()
                return 'OK'
            except Exception as e:
                db.session.rollback()
                return e


#Mètodo para realizar a remoção de uma nota do banco de dados
    def delete(self):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).delete()
            db.session.commit()

#Método para atualizar uma nota

    def update(self, id, nome_da_nota, texto):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).update({'nome_da_nota' : nome_da_nota, 'texto' : texto})
            db.session.commit()