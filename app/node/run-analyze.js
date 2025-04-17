import { runAudit } from "./audit/run-audit.js";
import { saveReports } from "./save-reports/save-reports.js";

async function main() {
  const url = process.argv[2];

  const filenameFromArg = process.argv.find((arg) =>
    arg.startsWith("--filename="),
  );
  const filename = filenameFromArg ? filenameFromArg.split("=")[1] : "default";

  if (!url) {
    throw new Error(
      "Укажите ссылку для проведения аудита, например, yarn start https://example.com",
    );
  }

  const report = await runAudit(url);
  saveReports(report, filename);
}

main();
