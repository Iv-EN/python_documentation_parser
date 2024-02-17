from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
"""Путь к сайту с документацией python."""
PEP_URL = 'https://peps.python.org/'
"""Путь к сайту с данными обо всех PEP."""

BASE_DIR = Path(__file__).parent
"""Рабочая дирректория парсера."""
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
"""Формат даты и времени."""
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    '': ('Draft', 'Active'),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
}
"""Словарь индексов статусов и их названий."""
