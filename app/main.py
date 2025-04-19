import json
import os
import subprocess
import time
import schedule
from yaspin import yaspin
from InquirerPy import inquirer
from app.core.analyze_reports import analyze_reports
from app.reports.html_report import generate_html_report
from app.reports.xlsx_report import generate_xlsx_report
from app.scheduled_runner import run_daily_report
from app.utils.logger.application_logger import ApplicationLogger


def main():
	logger = ApplicationLogger()

	choice_operating_mode = [
		{"name": "Постоянный режим работы", "value": "regular"},
		{"name": "Единоразовый режим работы", "value": "one-time"},
	]

	operating_mode = inquirer.select(
		message="Выберите режим работы:",
		choices=choice_operating_mode,
		default=choice_operating_mode[1]["value"]
	).execute()

	if (operating_mode == "regular"):
		run_daily_report()

		task_run_time = input("Введите время запуска программы, например, 12:10:00 или 09:02:00: ")

		logger.success("Ежедневный запуск установлен!")
		schedule.every().day.at(task_run_time).do(run_daily_report)

		while True:
			schedule.run_pending()
			time.sleep(1)
	
	url = input("Введите url сайта: ")

	with yaspin(text="Анализ сайта....", color="cyan") as spinner:
		os.makedirs("reports_output", exist_ok=True)
		command = f"npm start -- {url}"
		subprocess.run(command, shell=True)
		spinner.ok("Успешный ")

	choice_file = []

	for file in os.listdir("./reports_output"):
		if file.endswith(".json"):
			choice_file.append(file)

	selected_filename = inquirer.select(
		message="Выберите файл: ",
		choices=choice_file
	).execute()

	with open(f'./reports_output/{selected_filename}', 'r', encoding='UTF-8') as file:
		data = json.load(file)

	result = analyze_reports(data)

	choice_generated_format = [
		{"name": "Сгенерировать только Xlsx", "value": "xlsx"},
		{"name": "Сгенерировать только Html", "value": "html"},
		{"name": "Сгенерировать все", "value": "all"},
		{"name": "Выйти", "value": "exit"}
	]

	format_generated_report = inquirer.select(
			message="Выберите действие:",
			choices=choice_generated_format,
			default=choice_generated_format[2]["value"],
	).execute()

	if format_generated_report == 'xlsx':
		generate_xlsx_report(report=result)
	elif format_generated_report == 'html':
		generate_html_report(report=result)
	elif format_generated_report == 'all':
		generate_xlsx_report(report=result)
		generate_html_report(report=result)
	elif format_generated_report == 'exit':
		exit()
