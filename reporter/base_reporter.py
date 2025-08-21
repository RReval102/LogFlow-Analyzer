# Абстрактный класс для генераторов отчетов.

from abc import ABC, abstractmethod

class BaseReporter(ABC):
    """
    Абстрактный базовый класс для всех генераторов отчетов.
    """

    @abstractmethod
    def generate(self, analysis_data: dict, output_path: str):
        """
        Генерирует отчет на основе результатов анализа.

        :param analysis_data: Словарь с результатами от Analyzer.
        :param output_path: Путь для сохранения сгенерированного отчета.
        """
        pass