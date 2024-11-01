from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QFileDialog, QToolBar, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from core.sprite_processor import create_spritesheet
from PIL.ImageQt import ImageQt
from gui.settings_panel import SettingsPanel
from gui.preview_panel import PreviewPanel
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SheetMancer")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(os.path.join("assets", "icon.ico")))
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)  # Добавляем возможность растягивания окна

        # Верхняя панель инструментов
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)  # Отключаем возможность перетаскивания

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
        #button_layout.setContentsMargins(10, 10, 10, 10)  # Отступы от краев
        button_layout.setSpacing(5)  # Расстояние между кнопками

        # Добавление кнопок в контейнер
        button_layout.addWidget(load_button)
        button_layout.addWidget(save_button)
        toolbar.addWidget(button_container)

        self.addToolBar(toolbar)

        # Центральный виджет с layout
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)

        # Панель настроек
        self.settings_panel = SettingsPanel()
        self.settings_panel.create_button.clicked.connect(self.generate_spritesheet)

        # Область предпросмотра с возможностью масштабирования
        self.preview_panel = PreviewPanel()
        self.preview_panel.setMinimumSize(600, 600)  # Минимальный размер панели предпросмотра
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.preview_panel)

        # Добавляем панели в основной layout
        central_layout.addWidget(scroll_area, 3)  # Основная часть – область предпросмотра
        central_layout.addWidget(self.settings_panel, 1)  # Правая часть – панель настроек

        self.setCentralWidget(central_widget)

    def load_sprites(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите спрайты", "", "Images (*.png *.jpg *.jpeg)")
        if files:
            self.preview_panel.load_images(files)

    def generate_spritesheet(self):
        settings = self.settings_panel.get_settings()
        columns = settings["columns"]
        padding = settings["padding"]

        if not self.preview_panel.image_paths:
            print("Нет загруженных изображений для создания спрайтшита")
            return

        spritesheet = create_spritesheet(self.preview_panel.image_paths, columns, padding)
        if spritesheet:
            qimage = ImageQt(spritesheet)
            pixmap = QPixmap.fromImage(qimage)
            self.preview_panel.set_preview_image(pixmap)

    def save_spritesheet(self):
        if self.preview_panel.pixmap:
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить спрайтшит", "", "PNG Files (*.png)")
            if save_path:
                self.preview_panel.pixmap.save(save_path, "PNG")
        else:
            print("Спрайтшит еще не создан")
