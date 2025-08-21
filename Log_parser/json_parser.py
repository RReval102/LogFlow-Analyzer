# Парсер для логов в формате JSON.

import json
import pandas as pd
from .base_parser import BaseParser


class JSONParser(BaseParser):
    """
    Парсер для лог-файлов в формате JSON.
    Ожидает, что каждая строка файла является валидным JSON-объектом
    с ключами 'timestamp', 'level', 'message'.
    """

    def parse(self, filepath: str) -> pd.DataFrame:
        """
        Парсит JSON лог-файл.

        :param filepath: Путь к лог-файлу.
        :return: DataFrame с данными лога.
        """
        records = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    # Каждая строка - отдельный JSON
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    # Пропускаем некорректные строки
                    print(f"Предупреждение: Не удалось распарсить JSON-строку: {line.strip()}")

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        # Проверяем наличие обязательных колонок
        required_columns = {'timestamp', 'level', 'message'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"JSON-лог должен содержать ключи: {', '.join(required_columns)}")

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df