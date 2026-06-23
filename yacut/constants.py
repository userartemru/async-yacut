import string


AUTO_SHORT_ID_LENGTH = 6
CUSTOM_SHORT_ID_MAX_LENGTH = 16
DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
RESERVED_SHORT_IDS = {'files'}
SHORT_ID_CHARS = string.ascii_letters + string.digits
