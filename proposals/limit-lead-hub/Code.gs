/**
 * Limit Lead Hub MVP
 * Google Apps Script web app + Google Sheets ledger.
 *
 * External delivery rules:
 * - Email: queued and sent through MailApp under a configurable safety cap.
 * - LINE: user-initiated contact, then manual reply.
 * - X: user-initiated DM/reply, then manual reply.
 *
 * No secrets belong in source. Runtime values live in the Config sheet or
 * Script Properties.
 */

const LLH = Object.freeze({
  SHEETS: Object.freeze({
    LEADS: "Leads",
    DELIVERIES: "Deliveries",
    AUDIT: "Audit",
    CONFIG: "Config",
  }),
  DELIVERY_STATUS: Object.freeze({
    PENDING: "PENDING",
    SENT: "SENT",
    FAILED: "FAILED",
    CANCELLED: "CANCELLED",
    MANUAL_REQUIRED: "MANUAL_REQUIRED",
  }),
  LEAD_STATUS: Object.freeze({
    ACTIVE: "ACTIVE",
    UNSUBSCRIBED: "UNSUBSCRIBED",
    BLOCKED: "BLOCKED",
  }),
  CHANNELS: Object.freeze(["email", "line", "x"]),
  DEFAULTS: Object.freeze({
    CURRENT_KIT_VERSION: "v0.1.0",
    KIT_NAME: "限界開発スターターキット",
    KIT_URL: "https://example.com/replace-me",
    LINE_ADD_URL: "https://line.me/R/ti/p/@replace-me",
    X_PROFILE_URL: "https://x.com/replace-me",
    ADMIN_EMAIL: "",
    MAIL_SAFETY_CAP_PER_RUN: "20",
    MAIL_SAFETY_CAP_PER_DAY: "80",
    WEB_APP_URL: "",
    PRIVACY_POLICY_URL: "",
    SENDER_NAME: "限界開発",
  }),
});

const LEAD_HEADERS = Object.freeze([
  "lead_id",
  "created_at",
  "updated_at",
  "status",
  "display_name",
  "email",
  "line_name",
  "x_handle",
  "preferred_channel",
  "channel_email",
  "channel_line",
  "channel_x",
  "consent_delivery",
  "consent_updates",
  "consent_offers",
  "consent_text_version",
  "source",
  "current_kit_version",
  "unsubscribe_token",
  "last_delivery_at",
  "notes",
]);

const DELIVERY_HEADERS = Object.freeze([
  "delivery_id",
  "lead_id",
  "created_at",
  "updated_at",
  "channel",
  "destination",
  "kit_version",
  "status",
  "attempts",
  "last_attempt_at",
  "sent_at",
  "error_code",
  "error_message",
  "operator_note",
]);

const AUDIT_HEADERS = Object.freeze([
  "audit_id",
  "created_at",
  "actor",
  "event_type",
  "lead_id",
  "delivery_id",
  "details_json",
]);

const CONFIG_HEADERS = Object.freeze(["key", "value", "description"]);

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Limit Lead Hub")
    .addItem("初期セットアップ", "setupLimitLeadHub_")
    .addItem("トリガーを設定", "installLimitLeadHubTriggers_")
    .addSeparator()
    .addItem("メールキューを処理", "processDeliveryQueue_")
    .addItem("LINE/X手動配布を完了", "markManualDeliveryFromUi_")
    .addItem("設定を検証", "validateLimitLeadHubConfig_")
    .addToUi();
}

function doGet(e) {
  const action = String((e && e.parameter && e.parameter.action) || "form");
  if (action === "unsubscribe") {
    return renderUnsubscribePage_(e);
  }

  const template = HtmlService.createTemplateFromFile("Form");
  const config = getConfig_();
  template.appConfig = {
    kitName: config.KIT_NAME,
    kitVersion: config.CURRENT_KIT_VERSION,
    lineAddUrl: config.LINE_ADD_URL,
    xProfileUrl: config.X_PROFILE_URL,
    privacyPolicyUrl: config.PRIVACY_POLICY_URL,
  };
  return template.evaluate().setTitle(`${config.KIT_NAME} 受取申請`);
}

function setupLimitLeadHub_() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    throw new Error("Google Sheets に紐づいた Apps Script として実行してください。");
  }

  ensureSheet_(spreadsheet, LLH.SHEETS.LEADS, LEAD_HEADERS);
  ensureSheet_(spreadsheet, LLH.SHEETS.DELIVERIES, DELIVERY_HEADERS);
  ensureSheet_(spreadsheet, LLH.SHEETS.AUDIT, AUDIT_HEADERS);
  const configSheet = ensureSheet_(spreadsheet, LLH.SHEETS.CONFIG, CONFIG_HEADERS);
  seedConfig_(configSheet);

  PropertiesService.getScriptProperties().setProperty(
    "SPREADSHEET_ID",
    spreadsheet.getId(),
  );

  appendAudit_("SYSTEM", "SETUP_COMPLETED", "", "", {
    spreadsheetId: spreadsheet.getId(),
  });

  return {
    ok: true,
    spreadsheetId: spreadsheet.getId(),
    message: "初期セットアップが完了しました。Config シートを確認してください。",
  };
}

function installLimitLeadHubTriggers_() {
  const existing = ScriptApp.getProjectTriggers();
  for (const trigger of existing) {
    if (trigger.getHandlerFunction() === "processDeliveryQueue_") {
      ScriptApp.deleteTrigger(trigger);
    }
  }

  ScriptApp.newTrigger("processDeliveryQueue_")
    .timeBased()
    .everyMinutes(15)
    .create();

  appendAudit_("SYSTEM", "TRIGGER_INSTALLED", "", "", {
    handler: "processDeliveryQueue_",
    cadence: "every_15_minutes",
  });

  return { ok: true, message: "15分ごとのメールキュー処理を設定しました。" };
}

function submitLead(payload) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    assertInitialized_();
    const normalized = normalizeLeadPayload_(payload || {});
    validateLeadPayload_(normalized);

    const now = new Date();
    const leadId = buildLeadId_(now);
    const unsubscribeToken = Utilities.getUuid().replace(/-/g, "");
    const config = getConfig_();

    const leadRecord = {
      lead_id: leadId,
      created_at: now,
      updated_at: now,
      status: LLH.LEAD_STATUS.ACTIVE,
      display_name: normalized.displayName,
      email: normalized.email,
      line_name: normalized.lineName,
      x_handle: normalized.xHandle,
      preferred_channel: normalized.preferredChannel,
      channel_email: normalized.channels.email,
      channel_line: normalized.channels.line,
      channel_x: normalized.channels.x,
      consent_delivery: normalized.consentDelivery,
      consent_updates: normalized.consentUpdates,
      consent_offers: normalized.consentOffers,
      consent_text_version: "2026-08-01-v1",
      source: normalized.source,
      current_kit_version: config.CURRENT_KIT_VERSION,
      unsubscribe_token: unsubscribeToken,
      last_delivery_at: "",
      notes: normalized.notes,
    };

    appendObjectRow_(LLH.SHEETS.LEADS, LEAD_HEADERS, leadRecord);

    const instructions = [];
    if (normalized.channels.email) {
      createDelivery_(leadId, "email", normalized.email, config.CURRENT_KIT_VERSION);
      instructions.push("メール送信キューへ登録しました。届かない場合は迷惑メールも確認してください。");
    }

    if (normalized.channels.line) {
      createDelivery_(leadId, "line", normalized.lineName, config.CURRENT_KIT_VERSION);
      instructions.push(
        `LINE公式アカウントを追加し、「KIT ${leadId}」と送ってください。`,
      );
    }

    if (normalized.channels.x) {
      createDelivery_(leadId, "x", normalized.xHandle, config.CURRENT_KIT_VERSION);
      instructions.push(
        `XでDMまたは指定投稿への返信として「KIT ${leadId}」と送ってください。`,
      );
    }

    appendAudit_("PUBLIC_FORM", "LEAD_CREATED", leadId, "", {
      channels: Object.keys(normalized.channels).filter(
        (channel) => normalized.channels[channel],
      ),
      consentUpdates: normalized.consentUpdates,
      consentOffers: normalized.consentOffers,
      kitVersion: config.CURRENT_KIT_VERSION,
    });

    return {
      ok: true,
      leadId,
      kitVersion: config.CURRENT_KIT_VERSION,
      instructions,
      lineAddUrl: config.LINE_ADD_URL,
      xProfileUrl: config.X_PROFILE_URL,
    };
  } catch (error) {
    appendAuditSafe_("PUBLIC_FORM", "LEAD_CREATE_FAILED", "", "", {
      errorType: error && error.name ? error.name : "Error",
      message: safeErrorMessage_(error),
    });
    throw new Error(safeErrorMessage_(error));
  } finally {
    lock.releaseLock();
  }
}

function processDeliveryQueue_() {
  assertInitialized_();
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) {
    return { ok: false, message: "別のキュー処理が実行中です。" };
  }

  try {
    const config = getConfig_();
    const perRunCap = positiveInteger_(config.MAIL_SAFETY_CAP_PER_RUN, 20);
    const perDayCap = positiveInteger_(config.MAIL_SAFETY_CAP_PER_DAY, 80);
    const remainingQuota = MailApp.getRemainingDailyQuota();
    const alreadySentToday = countEmailDeliveriesSentToday_();
    const remainingDailySafety = Math.max(0, perDayCap - alreadySentToday);
    const sendBudget = Math.max(
      0,
      Math.min(perRunCap, remainingQuota, remainingDailySafety),
    );

    if (sendBudget < 1) {
      appendAudit_("SYSTEM", "EMAIL_QUEUE_SKIPPED", "", "", {
        remainingQuota,
        remainingDailySafety,
        alreadySentToday,
      });
      return {
        ok: true,
        sent: 0,
        message: "安全上限またはMailApp残量に達したため、今回は送信しませんでした。",
      };
    }

    const deliverySheet = getSheet_(LLH.SHEETS.DELIVERIES);
    const values = deliverySheet.getDataRange().getValues();
    const headerMap = headerIndexMap_(values[0]);
    let sent = 0;
    let failed = 0;

    for (let rowIndex = 1; rowIndex < values.length && sent < sendBudget; rowIndex += 1) {
      const row = values[rowIndex];
      if (
        String(row[headerMap.channel]) !== "email" ||
        String(row[headerMap.status]) !== LLH.DELIVERY_STATUS.PENDING
      ) {
        continue;
      }

      const delivery = rowToObject_(values[0], row);
      const lead = findLeadById_(String(delivery.lead_id));
      if (!lead || String(lead.status) !== LLH.LEAD_STATUS.ACTIVE) {
        updateDeliveryRow_(deliverySheet, rowIndex + 1, headerMap, {
          status: LLH.DELIVERY_STATUS.CANCELLED,
          updated_at: new Date(),
          error_code: "LEAD_INACTIVE",
          error_message: "Lead is missing or inactive.",
        });
        continue;
      }

      if (!toBoolean_(lead.consent_delivery)) {
        updateDeliveryRow_(deliverySheet, rowIndex + 1, headerMap, {
          status: LLH.DELIVERY_STATUS.CANCELLED,
          updated_at: new Date(),
          error_code: "NO_DELIVERY_CONSENT",
          error_message: "One-time delivery consent is not present.",
        });
        continue;
      }

      try {
        const attemptTime = new Date();
        const attempts = Number(delivery.attempts || 0) + 1;
        MailApp.sendEmail({
          to: String(delivery.destination),
          subject: `【${config.KIT_NAME}】受取リンク ${delivery.kit_version}`,
          htmlBody: buildKitEmailHtml_(lead, delivery, config),
          name: config.SENDER_NAME,
        });

        updateDeliveryRow_(deliverySheet, rowIndex + 1, headerMap, {
          status: LLH.DELIVERY_STATUS.SENT,
          updated_at: attemptTime,
          attempts,
          last_attempt_at: attemptTime,
          sent_at: attemptTime,
          error_code: "",
          error_message: "",
        });
        updateLeadLastDelivery_(String(delivery.lead_id), attemptTime);
        appendAudit_("SYSTEM", "EMAIL_SENT", String(delivery.lead_id), String(delivery.delivery_id), {
          kitVersion: delivery.kit_version,
        });
        sent += 1;
      } catch (error) {
        const attemptTime = new Date();
        const attempts = Number(delivery.attempts || 0) + 1;
        updateDeliveryRow_(deliverySheet, rowIndex + 1, headerMap, {
          status: attempts >= 3 ? LLH.DELIVERY_STATUS.FAILED : LLH.DELIVERY_STATUS.PENDING,
          updated_at: attemptTime,
          attempts,
          last_attempt_at: attemptTime,
          error_code: error && error.name ? error.name : "SEND_ERROR",
          error_message: safeErrorMessage_(error),
        });
        appendAudit_("SYSTEM", "EMAIL_SEND_FAILED", String(delivery.lead_id), String(delivery.delivery_id), {
          attempts,
          errorType: error && error.name ? error.name : "Error",
        });
        failed += 1;
      }
    }

    return {
      ok: true,
      sent,
      failed,
      remainingQuotaBeforeRun: remainingQuota,
      message: `${sent}件送信、${failed}件失敗。`,
    };
  } finally {
    lock.releaseLock();
  }
}

function markManualDelivery_(leadId, channel, operatorNote) {
  assertInitialized_();
  const normalizedChannel = String(channel || "").toLowerCase();
  if (!["line", "x"].includes(normalizedChannel)) {
    throw new Error("手動完了にできるチャネルは line または x です。");
  }

  const sheet = getSheet_(LLH.SHEETS.DELIVERIES);
  const values = sheet.getDataRange().getValues();
  const headers = values[0];
  const headerMap = headerIndexMap_(headers);

  for (let rowIndex = values.length - 1; rowIndex >= 1; rowIndex -= 1) {
    const row = values[rowIndex];
    if (
      String(row[headerMap.lead_id]) === String(leadId) &&
      String(row[headerMap.channel]) === normalizedChannel &&
      [LLH.DELIVERY_STATUS.MANUAL_REQUIRED, LLH.DELIVERY_STATUS.PENDING].includes(
        String(row[headerMap.status]),
      )
    ) {
      const now = new Date();
      updateDeliveryRow_(sheet, rowIndex + 1, headerMap, {
        status: LLH.DELIVERY_STATUS.SENT,
        updated_at: now,
        attempts: Number(row[headerMap.attempts] || 0) + 1,
        last_attempt_at: now,
        sent_at: now,
        operator_note: String(operatorNote || "manual delivery confirmed"),
      });
      updateLeadLastDelivery_(String(leadId), now);
      appendAudit_("ADMIN", "MANUAL_DELIVERY_CONFIRMED", String(leadId), String(row[headerMap.delivery_id]), {
        channel: normalizedChannel,
      });
      return { ok: true, leadId, channel: normalizedChannel };
    }
  }

  throw new Error("該当する未完了の配布レコードが見つかりません。");
}

function unsubscribeLead_(token, scope) {
  assertInitialized_();
  const normalizedToken = String(token || "").trim();
  const normalizedScope = String(scope || "all").toLowerCase();
  if (!normalizedToken) {
    throw new Error("配信停止トークンがありません。");
  }

  const sheet = getSheet_(LLH.SHEETS.LEADS);
  const values = sheet.getDataRange().getValues();
  const headers = values[0];
  const headerMap = headerIndexMap_(headers);

  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    if (String(values[rowIndex][headerMap.unsubscribe_token]) !== normalizedToken) {
      continue;
    }

    const rowNumber = rowIndex + 1;
    const now = new Date();
    if (normalizedScope === "updates") {
      sheet.getRange(rowNumber, headerMap.consent_updates + 1).setValue(false);
      sheet.getRange(rowNumber, headerMap.updated_at + 1).setValue(now);
      appendAudit_("PUBLIC_UNSUBSCRIBE", "UPDATES_UNSUBSCRIBED", String(values[rowIndex][headerMap.lead_id]), "", {});
      return { ok: true, scope: "updates" };
    }

    if (normalizedScope === "offers") {
      sheet.getRange(rowNumber, headerMap.consent_offers + 1).setValue(false);
      sheet.getRange(rowNumber, headerMap.updated_at + 1).setValue(now);
      appendAudit_("PUBLIC_UNSUBSCRIBE", "OFFERS_UNSUBSCRIBED", String(values[rowIndex][headerMap.lead_id]), "", {});
      return { ok: true, scope: "offers" };
    }

    sheet.getRange(rowNumber, headerMap.consent_updates + 1).setValue(false);
    sheet.getRange(rowNumber, headerMap.consent_offers + 1).setValue(false);
    sheet.getRange(rowNumber, headerMap.status + 1).setValue(LLH.LEAD_STATUS.UNSUBSCRIBED);
    sheet.getRange(rowNumber, headerMap.updated_at + 1).setValue(now);
    cancelPendingEmailDeliveries_(String(values[rowIndex][headerMap.lead_id]));
    appendAudit_("PUBLIC_UNSUBSCRIBE", "ALL_UNSUBSCRIBED", String(values[rowIndex][headerMap.lead_id]), "", {});
    return { ok: true, scope: "all" };
  }

  throw new Error("配信停止対象が見つかりません。");
}

function validateLimitLeadHubConfig_() {
  assertInitialized_();
  const config = getConfig_();
  const problems = [];

  if (!/^https:\/\//i.test(config.KIT_URL)) {
    problems.push("KIT_URL は https:// で始まるURLにしてください。");
  }
  if (config.KIT_URL.includes("example.com/replace-me")) {
    problems.push("KIT_URL が初期値のままです。");
  }
  if (config.LINE_ADD_URL && !/^https:\/\//i.test(config.LINE_ADD_URL)) {
    problems.push("LINE_ADD_URL は空欄または https:// URLにしてください。");
  }
  if (config.X_PROFILE_URL && !/^https:\/\//i.test(config.X_PROFILE_URL)) {
    problems.push("X_PROFILE_URL は空欄または https:// URLにしてください。");
  }
  if (config.PRIVACY_POLICY_URL && !/^https:\/\//i.test(config.PRIVACY_POLICY_URL)) {
    problems.push("PRIVACY_POLICY_URL は空欄または https:// URLにしてください。");
  }

  const result = { ok: problems.length === 0, problems, config: redactConfig_(config) };
  SpreadsheetApp.getUi().alert(
    result.ok ? "設定検証: PASS" : `設定検証: FAIL\n\n${problems.join("\n")}`,
  );
  return result;
}

function renderUnsubscribePage_(e) {
  const template = HtmlService.createTemplateFromFile("Unsubscribe");
  template.token = String((e && e.parameter && e.parameter.token) || "");
  template.scope = String((e && e.parameter && e.parameter.scope) || "all");
  return template.evaluate().setTitle("配信停止の確認");
}

function confirmUnsubscribe(token, scope) {
  try {
    const result = unsubscribeLead_(token, scope);
    return { ok: true, scope: result.scope, message: "配信停止を受け付けました。" };
  } catch (error) {
    throw new Error(safeErrorMessage_(error));
  }
}

function markManualDeliveryFromUi_() {
  const ui = SpreadsheetApp.getUi();
  const leadPrompt = ui.prompt(
    "手動配布の完了",
    "受付番号（LD-...）を入力してください。",
    ui.ButtonSet.OK_CANCEL,
  );
  if (leadPrompt.getSelectedButton() !== ui.Button.OK) return;

  const channelPrompt = ui.prompt(
    "手動配布の完了",
    "チャネルを line または x で入力してください。",
    ui.ButtonSet.OK_CANCEL,
  );
  if (channelPrompt.getSelectedButton() !== ui.Button.OK) return;

  const result = markManualDelivery_(
    leadPrompt.getResponseText().trim(),
    channelPrompt.getResponseText().trim(),
    "Spreadsheet menu confirmation",
  );
  ui.alert(`完了: ${result.leadId} / ${result.channel}`);
}

function createDelivery_(leadId, channel, destination, kitVersion) {
  const now = new Date();
  const status = channel === "email"
    ? LLH.DELIVERY_STATUS.PENDING
    : LLH.DELIVERY_STATUS.MANUAL_REQUIRED;

  appendObjectRow_(LLH.SHEETS.DELIVERIES, DELIVERY_HEADERS, {
    delivery_id: buildDeliveryId_(now),
    lead_id: leadId,
    created_at: now,
    updated_at: now,
    channel,
    destination,
    kit_version: kitVersion,
    status,
    attempts: 0,
    last_attempt_at: "",
    sent_at: "",
    error_code: "",
    error_message: "",
    operator_note: "",
  });
}

function normalizeLeadPayload_(payload) {
  const channels = {
    email: toBoolean_(payload.channelEmail),
    line: toBoolean_(payload.channelLine),
    x: toBoolean_(payload.channelX),
  };

  return {
    displayName: cleanText_(payload.displayName, 120),
    email: String(payload.email || "").trim().toLowerCase(),
    lineName: cleanText_(payload.lineName, 120),
    xHandle: normalizeXHandle_(payload.xHandle),
    preferredChannel: String(payload.preferredChannel || "").trim().toLowerCase(),
    channels,
    consentDelivery: toBoolean_(payload.consentDelivery),
    consentUpdates: toBoolean_(payload.consentUpdates),
    consentOffers: toBoolean_(payload.consentOffers),
    source: cleanText_(payload.source || "web_form", 120),
    notes: cleanText_(payload.notes, 500),
    website: String(payload.website || "").trim(),
  };
}

function validateLeadPayload_(payload) {
  if (payload.website) {
    throw new Error("送信を受け付けられませんでした。");
  }

  const selectedChannels = LLH.CHANNELS.filter((channel) => payload.channels[channel]);
  if (selectedChannels.length < 1) {
    throw new Error("メール・LINE・Xのうち、最低一つを選択してください。");
  }

  if (!payload.consentDelivery) {
    throw new Error("スターターキット送付のための利用目的への同意が必要です。");
  }

  if (payload.channels.email && !isValidEmail_(payload.email)) {
    throw new Error("有効なメールアドレスを入力してください。");
  }

  if (payload.channels.x && !payload.xHandle) {
    throw new Error("Xを選択した場合はXアカウント名を入力してください。");
  }

  if (
    payload.preferredChannel &&
    !LLH.CHANNELS.includes(payload.preferredChannel)
  ) {
    throw new Error("優先受取方法が不正です。");
  }

  if (
    payload.preferredChannel &&
    !payload.channels[payload.preferredChannel]
  ) {
    throw new Error("優先受取方法は、選択したチャネルの中から指定してください。");
  }
}

function buildKitEmailHtml_(lead, delivery, config) {
  const webAppUrl = config.WEB_APP_URL || ScriptApp.getService().getUrl() || "";
  const unsubscribeUrl = webAppUrl
    ? `${webAppUrl}?action=unsubscribe&scope=all&token=${encodeURIComponent(String(lead.unsubscribe_token))}`
    : "";
  const greeting = lead.display_name
    ? `${escapeHtml_(String(lead.display_name))} 様`
    : "お申込みいただいた方へ";

  return [
    `<p>${greeting}</p>`,
    `<p>${escapeHtml_(config.KIT_NAME)}（${escapeHtml_(String(delivery.kit_version))}）の受取リンクです。</p>`,
    `<p><a href="${escapeHtml_(config.KIT_URL)}">スターターキットを受け取る</a></p>`,
    `<p>受付番号: <strong>${escapeHtml_(String(lead.lead_id))}</strong></p>`,
    `<hr>`,
    `<p style="font-size:12px;color:#555">このメールは、スターターキット送付への同意に基づいて送信しています。</p>`,
    unsubscribeUrl
      ? `<p style="font-size:12px"><a href="${escapeHtml_(unsubscribeUrl)}">更新情報・案内を含む今後の配信を停止する</a></p>`
      : "",
  ].join("\n");
}

function cancelPendingEmailDeliveries_(leadId) {
  const sheet = getSheet_(LLH.SHEETS.DELIVERIES);
  const values = sheet.getDataRange().getValues();
  if (values.length < 2) return;
  const headerMap = headerIndexMap_(values[0]);

  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    if (
      String(values[rowIndex][headerMap.lead_id]) === leadId &&
      String(values[rowIndex][headerMap.channel]) === "email" &&
      String(values[rowIndex][headerMap.status]) === LLH.DELIVERY_STATUS.PENDING
    ) {
      updateDeliveryRow_(sheet, rowIndex + 1, headerMap, {
        status: LLH.DELIVERY_STATUS.CANCELLED,
        updated_at: new Date(),
        error_code: "UNSUBSCRIBED",
        error_message: "Cancelled by unsubscribe request.",
      });
    }
  }
}

function countEmailDeliveriesSentToday_() {
  const sheet = getSheet_(LLH.SHEETS.DELIVERIES);
  const values = sheet.getDataRange().getValues();
  if (values.length < 2) return 0;
  const headerMap = headerIndexMap_(values[0]);
  const today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd");
  let count = 0;

  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    if (
      String(values[rowIndex][headerMap.channel]) !== "email" ||
      String(values[rowIndex][headerMap.status]) !== LLH.DELIVERY_STATUS.SENT
    ) {
      continue;
    }
    const sentAt = values[rowIndex][headerMap.sent_at];
    if (!(sentAt instanceof Date)) continue;
    const sentDate = Utilities.formatDate(sentAt, Session.getScriptTimeZone(), "yyyy-MM-dd");
    if (sentDate === today) count += 1;
  }
  return count;
}

function updateLeadLastDelivery_(leadId, timestamp) {
  const sheet = getSheet_(LLH.SHEETS.LEADS);
  const values = sheet.getDataRange().getValues();
  const headerMap = headerIndexMap_(values[0]);

  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    if (String(values[rowIndex][headerMap.lead_id]) === leadId) {
      sheet.getRange(rowIndex + 1, headerMap.last_delivery_at + 1).setValue(timestamp);
      sheet.getRange(rowIndex + 1, headerMap.updated_at + 1).setValue(timestamp);
      return;
    }
  }
}

function findLeadById_(leadId) {
  const sheet = getSheet_(LLH.SHEETS.LEADS);
  const values = sheet.getDataRange().getValues();
  if (values.length < 2) return null;
  const headers = values[0];
  const headerMap = headerIndexMap_(headers);

  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    if (String(values[rowIndex][headerMap.lead_id]) === leadId) {
      return rowToObject_(headers, values[rowIndex]);
    }
  }
  return null;
}

function updateDeliveryRow_(sheet, rowNumber, headerMap, updates) {
  for (const [key, value] of Object.entries(updates)) {
    if (Object.prototype.hasOwnProperty.call(headerMap, key)) {
      sheet.getRange(rowNumber, headerMap[key] + 1).setValue(value);
    }
  }
}

function appendObjectRow_(sheetName, headers, record) {
  const sheet = getSheet_(sheetName);
  const row = headers.map((header) =>
    Object.prototype.hasOwnProperty.call(record, header) ? record[header] : "",
  );
  sheet.appendRow(row);
}

function appendAudit_(actor, eventType, leadId, deliveryId, details) {
  appendObjectRow_(LLH.SHEETS.AUDIT, AUDIT_HEADERS, {
    audit_id: `AU-${Utilities.getUuid()}`,
    created_at: new Date(),
    actor,
    event_type: eventType,
    lead_id: leadId,
    delivery_id: deliveryId,
    details_json: JSON.stringify(details || {}),
  });
}

function appendAuditSafe_(actor, eventType, leadId, deliveryId, details) {
  try {
    appendAudit_(actor, eventType, leadId, deliveryId, details);
  } catch (_error) {
    // Failure logging must never hide the original error.
  }
}

function getConfig_() {
  const sheet = getSheet_(LLH.SHEETS.CONFIG);
  const values = sheet.getDataRange().getValues();
  const config = { ...LLH.DEFAULTS };
  for (let rowIndex = 1; rowIndex < values.length; rowIndex += 1) {
    const key = String(values[rowIndex][0] || "").trim();
    if (!key) continue;
    config[key] = String(values[rowIndex][1] ?? "").trim();
  }
  return config;
}

function seedConfig_(sheet) {
  const existingValues = sheet.getDataRange().getValues();
  const existingKeys = new Set(
    existingValues.slice(1).map((row) => String(row[0] || "").trim()),
  );
  const descriptions = {
    CURRENT_KIT_VERSION: "現在配布するキット版",
    KIT_NAME: "配布物の表示名",
    KIT_URL: "固定の最新版配布URL。必ず差し替える",
    LINE_ADD_URL: "LINE公式アカウントの友だち追加URL",
    X_PROFILE_URL: "配布に使うXプロフィールURL",
    ADMIN_EMAIL: "管理通知先。空欄可",
    MAIL_SAFETY_CAP_PER_RUN: "キュー1回あたりの最大送信数",
    MAIL_SAFETY_CAP_PER_DAY: "本システムで使う1日安全上限",
    WEB_APP_URL: "デプロイ後のウェブアプリURL。配信停止リンクに使用",
    PRIVACY_POLICY_URL: "個人情報の利用目的・方針ページ",
    SENDER_NAME: "メール送信者表示名",
  };

  for (const [key, value] of Object.entries(LLH.DEFAULTS)) {
    if (!existingKeys.has(key)) {
      sheet.appendRow([key, value, descriptions[key] || ""]);
    }
  }
}

function ensureSheet_(spreadsheet, name, headers) {
  let sheet = spreadsheet.getSheetByName(name);
  if (!sheet) {
    sheet = spreadsheet.insertSheet(name);
  }

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
  } else {
    const existing = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const mismatch = headers.some((header, index) => existing[index] !== header);
    if (mismatch) {
      throw new Error(`${name} シートのヘッダーが想定と異なります。自動上書きはしません。`);
    }
  }
  return sheet;
}

function getSpreadsheet_() {
  const spreadsheetId = PropertiesService.getScriptProperties().getProperty("SPREADSHEET_ID");
  if (spreadsheetId) {
    return SpreadsheetApp.openById(spreadsheetId);
  }
  const active = SpreadsheetApp.getActiveSpreadsheet();
  if (!active) {
    throw new Error("SPREADSHEET_ID が未設定です。初期セットアップを実行してください。");
  }
  return active;
}

function getSheet_(name) {
  const sheet = getSpreadsheet_().getSheetByName(name);
  if (!sheet) {
    throw new Error(`${name} シートがありません。初期セットアップを実行してください。`);
  }
  return sheet;
}

function assertInitialized_() {
  for (const name of Object.values(LLH.SHEETS)) {
    getSheet_(name);
  }
}

function headerIndexMap_(headers) {
  return headers.reduce((map, header, index) => {
    map[String(header)] = index;
    return map;
  }, {});
}

function rowToObject_(headers, row) {
  return headers.reduce((record, header, index) => {
    record[String(header)] = row[index];
    return record;
  }, {});
}

function buildLeadId_(date) {
  const day = Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyyMMdd");
  const random = Utilities.getUuid().replace(/-/g, "").slice(0, 8).toUpperCase();
  return `LD-${day}-${random}`;
}

function buildDeliveryId_(date) {
  const day = Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyyMMdd");
  const random = Utilities.getUuid().replace(/-/g, "").slice(0, 10).toUpperCase();
  return `DL-${day}-${random}`;
}

function isValidEmail_(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || ""));
}

function normalizeXHandle_(value) {
  const clean = String(value || "").trim().replace(/^@/, "");
  if (!clean) return "";
  if (!/^[A-Za-z0-9_]{1,15}$/.test(clean)) {
    throw new Error("Xアカウント名は@を除く1〜15文字の英数字とアンダースコアで入力してください。");
  }
  return `@${clean}`;
}

function cleanText_(value, maxLength) {
  return String(value || "")
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "")
    .trim()
    .slice(0, maxLength);
}

function toBoolean_(value) {
  return value === true || String(value).toLowerCase() === "true" || String(value) === "1";
}

function positiveInteger_(value, fallback) {
  const parsed = Number.parseInt(String(value), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function safeErrorMessage_(error) {
  const raw = error && error.message ? String(error.message) : "予期しないエラーが発生しました。";
  return raw.replace(/[\r\n\t]+/g, " ").slice(0, 300);
}

function escapeHtml_(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function redactConfig_(config) {
  return Object.fromEntries(
    Object.entries(config).map(([key, value]) => [key, key.includes("SECRET") ? "***" : value]),
  );
}
