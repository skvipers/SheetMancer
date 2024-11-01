import logging
from PIL import Image
import math

# Настройка логирования
logger = logging.getLogger(__name__)

def create_spritesheet(image_paths, columns, padding):
    """
    Создает спрайтшит из заданных изображений.

    :param image_paths: список путей к изображениям
    :param columns: количество столбцов в спрайтшите
    :param padding: отступы между изображениями
    :return: объект Image спрайтшита или None, если не удалось создать спрайтшит
    """
    # Загрузка изображений
    images = []
    for path in image_paths:
        try:
            images.append(Image.open(path))
        except Exception as e:
            logger.error(f"Ошибка при открытии файла {path}: {e}")

    if not images:
        logger.warning("Не удалось загрузить ни одного изображения для создания спрайтшита.")
        return None

    # Размеры отдельных изображений
    img_width, img_height = images[0].size
    logger.info(f"Размеры отдельных изображений: {img_width}x{img_height}")

    # Вычисляем размеры итогового спрайтшита
    rows = math.ceil(len(images) / columns)
    sheet_width = columns * img_width + (columns - 1) * padding
    sheet_height = rows * img_height + (rows - 1) * padding
    logger.info(f"Размеры спрайтшита: {sheet_width}x{sheet_height}, строки: {rows}, столбцы: {columns}")

    # Создаем пустое изображение для спрайтшита
    spritesheet = Image.new("RGBA", (sheet_width, sheet_height))
    logger.info("Пустой спрайтшит создан.")

    # Размещение изображений на спрайтшите
    for index, img in enumerate(images):
        x = (index % columns) * (img_width + padding)
        y = (index // columns) * (img_height + padding)
        spritesheet.paste(img, (x, y))
        logger.debug(f"Изображение {index + 1} размещено на спрайтшите в позиции ({x}, {y}).")

    logger.info("Спрайтшит успешно создан.")
    return spritesheet
