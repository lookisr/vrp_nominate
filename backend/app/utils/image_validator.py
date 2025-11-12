from io import BytesIO

from PIL import Image


def is_square_image(image_data: bytes) -> bool:
    """Эта функция проверяет, является ли изображение квадратным."""

    try:
        image = Image.open(BytesIO(image_data))
        width, height = image.size
        return width == height
    except Exception:
        return False


def validate_image_square(image_data: bytes) -> tuple[bool, str]:
    """Эта функция валидирует изображение и возвращает результат с сообщением."""

    if not is_square_image(image_data):
        return False, "Изображение должно быть квадратным (одинаковые ширина и высота)"
    return True, ""

