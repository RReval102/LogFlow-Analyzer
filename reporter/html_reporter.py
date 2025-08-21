# Генератор отчетов в формате HTML с графиками.

import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader
from .base_reporter import BaseReporter


class HTMLReporter(BaseReporter):
    """
    Генерирует отчеты в формате HTML с визуализациями.
    """

    def _plot_to_base64(self, plot_function, *args, **kwargs):
        """
        Выполняет функцию построения графика и возвращает его в виде строки base64.
        """
        plt.figure(figsize=(10, 5))
        plot_function(*args, **kwargs)
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight')
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def generate(self, analysis_data: dict, output_path: str):
        """
        Создает HTML-файл с отчетом, используя шаблонизатор Jinja2.
        """
        # Настройка Seaborn для красивых графиков
        sns.set_theme(style="whitegrid")

        # График по уровням
        levels_plot = self._plot_to_base64(
            sns.barplot,
            x=analysis_data['level_counts'].index,
            y=analysis_data['level_counts'].values
        )

        # График активности по часам
        activity_plot = self._plot_to_base64(
            sns.lineplot,
            data=analysis_data['activity_by_hour']
        )

        # Настройка Jinja2
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('report_template.html')

        # Рендеринг шаблона с данными
        html_content = template.render(
            data=analysis_data,
            levels_plot=levels_plot,
            activity_plot=activity_plot
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)