import requests
from PySide6.QtWidgets import (QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QWidget, QMessageBox,
                               QSizePolicy, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit)

from model.bloco_de_notas import Bloco_De_Notas
from controller.bloco_de_notas_dao import DataBase
from datetime import datetime

from infra.configs.connection import DBConnectionHandler

class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        conn = DBConnectionHandler()
        conn.create_database()

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
        self.detalhes = QTableWidget()

        self.detalhes.setColumnCount(4)
        self.detalhes.setHorizontalHeaderLabels(['ID', 'NOME DA NOTA', 'DATA', 'TEXTO'])

        self.detalhes.setSelectionMode(QAbstractItemView.NoSelection)
        self.detalhes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_da_nota)
        layout.addWidget(self.txt_nome_da_nota)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.txt_texto)
        layout.addWidget(self.detalhes)
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
        self.detalhes.cellDoubleClicked.connect(self.carrega_dados)
        self.mais_detalhes()


    def criar_nota(self):
        db = DataBase()

        nota = Bloco_De_Notas(
            id=self.txt_id.text(),
            nome_da_nota=self.txt_nome_da_nota.text(),
            data=datetime.now().strftime("%Y-%m-%d"),
            texto=self.txt_texto.toPlainText()

        )
        if self.btn_criar.text() == 'Criar':
            retorno = db.registar_notas(nota)

            if retorno == 'ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota Criada')
                msg.setText('Sua nota foi criada')
                msg.exec()

        elif self.btn_criar.text() == 'Atualizar':

            retorno = db.atualizar_notas(nota)

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
        msg = QMessageBox()
        msg.setWindowTitle('Remover nota')
        msg.setText('Esta nota será removida')
        msg.setInformativeText(f'Você deseja remover a nota de id {self.txt_id.text()}?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')

        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            db = DataBase()
            retorno = db.deletar_notas(self.txt_id.text())

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
        self.detalhes.setRowCount(0)
        db = DataBase()
        lista_notas = db.consultar_todas_notas()
        self.detalhes.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):
            for coluna, valor in enumerate(nota):
                self.detalhes.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carrega_dados(self, row, column):
        self.txt_id.setText(self.detalhes.item(row, 0).text())
        self.txt_data.setText(self.detalhes.item(row, 2).text())
        self.txt_nome_da_nota.setText(self.detalhes.item(row, 1).text())
        self.txt_texto.setText(self.detalhes.item(row, 3).text())

        self.btn_criar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.txt_id.setReadOnly(True)