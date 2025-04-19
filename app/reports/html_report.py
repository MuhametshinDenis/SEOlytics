from pathlib import Path

from app.utils.logger.application_logger import ApplicationLogger

"""
Функция генерирует HTML отчет на основе данных, предоставленных в объекте 'report'.
Для каждой секции отчета выводится средний балл, который отображается с соответствующим стилем (в зависимости от значения).
Если есть проблемы, они выводятся в виде таблицы с идентификатором, названием, баллом, описанием и значением для отображения.
Если проблем нет, отображается сообщение "No problems found".
Итоговый HTML сохраняется в файл с именем 'filename' в папке './reports_output'.
"""
def generate_html_report(report, filename = 'seolitics_report'):
    log = ApplicationLogger()
    html_parts = []

    html_parts.append("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SEOlitics Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            h2 { background: #333; color: white; padding: 10px; border-radius: 5px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #eee; }
            .score-high { color: green; font-weight: bold; }
            .score-low { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
    <h1>SEOlitics Report</h1>
    """)

    for section, content in report.items():
        avg = content['averageScore']
        issues = content['issuesBelowThreshold']

        html_parts.append(f'<h2>{section.title()} (Average Score: <span class="{ "score-high" if avg >= 0.9 else "score-low" if avg < 0.5 else ""}">{avg:.2f}</span>)</h2>')

        if not issues:
            html_parts.append('<p><em>No problems found</em></p>')
            continue

        html_parts.append("""
        <table>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Score</th>
                <th>Description</th>
                <th>Display Value</th>
            </tr>
        """)

        for issue in issues:
            score = issue['score']
            score_class = 'score-high' if score >= 0.9 else 'score-low' if score < 0.5 else ''
            html_parts.append(f"""
                <tr>
                    <td>{issue.get('id')}</td>
                    <td>{issue.get('title')}</td>
                    <td class="{score_class}">{score:.2f}</td>
                    <td>{issue.get('description')}</td>
                    <td>{issue.get('displayValue') or ''}</td>
                </tr>
            """)

        html_parts.append('</table>')

    html_parts.append('</body></html>')

    Path(f'./reports_output/{filename}.html').write_text(''.join(html_parts), encoding='utf-8')
    
    log.info(f'HTML report saved to {filename}.html')

