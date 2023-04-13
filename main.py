import sys


from PySide6.QtWidgets import QApplication
from controller.bloco_de_notas_dao import DataBase
from view.tela_principal import MainWindow

db = DataBase()
db.connect()
db.create_table_notas()
db.close_conection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()