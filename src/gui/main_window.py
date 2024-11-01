import logging
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QFileDialog, QToolBar, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from core.sprite_processor import create_spritesheet
from PIL.ImageQt import ImageQt
from gui.settings_panel import SettingsPanel
from gui.preview_panel import PreviewPanel
import json
import os

CONFIG_PATH = "config.json"

# Настройка логирования
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sheet Mancer")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(os.path.join("assets", "icon.ico")))
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)  # Добавляем возможность растягивания окна

        # Загружаем конфигурацию
        self.config = self.load_config()

        # Верхняя панель инструментов
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)

        # Кнопка загрузки спрайтов
        load_button = QPushButton()
        load_button.setIcon(QIcon(os.path.join("assets/icons", "open-folder.svg")))
        load_button.setToolTip("Загрузить спрайты")
        load_button.setFixedSize(48, 48)
        load_button.setIconSize(QSize(44, 44))
        load_button.clicked.connect(self.load_sprites)

        # Кнопка сохранения спрайтшита
        save_button = QPushButton()
        save_button.setIcon(QIcon(os.path.join("assets/icons", "save.svg")))
        save_button.setToolTip("Сохранить спрайтшит")
        save_button.setFixedSize(48, 48)
        save_button.setIconSize(QSize(44, 44))
        save_button.clicked.connect(self.save_spritesheet)

        # Установка отступов между кнопками
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(5)
        button_layout.addWidget(load_button)
        button_layout.addWidget(save_button)
        toolbar.addWidget(button_container)
        self.addToolBar(toolbar)

        # Центральный виджет
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)

        # Панель настроек
        self.settings_panel = SettingsPanel()
        self.settings_panel.create_button.clicked.connect(self.generate_spritesheet)

        # Область предпросмотра
        self.preview_panel = PreviewPanel()
        self.preview_panel.setMinimumSize(600, 600)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.preview_panel)

        # Подключаем сигнал files_dropped к функции generate_spritesheet
        self.preview_panel.files_dropped.connect(self.generate_spritesheet)

        central_layout.addWidget(scroll_area, 3)
        central_layout.addWidget(self.settings_panel, 1)
        self.setCentralWidget(central_widget)

    def load_config(self):
        """Загружает конфигурацию из файла JSON или создаёт новую конфигурацию по умолчанию."""
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r") as file:
                    config = json.load(file)
                    logger.info("Конфигурация загружена.")
                    return config
            except json.JSONDecodeError:
                logger.error("Ошибка чтения конфигурационного файла.")
        logger.warning("Конфигурационный файл не найден или повреждён. Загружается конфигурация по умолчанию.")
        return {"last_open_dir": "", "last_save_dir": ""}

    def save_config(self):
        """Сохраняет текущую конфигурацию в файл JSON."""
        try:
            with open(CONFIG_PATH, "w") as file:
                json.dump(self.config, file)
                logger.info("Конфигурация сохранена.")
        except IOError as e:
            logger.error(f"Ошибка при сохранении конфигурации: {e}")

    def load_sprites(self):
        """Загружает файлы с изображениями и обновляет путь последней открытой папки в конфигурации."""
        initial_dir = self.config.get("last_open_dir", "")
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите спрайты", initial_dir, "Images (*.png *.jpg *.jpeg)")
        
        if files:
            self.config["last_open_dir"] = os.path.dirname(files[0])
            self.save_config()
            self.preview_panel.load_images(files)
            logger.info(f"Загружено {len(files)} изображений для создания спрайтшита.")
            self.generate_spritesheet()

    def generate_spritesheet(self):
        settings = self.settings_panel.get_settings()
        columns = settings["columns"]
        padding = settings["padding"]

        # Проверяем, что загружены изображения
        if not self.preview_panel.image_paths:
            logger.warning("Нет загруженных изображений для создания спрайтшита.")
            return

        spritesheet = create_spritesheet(self.preview_panel.image_paths, columns, padding)
        if spritesheet:
            qimage = ImageQt(spritesheet)
            pixmap = QPixmap.fromImage(qimage)
            self.preview_panel.set_preview_image(pixmap)
            logger.info("Спрайтшит успешно создан и отображён.")

    def save_spritesheet(self):
        """Сохраняет спрайтшит и обновляет путь последней сохранённой папки в конфигурации."""
        initial_dir = self.config.get("last_save_dir", "")
        save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить спрайтшит", initial_dir, "PNG Files (*.png)")
        
        if save_path:
            self.config["last_save_dir"] = os.path.dirname(save_path)
            self.save_config()
            if self.preview_panel.pixmap:
                self.preview_panel.pixmap.save(save_path, "PNG")
                logger.info(f"Спрайтшит успешно сохранён по пути {save_path}.")
            else:
                logger.warning("Спрайтшит не был создан для сохранения.")
