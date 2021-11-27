import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTextEdit, QMessageBox, QWidget

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets


# __---____----_____-----____---__
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.pushButton.clicked.connect(self.update_result)

        cur = self.con.cursor()
        que = "SELECT * FROM coffee"
        result = cur.execute(que).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def update_result(self):
        cur = self.con.cursor()


    def new(self, ids):
        cur = self.con.cursor()
        for i in ids:
            data = cur.execute(f'SELECT * FROM films WHERE id = {i}').fetchone()
            new_data = (data[0], data[1][::-1], data[2] + 1000, data[3], data[4] * 2)
            cur.execute(f'DELETE FROM films WHERE id = {data[0]}')
            cur.execute("INSERT INTO films VALUES(?,?,?,?,?)", new_data)
        self.con.commit()

    def update_elems(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            self.new(ids)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())