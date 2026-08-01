const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const codePath = path.join(__dirname, "..", "Code.gs");
const source = fs.readFileSync(codePath, "utf8");

let uuidCounter = 0;
const context = {
  console,
  Date,
  Object,
  String,
  Number,
  Boolean,
  RegExp,
  JSON,
  Math,
  Set,
  Map,
  Error,
  encodeURIComponent,
  Utilities: {
    getUuid() {
      uuidCounter += 1;
      return `12345678-1234-1234-1234-${String(uuidCounter).padStart(12, "0")}`;
    },
    formatDate(date, _timezone, format) {
      assert.equal(format, "yyyyMMdd");
      const yyyy = date.getUTCFullYear();
      const mm = String(date.getUTCMonth() + 1).padStart(2, "0");
      const dd = String(date.getUTCDate()).padStart(2, "0");
      return `${yyyy}${mm}${dd}`;
    },
  },
  Session: {
    getScriptTimeZone() {
      return "Asia/Tokyo";
    },
  },
  ScriptApp: {
    getService() {
      return { getUrl: () => "https://script.google.com/macros/s/test/exec" };
    },
  },
};

vm.createContext(context);
vm.runInContext(
  `${source}\nthis.__testExports = {\n    normalizeLeadPayload_,\n    validateLeadPayload_,\n    normalizeXHandle_,\n    isValidEmail_,\n    buildLeadId_,\n    buildDeliveryId_,\n    buildKitEmailHtml_,\n    positiveInteger_,\n  };`,
  context,
  { filename: "Code.gs" },
);

const f = context.__testExports;

const normalized = f.normalizeLeadPayload_({
  channelEmail: true,
  email: " Test@Example.com ",
  consentDelivery: true,
  consentUpdates: true,
});
assert.equal(normalized.email, "test@example.com");
assert.equal(normalized.channels.email, true);
assert.doesNotThrow(() => f.validateLeadPayload_(normalized));

assert.throws(
  () => f.validateLeadPayload_(f.normalizeLeadPayload_({ consentDelivery: true })),
  /最低一つ/,
);
assert.throws(
  () =>
    f.validateLeadPayload_(
      f.normalizeLeadPayload_({
        channelEmail: true,
        email: "bad",
        consentDelivery: true,
      }),
    ),
  /有効なメール/,
);
assert.equal(f.normalizeXHandle_("example_123"), "@example_123");
assert.throws(() => f.normalizeXHandle_("bad-handle"), /Xアカウント名/);
assert.equal(f.isValidEmail_("a@example.com"), true);
assert.equal(f.isValidEmail_("a@localhost"), false);

const date = new Date("2026-08-01T00:00:00Z");
assert.match(f.buildLeadId_(date), /^LD-20260801-[A-F0-9]{8}$/);
assert.match(f.buildDeliveryId_(date), /^DL-20260801-[A-F0-9]{10}$/);

const html = f.buildKitEmailHtml_(
  {
    display_name: "利用者",
    lead_id: "LD-20260801-ABCDEF12",
    unsubscribe_token: "unsubscribe-token",
  },
  { kit_version: "v0.1.0" },
  {
    KIT_NAME: "限界開発スターターキット",
    KIT_URL: "https://example.test/kit",
    WEB_APP_URL: "https://script.google.com/macros/s/test/exec",
  },
);
assert.match(html, /unsubscribe/);
assert.match(html, /スターターキットを受け取る/);

assert.equal(f.positiveInteger_("20", 3), 20);
assert.equal(f.positiveInteger_("0", 3), 3);

assert.match(source, /getRemainingDailyQuota/);
assert.match(source, /MANUAL_REQUIRED/);
assert.match(source, /confirmUnsubscribe/);

console.log("Limit Lead Hub static contract tests: PASS");
