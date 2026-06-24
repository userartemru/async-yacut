import random
import re

from yacut.constants import (
    AUTO_SHORT_ID_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_CHARS,
    SHORT_IDENTIFIER_CHARACTERS,
)
from yacut.models import URLMap


SHORT_ID_REGEX = re.compile(SHORT_IDENTIFIER_CHARACTERS)


def is_valid_short_id(short_id):
    return (
        isinstance(short_id, str)
        and SHORT_ID_REGEX.fullmatch(short_id)
    )


def is_short_id_available(short_id):
    return (
        short_id not in RESERVED_SHORT_IDS
        and URLMap.query.filter_by(short=short_id).first() is None
    )


def get_unique_short_id(length=AUTO_SHORT_ID_LENGTH):
    while True:
        short_id = ''.join(random.choices(SHORT_ID_CHARS, k=length))
        if is_short_id_available(short_id):
            return short_id
