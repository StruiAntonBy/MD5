import resources

from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from algorithm import *
from config import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.text_edit = QTextEdit()
        self.btn_calculate = QPushButton(NAME_BUTTON)
        self.btn_calculate.clicked.connect(self.calculate)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text_edit)
        self.vbox.addWidget(self.btn_calculate, alignment=Qt.AlignLeft)
        self.setLayout(self.vbox)

    def calculate(self):
        md5_to_hex = lambda digest: "{:032x}".format(int.from_bytes(digest.to_bytes(16, byteorder="little"),
                                                                    byteorder="big"))
        dialog = QMessageBox(QMessageBox.NoIcon, TITLE_DIALOG, md5_to_hex(md5(bytearray(self.text_edit.toPlainText(),
                                                                ENCODING))), buttons=QMessageBox.NoButton, parent=self)
        dialog.exec()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON))
    window = MainWindow()
    window.resize(*WINDOW_SIZE)
    window.setWindowTitle(APP_NAME)
    desktop = QApplication.desktop()
    window.move((desktop.width() - window.width()) // 2, (desktop.height() - window.height()) // 2)
    window.show()
    sys.exit(app.exec_())
