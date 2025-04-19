import * as chromeLauncher from "chrome-launcher";
import lighthouse from "lighthouse";
import config from "../config/lighthouse.config.js";

/**
Функция выполняет аудит страницы с помощью Lighthouse и возвращает результаты.
  - Запускает Chrome в режиме headless с использованием chrome-launcher.
  - Настроены параметры аудита, включая уровень логирования, формат вывода (json) и порт для подключения к Chrome.
  - Выполняет аудит страницы через Lighthouse, используя переданный URL и настройки из конфигурации.
  - Извлекает ключевые данные из результатов аудита, включая показатели по производительности, SEO, доступности, безопасности (SSL) и HTTP статусу.
  - Закрывает Chrome после завершения аудита.
  - Возвращает объект с результатами аудита для дальнейшего анализа.
*/

export const runAudit = async (url) => {
  const chrome = await chromeLauncher.launch({ chromeFlags: ["--headless"] });

  const options = {
    logLevel: "silent",
    output: "json",
    port: chrome.port,
  };

  const runnerResult = await lighthouse(url, options, config);

  const lhr = runnerResult.lhr;

  const scores = {
    url: lhr.finalUrl,
    fetchTime: lhr.fetchTime,

    performance: [
      lhr.audits["first-contentful-paint"],
      lhr.audits["speed-index"],
      lhr.audits["interactive"],
      lhr.audits["total-blocking-time"],
      lhr.audits["largest-contentful-paint"],
      lhr.audits["cumulative-layout-shift"],
    ],

    seo: [
      lhr.audits["document-title"],
      lhr.audits["meta-description"],
      lhr.audits["http-status-code"],
      lhr.audits["is-crawlable"],
      lhr.audits["viewport"],
      lhr.audits["font-size"],
      lhr.audits["tap-targets"],
    ],

    accessibility: [
      lhr.audits["color-contrast"],
      lhr.audits["image-alt"],
      lhr.audits["label"],
      lhr.audits["tabindex"],
    ],

    ssl: [
      lhr.audits["is-on-https"],
      lhr.audits["redirects-http"],
      lhr.audits["uses-http2"],
    ],

    httpCode: [lhr.audits["http-status-code"]],
  };

  chrome.kill();

  return scores;
};
