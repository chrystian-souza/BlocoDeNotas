import requests
from PySide6.QtWidgets import (QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QWidget, QMessageBox,
                               QSizePolicy, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit)

from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota
from infra.repository.nota_repository import NotaRepository
from infra.configs.base import Base
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        conn = DBConnectionHandler()

        self.setMinimumSize(400, 400)

        self.setWindowTitle('Bloco de notas')

        self.lbl_id = QLabel('id')
        self.txt_id = QLineEdit()
        self.txt_id.setReadOnly(True)
        self.lbl_nome_da_nota = QLabel('Título da nota')
        self.txt_nome_da_nota = QLineEdit()
        self.lbl_texto = QLabel('Texto')
        self.txt_texto = QTextEdit()
        self.txt_data = QLineEdit()
        self.btn_criar = QPushButton('Criar')
        self.btn_remover = QPushButton('Remover')
        self.btn_limpar = QPushButton('Limpar')
        self.tabela_detalhes = QTableWidget()

        self.tabela_detalhes.setColumnCount(4)
        self.tabela_detalhes.setHorizontalHeaderLabels(['ID', 'NOME DA NOTA', 'TEXTO', 'DATA'])

        self.tabela_detalhes.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_detalhes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_da_nota)
        layout.addWidget(self.txt_nome_da_nota)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.txt_texto)
        layout.addWidget(self.tabela_detalhes)
        layout.addWidget(self.btn_criar)
        layout.addWidget(self.btn_remover)
        layout.addWidget(self.btn_limpar)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_criar.clicked.connect(self.criar_nota)
        self.btn_limpar.clicked.connect(self.limpar_conteudo)
        self.btn_remover.clicked.connect(self.remover_nota)
        self.tabela_detalhes.cellDoubleClicked.connect(self.carrega_dados)
        self.mais_detalhes()

    def criar_nota(self):
        db = NotaRepository()
        nota = Nota(
            nome_da_nota=self.txt_nome_da_nota.text(),
            data=datetime.now().strftime("%Y-%m-%d"),
            texto=self.txt_texto.toPlainText()

        )
        if self.btn_criar.text() == 'Criar':
            retorno = db.insert(nota)

            if retorno == 'ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota Criada')
                msg.setText('Sua nota foi criada')
                msg.exec()

        elif self.btn_criar.text() == 'Atualizar':

            nota.id = int(self.txt_id.text())
            retorno = db.update(nota)

            if retorno == 'ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota atualizada')
                msg.setText('Nota atualizada com sucesso')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao atualizar')
                msg.setText('Erro ao cadastrar, verifique os dados inseridos')
                msg.exec()
            self.txt_id.setReadOnly(False)
        self.mais_detalhes()

    def limpar_conteudo(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()
        self.btn_remover.setVisible(False)
        self.txt_id.setReadOnly(True)
        self.btn_criar.setText('Criar')

    def remover_nota(self):
        db = NotaRepository()
        msg = QMessageBox()
        msg.setWindowTitle('Remover nota')
        msg.setText('Esta nota será removida')
        msg.setInformativeText(f'Você deseja remover a nota de id {self.txt_id.text()}?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')

        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            retorno = db.delete(self.txt_id.text())

            if retorno == 'ok':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover nota')
                nv_msg.setText('Nota removida com sucesso')
                nv_msg.exec()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover nota')
                nv_msg.setText('Erro ao Remover')
                nv_msg.exec()
            self.txt_id.setReadOnly(False)
            self.mais_detalhes()
        self.mais_detalhes()

    def mais_detalhes(self):
        self.tabela_detalhes.setRowCount(0)
        conn = NotaRepository()
        lista_notas = conn.select_all()
        print('mais detalhes def')
        self.tabela_detalhes.setRowCount(len(lista_notas))

        linha = 0
        for nota in lista_notas:
            valores = [nota.id, nota.nome_da_nota, nota.texto, nota.data]
            for valor in valores:
                item = QTableWidgetItem(str(valor))
                self.tabela_detalhes.setItem(linha, valores.index(valor), item)
                self.tabela_detalhes.item(linha, valores.index(valor))
            linha += 1

    def carrega_dados(self, row, column):
        self.txt_id.setText(self.tabela_detalhes.item(row, 0).text())
        self.txt_nome_da_nota.setText(self.tabela_detalhes.item(row, 1).text()
                                      if self.tabela_detalhes.item(row, 1) is not None else '')
        self.txt_texto.setText(self.tabela_detalhes.item(row, 2).text()
                               if self.tabela_detalhes.item(row, 2) is not None else '')
        self.txt_data.setText(self.tabela_detalhes.item(row, 3).text()
                              if self.tabela_detalhes.item(row, 3) is not None else '')

        self.btn_criar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.txt_id.setReadOnly(True)
