import fs from "fs";
import path from "path";

/**
Функция сохраняет отчет в формате JSON в указанную директорию.
  - Если имя файла не указано (значение "default"), имя файла будет основано на текущей дате в формате YYYY-MM-DD.
  - В противном случае файл будет сохранен с указанным именем.
  - Отчет сохраняется в папке `reports_output` на уровне выше текущего модуля.
  - Для сохранения используется метод `fs.writeFileSync`, который записывает JSON-объект в файл.
 */
export const saveReports = (report, filename) => {
  const __dirname = import.meta.dirname;
  const currentDate = new Date();

  if (filename === "default") {
    const pathToReports = path.join(
      __dirname,
      "../../../reports_output",
      `${currentDate.toISOString().split("T")[0]}.json`,
    );

    fs.writeFileSync(pathToReports, JSON.stringify(report));

    return;
  }

  const pathToReports = path.join(
    __dirname,
    "../../../reports_output",
    `${filename}.json`,
  );

  fs.writeFileSync(pathToReports, JSON.stringify(report));
};
