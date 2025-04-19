import json
import os
import subprocess
import schedule
from InquirerPy import inquirer
from app.config import ApplicationConfig
from app.core.analyze_reports import analyze_reports
from app.reports.html_report import generate_html_report
from app.reports.xlsx_report import generate_xlsx_report
from app.utils.logger.application_logger import ApplicationLogger

def run_daily_report():
	config = ApplicationConfig()
	logger = ApplicationLogger()

	url = config.get("APPLICATION", "URL")
	filename = config.get("APPLICATION", "FILENAME")

	if (url is None) or (filename is None):
		url = input("Введите url сайта: ")
		config.set("APPLICATION", "URL", url)

		filename = input("Введите название для отчета: ")
		config.set("APPLICATION", "FILENAME", filename)

	os.makedirs("reports_output", exist_ok=True)

	command = f"npm start -- {config.get("APPLICATION", "URL")} --filename={config.get("APPLICATION", "FILENAME")}"

	logger.info("Запущен анализ сайта")

	subprocess.run(command, shell=True)

	logger.info("Успешно проанализирован сайт")

	with open(f'./reports_output/{config.get("APPLICATION", "FILENAME")}.json', 'r', encoding='UTF-8') as file:
		data = json.load(file)

	result = analyze_reports(data)

	generate_report = config.get("APPLICATION", "GENERATE_REPORT")

	if generate_report is None:
		choice_generated_format = [
			{"name": "Сгенерировать только Xlsx", "value": "xlsx"},
			{"name": "Сгенерировать только Html", "value": "html"},
			{"name": "Сгенерировать все", "value": "all"}
		]

		format_generated_report = inquirer.select(
				message="Выберите действие:",
				choices=choice_generated_format,
				default=choice_generated_format[2]["value"],
		).execute()

		config.set("APPLICATION", "GENERATE_REPORT", format_generated_report)

	filename = config.get("APPLICATION", "FILENAME")

	if config.get("APPLICATION", "GENERATE_REPORT") == 'xlsx':
		generate_xlsx_report(report=result, filename=filename)
	elif config.get("APPLICATION", "GENERATE_REPORT") == 'html':
		generate_html_report(report=result, filename=filename)
	elif config.get("APPLICATION", "GENERATE_REPORT") == 'all':
		generate_xlsx_report(report=result, filename=filename)
		generate_html_report(report=result, filename=filename)

	config.save()