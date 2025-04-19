import xlsxwriter

from app.utils.logger.application_logger import ApplicationLogger


"""
Функция генерирует отчет в формате Excel (.xlsx) на основе данных из отчета 'report'.
Для каждой секции создается отдельный лист в Excel-файле, где записываются следующие данные:
	- averageScore для каждой категории.
	- Для каждой проблемы в секции записываются данные: ID, Title, Score, Description, DisplayValue.
Если проблем нет в секции, то только записывается средний балл.
Файл сохраняется в папке './reports_output' с именем 'filename'.
"""
def generate_xlsx_report(report,  filename = 'seolitics_report'):
	log = ApplicationLogger()
	workbook = xlsxwriter.Workbook(f'./reports_output/{filename}.xlsx')

	headers = ['averageScore', 'id', 'title', 'score', 'description', 'displayValue']

	header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC'})

	for section, content in report.items():
			worksheet = workbook.add_worksheet(section[:31])
			worksheet.write_row(0, 0, headers, header_format)

			avg = content['averageScore']
			issues = content['issuesBelowThreshold']
			row = 1

			if issues:
					for issue in issues:
							worksheet.write(row, 0, avg)
							worksheet.write(row, 1, issue.get('id'))
							worksheet.write(row, 2, issue.get('title'))
							worksheet.write(row, 3, issue.get('score'))
							worksheet.write(row, 4, issue.get('description'))
							worksheet.write(row, 5, issue.get('displayValue'))
							row += 1
			else:
					worksheet.write(row, 0, avg)

			for col in range(len(headers)):
					worksheet.set_column(col, col, 30)

	workbook.close()
	log.info(f'Xlsx report saved to {filename}.xlsx')