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
    try:
        # Парсим initData
        parsed_data = dict(parse_qsl(init_data))
        
        # Извлекаем hash
        data_check_string_parts = []
        hash_value = None
        
        for key, value in sorted(parsed_data.items()):
            if key == 'hash':
                hash_value = value
            else:
                data_check_string_parts.append(f'{key}={value}')
        
        if not hash_value:
            raise HTTPException(status_code=401, detail="Отсутствует hash в initData")
        
        # Формируем строку для проверки
        data_check_string = '\n'.join(data_check_string_parts)
        
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
            raise HTTPException(status_code=401, detail="Невалидные данные Telegram")
        
        # Извлекаем данные пользователя
        if 'user' not in parsed_data:
            raise HTTPException(status_code=401, detail="Отсутствуют данные пользователя")
        
        user_data = json.loads(parsed_data['user'])
        
        return {
            'user_id': user_data.get('id'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'username': user_data.get('username'),
            'language_code': user_data.get('language_code'),
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Невалидный формат данных")
    except Exception as e:
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
    from app.core.config import settings
    
    # Режим разработки: пропускаем валидацию Telegram
    if settings.development_mode:
        # В режиме разработки возвращаем тестовый ID
        # Можно использовать разные ID для тестирования
        return 123456789
    
    if not x_telegram_init_data:
        raise HTTPException(
            status_code=401,
            detail="Требуется авторизация через Telegram"
        )
    
    user_data = validate_telegram_init_data(x_telegram_init_data, settings.telegram_bot_token)
    
    if not user_data.get('user_id'):
        raise HTTPException(status_code=401, detail="Не удалось получить user_id")
    
    return user_data['user_id']

