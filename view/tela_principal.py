import requests
from PySide6.QtWidgets import (QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QWidget, QMessageBox,
                               QSizePolicy, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem)

class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(400, 400)

        self.setWindowTitle('Bloco de notas')

        self.lbl_id = QLabel('id')
        self.txt_id = QLineEdit()
        self.lbl_nome_da_nota = QLabel('Título da nota')
        self.txt_nome_da_nota = QLineEdit()
        self.lbl_texto = QLabel('Testo')
        self.txt_texto = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_da_nota)
        layout.addWidget(self.txt_nome_da_nota)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.txt_texto)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)
