import logging
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QScrollArea
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, Signal

# Настройка логирования
logger = logging.getLogger(__name__)

class PreviewPanel(QWidget):
    files_dropped = Signal()  # Сигнал для MainWindow, что файлы были загружены

    def __init__(self):
        super().__init__()
        self.image_paths = []
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Надпись для информации
        self.preview_label = QLabel("Перетащите файлы сюда для загрузки")
        self.preview_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Область прокрутки для изображения
        self.scroll_area = QScrollArea()
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidgetResizable(True)
        
        # Виджет для изображения
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #333333;")
        self.scroll_area.setWidget(self.image_label)

        # Оверлей для дроп-зоны
        self.drop_overlay = QLabel("Перетащите файлы сюда")
        self.drop_overlay.setAlignment(Qt.AlignCenter)
        self.drop_overlay.setStyleSheet("""
            background-color: rgba(80, 227, 194, 0.3);
            border: 2px dashed #50E3C2;
            color: #50E3C2;
            font-size: 18px;
        """)
        self.drop_overlay.setVisible(False)

        self.pixmap = None
        self.scale_factor = 1.0

        # Слайдер для изменения масштаба
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setValue(100)
        self.scale_slider.valueChanged.connect(self.update_scale)

        # Добавляем элементы на панель
        layout.addWidget(self.preview_label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.scale_slider)
        self.setLayout(layout)

        # Настраиваем оверлей, чтобы он занимал всю область
        self.drop_overlay.setParent(self)
        self.drop_overlay.resize(self.size())
        self.drop_overlay.raise_()

        # Настраиваем виджет для поддержки перетаскивания
        self.setAcceptDrops(True)

    def resizeEvent(self, event):
        self.drop_overlay.resize(self.size())
        self.update_image()
        super().resizeEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_overlay.setVisible(True)
            logger.info("Файлы перетаскиваются в область загрузки.")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.drop_overlay.setVisible(False)
        logger.info("Файлы покинули область загрузки.")

    def dropEvent(self, event: QDropEvent):
        self.drop_overlay.setVisible(False)
        urls = event.mimeData().urls()
        self.image_paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        
        if self.image_paths:
            self.load_images(self.image_paths)
            self.files_dropped.emit()
            logger.info(f"Загружено {len(self.image_paths)} файлов.")

    def load_images(self, image_paths):
        """Загружает изображения и сохраняет пути к ним."""
        self.image_paths = image_paths
        logger.info("Пути к изображениям сохранены.")

    def set_preview_image(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.update_image()
        logger.info("Изображение для предпросмотра установлено.")

    def update_image(self):
        if self.pixmap:
            scaled_pixmap = self.pixmap.scaled(
                int(self.scroll_area.width() * self.scale_factor),
                int(self.scroll_area.height() * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            logger.debug("Изображение обновлено с текущим масштабом.")

    def update_scale(self, value):
        self.scale_factor = value / 100
        self.update_image()
        logger.info(f"Масштаб изображения обновлен: {self.scale_factor * 100}%.")
