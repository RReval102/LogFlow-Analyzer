# Абстрактный класс, который определяет интерфейс для всех парсеров.
# Это гарантирует, что любой новый парсер будет иметь метод parse.

from abc import ABC, abstractmethod
import pandas as pd

class BaseParser(ABC):
    """
    Абстрактный базовый класс для всех парсеров логов.
    Определяет единый интерфейс для парсинга файлов.
    """

    @abstractmethod
    def parse(self, filepath: str) -> pd.DataFrame:
        """
        Основной метод, который должен быть реализован в дочерних классах.
        Он читает лог-файл и преобразует его в pandas DataFrame.

        :param filepath: Путь к лог-файлу.
        :return: DataFrame со стандартизированными колонками: 'timestamp', 'level', 'message'.
        """
        pass