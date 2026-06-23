import random
import re

from yacut.constants import (
    AUTO_SHORT_ID_LENGTH,
    CUSTOM_SHORT_ID_MAX_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_CHARS,
)
from yacut.models import URLMap


SHORT_ID_PATTERN = re.compile(r'^[A-Za-z0-9]+$')


def is_valid_short_id(short_id):
    return (
        isinstance(short_id, str)
        and short_id
        and len(short_id) <= CUSTOM_SHORT_ID_MAX_LENGTH
        and SHORT_ID_PATTERN.fullmatch(short_id)
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
