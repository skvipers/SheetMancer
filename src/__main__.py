from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.main_window import MainWindow
import sys
import os


def load_stylesheet(app, path):
    with open(path, "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet_path = os.path.join("assets", "style.css")
    load_stylesheet(app, stylesheet_path)  # Применяем стили из файла
    app.setWindowIcon(QIcon(os.path.join("assets", "icon.ico")))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())