import fs from "fs";
import path from "path";

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
