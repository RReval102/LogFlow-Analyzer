# Содержит всю логику анализа данных, полученных от парсера.

import pandas as pd

class Analyzer:
    """
    Класс, отвечающий за анализ данных из логов, представленных в виде DataFrame.
    """
    def __init__(self, dataframe: pd.DataFrame):
        """
        Инициализирует анализатор.

        :param dataframe: DataFrame с распарсенными данными лога.
        """
        if not isinstance(dataframe, pd.DataFrame) or dataframe.empty:
            raise ValueError("Для анализа требуется непустой pandas DataFrame.")
        self.df = dataframe

    def analyze(self, top_n_errors: int = 5) -> dict:
        """
        Выполняет полный анализ данных.

        :param top_n_errors: Количество наиболее частых ошибок для включения в отчет.
        :return: Словарь с результатами анализа.
        """
        return {
            'total_records': self._count_total_records(),
            'log_period': self._get_log_period(),
            'level_counts': self._count_by_level(),
            'top_errors': self._find_top_errors(top_n_errors),
            'activity_by_hour': self._get_activity_by_hour()
        }

    def _count_total_records(self) -> int:
        """Подсчитывает общее количество записей."""
        return len(self.df)

    def _get_log_period(self) -> tuple:
        """Определяет начальную и конечную временные метки."""
        return (self.df['timestamp'].min(), self.df['timestamp'].max())

    def _count_by_level(self) -> pd.Series:
        """Группирует записи по уровню логирования (INFO, ERROR и т.д.)."""
        return self.df['level'].value_counts()

    def _find_top_errors(self, n: int) -> pd.Series:
        """Находит N самых частых сообщений с уровнем ERROR."""
        error_df = self.df[self.df['level'] == 'ERROR']
        if error_df.empty:
            return pd.Series(dtype='int64')
        return error_df['message'].value_counts().nlargest(n)

    def _get_activity_by_hour(self) -> pd.Series:
        """Подсчитывает количество записей по часам."""
        return self.df.set_index('timestamp').resample('H').size()