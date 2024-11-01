from PIL import Image
import math

def create_spritesheet(image_paths, columns, padding):
    # Загрузка изображений
    images = [Image.open(path) for path in image_paths]
    if not images:
        return None  # Проверка: если нет изображений, возвращаем None

    # Размеры отдельных изображений
    img_width, img_height = images[0].size

    # Вычисляем размеры итогового спрайтшита
    rows = math.ceil(len(images) / columns)
    sheet_width = columns * img_width + (columns - 1) * padding
    sheet_height = rows * img_height + (rows - 1) * padding

    # Создаем пустое изображение для спрайтшита
    spritesheet = Image.new("RGBA", (sheet_width, sheet_height))

    # Размещение изображений на спрайтшите
    for index, img in enumerate(images):
        x = (index % columns) * (img_width + padding)
        y = (index // columns) * (img_height + padding)
        spritesheet.paste(img, (x, y))

    return spritesheet
