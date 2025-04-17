export default {
  extends: "lighthouse:default",
  settings: {
    onlyAudits: [
      // performance
      "first-contentful-paint",
      "speed-index",
      "interactive",
      "total-blocking-time",
      "largest-contentful-paint",
      "cumulative-layout-shift",

      // seo
      "document-title",
      "meta-description",
      "is-crawlable",
      "viewport",
      "font-size",
      "tap-targets",

      // accessibility
      "color-contrast",
      "image-alt",
      "label",
      "tabindex",

      // SSL
      "is-on-https",
      "uses-http2",
      "redirects-http",

      // HTTP-codes
      "http-status-code",
    ],
  },
};
