# Главный файл для запуска утилиты из командной строки.
# Он отвечает за парсинг аргументов, выбор нужных модулей и запуск процесса анализа.

import argparse
import pandas as pd
from datetime import datetime

# Импортируем парсеры
from log_parser.regex_parser import RegexParser
from log_parser.json_parser import JSONParser

# Импортируем анализатор
from analyzer.analyzer import Analyzer

# Импортируем генераторы отчетов
from reporter.markdown_reporter import MarkdownReporter
from reporter.html_reporter import HTMLReporter


def main():
    """
    Основная функция, управляющая логикой приложения.
    """
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Анализатор лог-файлов 'LogFlow Analyzer'")
    parser.add_argument("logfile", help="Путь к файлу лога для анализа.")
    parser.add_argument("--parser", required=True, choices=['regex', 'json'], help="Тип парсера для лог-файла.")
    parser.add_argument("--report", required=True, choices=['markdown', 'html'], help="Формат генерируемого отчета.")
    parser.add_argument("--output", help="Имя файла для сохранения отчета. По умолчанию: report.<ext>")
    parser.add_argument("--top-errors", type=int, default=5, help="Количество самых частых ошибок для вывода.")

    args = parser.parse_args()

    # Словарь для выбора нужного парсера
    parsers = {
        'regex': RegexParser(),
        'json': JSONParser()
    }

    # Словарь для выбора нужного генератора отчета
    reporters = {
        'markdown': MarkdownReporter(),
        'html': HTMLReporter()
    }

    # Определяем имя выходного файла по умолчанию, если оно не указано
    if not args.output:
        extension = 'md' if args.report == 'markdown' else 'html'
        args.output = f"report.{extension}"

    print(f"[{datetime.now()}] Начало анализа файла: {args.logfile}")

    try:
        # 1. Выбор парсера и парсинг лог-файла
        log_parser = parsers.get(args.parser)
        if not log_parser:
            print(f"Ошибка: Неизвестный тип парсера '{args.parser}'")
            return

        print(f"[{datetime.now()}] Используется парсер: {args.parser}")
        log_dataframe = log_parser.parse(args.logfile)

        if log_dataframe.empty:
            print(f"[{datetime.now()}] Внимание: После парсинга не найдено данных в файле.")
            return

        print(f"[{datetime.now()}] Файл успешно распарсен. Найдено записей: {len(log_dataframe)}")

        # 2. Анализ данных
        analyzer = Analyzer(log_dataframe)
        analysis_results = analyzer.analyze(top_n_errors=args.top_errors)
        print(f"[{datetime.now()}] Анализ данных завершен.")

        # 3. Генерация отчета
        report_generator = reporters.get(args.report)
        if not report_generator:
            print(f"Ошибка: Неизвестный тип отчета '{args.report}'")
            return

        report_generator.generate(analysis_results, args.output)
        print(f"[{datetime.now()}] Отчет успешно сгенерирован и сохранен в файл: {args.output}")

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути '{args.logfile}'")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
