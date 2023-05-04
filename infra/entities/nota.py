from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime

class Nota(Base):
    #Nome da tabela criada
    __tablename__ = 'nota'
    #Colunas da tabela que serão criadas na tabela
    id = Column(Integer, autoincrement=True, primary_key=True)
    nome_da_nota = Column(String(length=100), nullable=False)
    data = Column(DateTime)
    texto = Column(String(length=100), nullable=False)

    #Função que sobrescreve a maneira de 'printar' o objeto
    def __repr__(self):
        return f'Título da nota = {self.titulo}, id = {self.id}'


