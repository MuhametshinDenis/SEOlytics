from app.utils.logger.application_logger import ApplicationLogger

"""
Функция анализирует отчет Lighthouse, извлекая данные по каждой категории.
Для каждой категории рассчитывается средний балл и собираются проблемы, у которых балл меньше или равен 0.8.
Возвращает словарь с результатами анализа: средний балл по каждой категории и список проблем.
"""
def analyze_reports(report):
    log = ApplicationLogger()
    analysis_result = {}

    log.info(f'Начался анализ страницы {report["url"]}')

    for category, audits in report.items():
        if category in ("url", "fetchTime"):
            continue

        scores = []
        issues = []

        for audit in audits:
            if audit is None:
                continue

            score = audit.get("score")
            mode = audit.get("scoreDisplayMode")

            if score is not None and mode != "notApplicable":
                scores.append(score)

                if score <= 0.8:
                    issues.append({
                        "id": audit.get("id"),
                        "title": audit.get("title"),
                        "score": score,
                        "description": audit.get("description"),
                        "displayValue": audit.get("displayValue")
                    })

        average_score = round(sum(scores) / len(scores), 2) if scores else 0.0
        analysis_result[category] = {
            "averageScore": average_score,
            "issuesBelowThreshold": issues
        }
        
    log.info("Анализ документа завершен!")

    return analysis_result
