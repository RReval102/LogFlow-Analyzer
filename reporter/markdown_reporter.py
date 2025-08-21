# Генератор отчетов в формате Markdown.

from .base_reporter import BaseReporter

class MarkdownReporter(BaseReporter):
    """
    Генерирует отчеты в формате Markdown.
    """
    def generate(self, analysis_data: dict, output_path: str):
        """
        Создает Markdown-файл с отчетом.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 📊 Отчет по анализу лог-файла\n\n")

            # Общая статистика
            f.write("## 📝 Общая статистика\n")
            f.write(f"- **Всего записей:** {analysis_data['total_records']}\n")
            start_time, end_time = analysis_data['log_period']
            f.write(f"- **Период логов:** с `{start_time}` по `{end_time}`\n\n")

            # Статистика по уровням
            f.write("## 🚦 Статистика по уровням\n")
            f.write("| Уровень | Количество |\n")
            f.write("|---------|------------|\n")
            for level, count in analysis_data['level_counts'].items():
                f.write(f"| {level} | {count} |\n")
            f.write("\n")

            # Топ ошибок
            f.write(f"## ❌ Топ-{len(analysis_data['top_errors'])} ошибок\n")
            if not analysis_data['top_errors'].empty:
                f.write("| Ошибка | Частота |\n")
                f.write("|--------|---------|\n")
                for msg, count in analysis_data['top_errors'].items():
                    f.write(f"| `{msg}` | {count} |\n")
            else:
                f.write("Ошибки не найдены.\n")
            f.write("\n")

            # Активность по часам
            f.write("## ⏰ Активность по часам\n")
            f.write("| Час | Количество записей |\n")
            f.write("|-----|--------------------|\n")
            for time, count in analysis_data['activity_by_hour'].items():
                f.write(f"| {time.strftime('%Y-%m-%d %H:00')} | {count} |\n")