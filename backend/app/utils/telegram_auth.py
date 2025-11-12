import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from fastapi import HTTPException, Header


def validate_telegram_init_data(init_data: str, bot_token: str) -> dict:
    """
    Валидирует Telegram initData и извлекает данные пользователя.
    
    Args:
        init_data: Строка initData от Telegram WebApp
        bot_token: Токен бота
        
    Returns:
        dict: Данные пользователя (включая user_id)
        
    Raises:
        HTTPException: Если данные невалидны
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Получены initData длиной {len(init_data)} символов")
        
        # Парсим initData
        parsed_data = dict(parse_qsl(init_data))
        logger.info(f"Распарсены ключи: {list(parsed_data.keys())}")
        
        # Извлекаем hash
        data_check_string_parts = []
        hash_value = None
        
        for key, value in sorted(parsed_data.items()):
            if key == 'hash':
                hash_value = value
            else:
                data_check_string_parts.append(f'{key}={value}')
        
        if not hash_value:
            logger.error("Отсутствует hash в initData")
            raise HTTPException(status_code=401, detail="Отсутствует hash в initData")
        
        # Формируем строку для проверки
        data_check_string = '\n'.join(data_check_string_parts)
        logger.info(f"Data check string создана, количество полей: {len(data_check_string_parts)}")
        
        # Создаём секретный ключ из токена бота
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Вычисляем hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Проверяем hash
        if calculated_hash != hash_value:
            logger.error(f"Hash не совпадает. Ожидается: {calculated_hash}, получен: {hash_value}")
            raise HTTPException(status_code=401, detail="Невалидные данные Telegram")
        
        logger.info("Hash валиден!")
        
        # Извлекаем данные пользователя
        if 'user' not in parsed_data:
            logger.error("Отсутствуют данные пользователя")
            raise HTTPException(status_code=401, detail="Отсутствуют данные пользователя")
        
        user_data = json.loads(parsed_data['user'])
        logger.info(f"Пользователь извлечён: ID={user_data.get('id')}, username={user_data.get('username')}")
        
        return {
            'user_id': user_data.get('id'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'username': user_data.get('username'),
            'language_code': user_data.get('language_code'),
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail="Невалидный формат данных")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка валидации: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Ошибка валидации: {str(e)}")


async def get_telegram_user_id(
    x_telegram_init_data: str = Header(None, alias="X-Telegram-Init-Data")
) -> int:
    """
    Dependency для получения telegram_user_id из заголовка.
    
    Args:
        x_telegram_init_data: Telegram initData из заголовка запроса
        
    Returns:
        int: Telegram user ID
        
    Raises:
        HTTPException: Если данные невалидны или отсутствуют
    """
    import logging
    logger = logging.getLogger(__name__)
    
    from app.core.config import settings
    
    # Режим разработки: пропускаем валидацию Telegram
    if settings.development_mode:
        logger.info("Режим разработки: используется тестовый user_id")
        return 123456789
    
    logger.info(f"Заголовок X-Telegram-Init-Data присутствует: {bool(x_telegram_init_data)}")
    
    if not x_telegram_init_data:
        logger.error("Отсутствует заголовок X-Telegram-Init-Data")
        raise HTTPException(
            status_code=401,
            detail="Требуется авторизация через Telegram"
        )
    
    user_data = validate_telegram_init_data(x_telegram_init_data, settings.telegram_bot_token)
    
    if not user_data.get('user_id'):
        logger.error("user_id отсутствует в данных пользователя")
        raise HTTPException(status_code=401, detail="Не удалось получить user_id")
    
    logger.info(f"Авторизация успешна: user_id={user_data['user_id']}")
    return user_data['user_id']

