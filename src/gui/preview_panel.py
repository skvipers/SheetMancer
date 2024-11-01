from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class PreviewPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы вокруг панели

        # Заголовок с выравниванием по левому краю и верху
        self.preview_label = QLabel("Предпросмотр")
        self.preview_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Метка для изображения
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.image_paths = []
        self.pixmap = None
        self.scale_factor = 1.0  # Коэффициент масштабирования

        # Слайдер для изменения масштаба
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(200)  # 200% масштаб
        self.scale_slider.setValue(100)  # По умолчанию 100%
        self.scale_slider.valueChanged.connect(self.update_scale)

        # Добавляем элементы на панель
        layout.addWidget(self.preview_label)  # Надпись сверху
        layout.addWidget(self.image_label)    # Поле для изображения
        layout.addWidget(self.scale_slider)   # Слайдер масштаба
        self.setLayout(layout)

    def load_images(self, image_paths):
        self.image_paths = image_paths

    def set_preview_image(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.update_image()

    def update_image(self):
        if self.pixmap:
            scaled_pixmap = self.pixmap.scaled(
                self.pixmap.width() * self.scale_factor,
                self.pixmap.height() * self.scale_factor,
                Qt.KeepAspectRatio
            )
            self.image_label.setPixmap(scaled_pixmap)

    def update_scale(self, value):
        self.scale_factor = value / 100  # Приводим значение слайдера к коэффициенту
        self.update_image()
