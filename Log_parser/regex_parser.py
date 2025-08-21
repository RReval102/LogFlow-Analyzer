# Парсер для стандартных текстовых логов с использованием регулярных выражений.

import re
import pandas as pd
from .base_parser import BaseParser


class RegexParser(BaseParser):
    """
    Парсер для текстовых лог-файлов, использующий регулярные выражения.
    Ожидаемый формат строки:
    ГГГГ-ММ-ДД ЧЧ:ММ:СС - УРОВЕНЬ - Сообщение
    """
    # Регулярное выражение для извлечения данных из строки лога
    LOG_PATTERN = re.compile(
        r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - '
        r'(?P<level>\w+) - '
        r'(?P<message>.*)$'
    )

    def parse(self, filepath: str) -> pd.DataFrame:
        """
        Парсит текстовый лог-файл.

        :param filepath: Путь к лог-файлу.
        :return: DataFrame с данными лога.
        """
        records = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = self.LOG_PATTERN.match(line)
                if match:
                    records.append(match.groupdict())

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        # Преобразуем строку с датой в объект datetime для удобства анализа
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df