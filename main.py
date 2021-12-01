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
        self.dialog = Form()
        self.dialog.show()


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


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.new)
        self.modified = {}
        self.titles = None


    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffee").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            print(que)
            cur.execute(que)
            self.con.commit()
            self.modified.clear()

    def new(self):
        cur = self.con.cursor()
        cur.execute("INSERT INTO coffee VALUES(0,0,0,0, 0, 0)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())