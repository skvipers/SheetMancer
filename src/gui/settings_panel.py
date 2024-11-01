import logging
from PySide6.QtWidgets import QWidget, QSpinBox, QLabel, QVBoxLayout, QPushButton

# Настройка логирования
logger = logging.getLogger(__name__)

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Дополнительные отступы

        # Настройка количества столбцов
        self.columns_label = QLabel("Количество столбцов:")
        self.columns_spin = QSpinBox()
        self.columns_spin.setRange(1, 20)
        self.columns_spin.setValue(5)  # По умолчанию 5 столбцов

        # Настройка отступов
        self.padding_label = QLabel("Отступы (в пикселях):")
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(0, 50)
        self.padding_spin.setValue(5)  # По умолчанию отступ 5 пикселей

        # Кнопка для создания спрайтшита
        self.create_button = QPushButton("Создать спрайтшит")

        # Добавление элементов на панель
        layout.addWidget(self.columns_label)
        layout.addWidget(self.columns_spin)
        layout.addWidget(self.padding_label)
        layout.addWidget(self.padding_spin)
        
        layout.addStretch(1)  # Добавляем растягиваемое пространство перед кнопкой
        layout.addWidget(self.create_button)

        self.setLayout(layout)

        logger.info("Панель настроек инициализирована.")

    def get_settings(self):
        """Возвращает текущие настройки в виде словаря."""
        settings = {
            "columns": self.columns_spin.value(),
            "padding": self.padding_spin.value(),
        }
        logger.info(f"Получены текущие настройки: {settings}")
        return settings
