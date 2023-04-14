import requests
from PySide6.QtWidgets import (QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QWidget, QMessageBox,
                               QSizePolicy, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem)

from model.bloco_de_notas import Bloco_De_Notas
from controller.bloco_de_notas_dao import DataBase
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(400, 400)

        self.setWindowTitle('Bloco de notas')

        #self.lbl_id = QLabel('id')
        #self.txt_id = QLineEdit()
        self.lbl_nome_da_nota = QLabel('Título da nota')
        self.txt_nome_da_nota = QLineEdit()
        self.lbl_texto = QLabel('Texto')
        self.txt_texto = QLineEdit()
        self.txt_data = QLineEdit()
        self.btn_criar = QPushButton('Criar')

        layout = QVBoxLayout()
        #layout.addWidget(self.lbl_id)
        #layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_da_nota)
        layout.addWidget(self.txt_nome_da_nota)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.txt_texto)
        layout.addWidget(self.btn_criar)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_criar.clicked.connect(self.criar_nota)


    def criar_nota(self):
        db = DataBase()

        nota = Bloco_De_Notas(
            #id = self.txt_id.text(),
            nome_da_nota = self.txt_nome_da_nota.text(),
            data = self.txt_data.text(),
            texto = self.txt_texto.text()

        )
        if self.btn_criar.text() == 'Criar':
            retorno = db.registar_notas(nota)

            if retorno == 'ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota Criada')
                msg.setText('Sua nota foi criada')
                msg.exec()



