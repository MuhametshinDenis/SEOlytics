import json
import os
import subprocess

from PyQt5.QtCore import pyqtSignal, QObject

from app.core.analyze_reports import analyze_reports
from app.reports.html_report import generate_html_report
from app.reports.xlsx_report import generate_xlsx_report

"""
Класс AnalysisWorker отвечает за выполнение процесса анализа отчета в отдельном потоке.
Он принимает URL, имя файла и формат отчета, затем:
    - запускает внешний процесс через npm
    - анализирует собранные данные
    - формирует итоговый отчет в нужном формате
"""
class AnalysisWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    # Конструктор
    def __init__(self, url, filename, format_report):
        super().__init__()
        self.url = url
        self.filename = filename
        self.format_report = format_report

    # Основной метод выполнения анализа
    def run(self):
        try:
            os.makedirs("reports_output", exist_ok=True)

            self.progress.emit(10)
            command = f"npm start -- {self.url} --filename={self.filename}"
            subprocess.run(command, shell=True, check=True)
            self.progress.emit(50)

            with open(f'./reports_output/{self.filename}.json', 'r', encoding='UTF-8') as file:
                data = json.load(file)

            result = analyze_reports(data)
            self.progress.emit(75)

            if self.format_report == 'Excel':
                generate_xlsx_report(report=result, filename=self.filename)
            elif self.format_report == 'Html':
                generate_html_report(report=result, filename=self.filename)
            elif self.format_report == 'Оба':
                generate_xlsx_report(report=result, filename=self.filename)
                generate_html_report(report=result, filename=self.filename)

            self.progress.emit(100)
        except Exception as e:
            print(f"Ошибка при анализе: {e}")
        finally:
            self.finished.emit()