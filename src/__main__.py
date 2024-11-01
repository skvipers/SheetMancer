import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.main_window import MainWindow
import sys
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_stylesheet(app, path):
    if os.path.exists(path):  # Проверяем, существует ли файл стилей
        with open(path, "r") as f:
            app.setStyleSheet(f.read())
        logger.info("Стили успешно загружены.")
    else:
        logger.warning(f"Файл стилей {path} не найден.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet_path = os.path.join("assets", "style.css")
    load_stylesheet(app, stylesheet_path)  # Применяем стили из файла
    app.setWindowIcon(QIcon(os.path.join("assets", "icon.ico")))
    window = MainWindow()
    window.show()
    logger.info("Приложение запущено.")
    sys.exit(app.exec())
