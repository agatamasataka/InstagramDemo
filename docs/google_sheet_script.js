// ▼▼▼ Slackへの投稿先 Webhook URL ▼▼▼
var SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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';
// ▲▲▲ あなたのメインのWebhook URLを貼り付けてください ▲▲▲

// --- シート名の定義 ---
var DB_SHEET_NAME = "データベース";
var TODAY_SUMMARY_SHEET_NAME = "集計表";
var ARCHIVE_SHEET_NAME = "過去の集計";

// --- セル名の定義 ---
var SUMMARY_CELL_TODAY = "A1";

// --- データベース列の定義 --- (フォームから取得される値の場所 - 1からカウント)
var DB_COL_APO_STATUS = 5;      // E列 (結果)
var DB_COL_APO_PERSON = 4;      // D列 (アポ担当者)
var DB_COL_CLIENT_NAME = 3;     // C列 (会社名)

// -------------------------------------------------------------------------
// 1. スプレッドシートを開いた時に「手動実行メニュー」を追加する
// -------------------------------------------------------------------------
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('スラック自動集計（LMS）')
    .addItem('【手動】日付入力 ＆ 今すぐ投稿', 'manualRun_PostNow')
    .addItem('【手動】昨日の集計を「過去の集計」に記録', 'archiveYesterdaySummary')
    .addToUi();
}

// -------------------------------------------------------------------------
// 2.【手動実行用】集計投稿関数
// -------------------------------------------------------------------------
function manualRun_PostNow() {
  try {
    fillMissingDates();
    SpreadsheetApp.flush();
    Utilities.sleep(1000);

    var message = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(TODAY_SUMMARY_SHEET_NAME).getRange(SUMMARY_CELL_TODAY).getValue();
    sendToSlack(message, SLACK_WEBHOOK_URL);

    SpreadsheetApp.getUi().alert('最新の集計をSlackに投稿しました。');
  } catch (e) {
    SpreadsheetApp.getUi().alert('エラー: ' + e.message);
  }
}

function manualRun_ArchiveAndPost() {
  try {
    archiveYesterdaySummary();
    postYesterdaySummary_ChannelB();

    SpreadsheetApp.getUi().alert('「昨日の集計」を「過去の集計」シートに記録し、Slackに投稿しました。');
  } catch (e) {
    SpreadsheetApp.getUi().alert('エラー: ' + e.message);
  }
}

// -------------------------------------------------------------------------
// 3.【自動実行用】定時投稿（本日の集計）
// -------------------------------------------------------------------------
function postTodaySummary() {
  try {
    fillMissingDates();
    var message = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(TODAY_SUMMARY_SHEET_NAME).getRange(SUMMARY_CELL_TODAY).getValue();
    sendToSlack(message, SLACK_WEBHOOK_URL);
    Logger.log("定時投稿: 本日の集計を投稿しました。");
  } catch (e) {
    Logger.log("定時投稿エラー: " + e.message);
  }
}

// -------------------------------------------------------------------------
// 4.【自動実行用】昨日の集計（9:00の投稿など）
// -------------------------------------------------------------------------
function postYesterdaySummary_ChannelB() {
  try {
    var archiveSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(ARCHIVE_SHEET_NAME);
    var lastRow = archiveSheet.getLastRow();
    if (lastRow < 2) {
      sendToSlack("昨日の集計データが「過去の集計」シートにまだありません。", SLACK_WEBHOOK_URL);
      return;
    }

    // 「過去の集計」シートの「一番下の行」のデータを取得 (A列からG列まで、合計7列)
    var yesterdayData = archiveSheet.getRange(lastRow, 1, 1, 7).getValues()[0];
    var date = Utilities.formatDate(yesterdayData[0], "JST", "yyyy/MM/dd");

    // Slack投稿用の文章をここで組み立てる
    var message = "【昨日の営業結果】 (" + date + " 終日)" + "\n"
      + "------------------------------" + "\n"
      + "商談総数：" + yesterdayData[1] + " 件" + "\n" // B列
      + "受注　　：" + yesterdayData[2] + " 件" + "\n" // C列
      + "失注　　：" + yesterdayData[3] + " 件" + "\n" // D列
      + "検討（短期）：" + yesterdayData[4] + " 件" + "\n" // E列
      + "検討（長期）：" + yesterdayData[5] + " 件" + "\n" // F列
      + "------------------------------" + "\n"
      + "受注ID数合計：" + yesterdayData[6]; // G列

    sendToSlack(message, SLACK_WEBHOOK_URL); // メインURLに投稿
    Logger.log("昨日の集計投稿: 投稿しました。");

  } catch (e) {
    Logger.log("昨日の集計投稿エラー: " + e.message);
  }
}

// -------------------------------------------------------------------------
// 5.【自動実行用】「昨日の集計」を「過去の集計」シートに蓄積する
// -------------------------------------------------------------------------
function archiveYesterdaySummary() {
  try {
    var todaySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(TODAY_SUMMARY_SHEET_NAME);

    // 過去データ蓄積の基準となる「昨日」の集計値をD列から取得
    var yesterdayDate = new Date();
    yesterdayDate.setDate(yesterdayDate.getDate() - 1);

    var summaryValues = {
      // 集計表のD列から値を取得
      total: todaySheet.getRange("D3").getValue(),
      succeeded: todaySheet.getRange("D4").getValue(),
      failed: todaySheet.getRange("D5").getValue(),
      pendingShort: todaySheet.getRange("D6").getValue(),
      pendingLong: todaySheet.getRange("D7").getValue(),
      cancelled: todaySheet.getRange("D8").getValue(),   // アポ不成立
      idSum: todaySheet.getRange("D10").getValue()       // ★【修正済み】受注ID数合計 (D10セルを参照)
    };

    // 受注ID数合計が0の場合、明示的に0に変換する処理を追加
    var idSumValue = (summaryValues.idSum === "" || summaryValues.idSum === null) ? 0 : summaryValues.idSum;

    // 2. 「過去の集計」シートに書き込む (7列分)
    var archiveSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(ARCHIVE_SHEET_NAME);
    archiveSheet.appendRow([
      yesterdayDate,        // A列: 日付
      (summaryValues.total === "") ? 0 : summaryValues.total,       // B列: 商談総数
      (summaryValues.succeeded === "") ? 0 : summaryValues.succeeded, // C列: 受注
      (summaryValues.failed === "") ? 0 : summaryValues.failed,      // D列: 失注
      (summaryValues.pendingShort === "") ? 0 : summaryValues.pendingShort,// E列: 検討（短期）
      (summaryValues.pendingLong === "") ? 0 : summaryValues.pendingLong, // F列: 検討（長期）
      idSumValue      // G列: 受注ID数合計
    ]);

    Logger.log("昨日の集計を「過去の集計」シートに保存しました。");

  } catch (e) {
    Logger.log("アーカイブエラー: " + e.message);
  }
}

// -------------------------------------------------------------------------
// 6. Slackにメッセージを送信する共通関数
// -------------------------------------------------------------------------
function sendToSlack(messageText, targetUrl) {
  var payload = {
    "text": messageText
  };
  UrlFetchApp.fetch(targetUrl, {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload)
  });
}

// -------------------------------------------------------------------------
// 7. 日付を自動で埋める関数 (最新のシート構成に合わせて修正)
// -------------------------------------------------------------------------
function fillMissingDates() {
  var dbSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(DB_SHEET_NAME);
  var lastRow = dbSheet.getLastRow();
  if (lastRow <= 1) return;
  var aRange = dbSheet.getRange("A2:A" + lastRow);
  var iRange = dbSheet.getRange("I2:I" + lastRow);
  var aValues = aRange.getValues();
  var iValues = iRange.getValues();
  var updated = false;
  for (var i = 0; i < aValues.length; i++) {
    if (iValues[i][0] === "" && aValues[i][0] !== "") {
      try {
        var timestampText = aValues[i][0];
        var dateObject = new Date(timestampText);
        dateObject.setHours(0, 0, 0, 0);
        if (!isNaN(dateObject.getTime())) {
          iValues[i][0] = dateObject;
          updated = true;
        }
      } catch (e) {
        Logger.log("Row " + (i + 2) + " 日付変換エラー: " + e);
      }
    }
  }
  if (updated) {
    iRange.setValues(iValues).setNumberFormat("yyyy/MM/dd");
    SpreadsheetApp.flush();
    Utilities.sleep(1000);
    Logger.log("I列の日付を自動入力しました（時刻切り捨て版）。");
  }
}
// -------------------------------------------------------------
// ▼▼▼ 新機能：シートが編集されたらMacへ通知 (Google Drive経由) ▼▼▼
// -------------------------------------------------------------

function manualEditTrigger(e) {
  // 手動編集時はここが呼ばれる
  checkAndNotify(e.range.getSheet(), e.range.getRow());
}

function onFormSubmit(e) {
  // フォーム送信時はここが呼ばれる
  checkAndNotify(e.range.getSheet(), e.range.getRow());
}

function checkAndNotify(sheet, row) {
  try {
    // シート名チェック（「テスト」または「データベース」で動作）
    var sheetName = sheet.getName();
    if (sheetName !== "テスト" && sheetName !== "データベース") return;

    // その行のデータを取得 (B列〜G列)
    // B=2, C=3, D=4, E=5, F=6, G=7
    var range = sheet.getRange(row, 2, 1, 6);
    var values = range.getValues()[0];

    var personName = values[0]; // B列:担当者
    // var client   = values[1]; // C列:会社名(使わない)
    // var type     = values[2]; // D列:種類(使わない)
    var result = values[3]; // E列:結果 (受注)
    var idCount = values[4]; // F列:ID数
    var comment = values[5]; // G列:コメント

    // 「受注」じゃなければ何もしないで終了
    if (result !== "受注") return;

    // --- 通知メッセージ作成 (修正箇所) ---
    // 既存のメッセージ + 新しいお祝いメッセージ
    var messageText = personName + "さんが、" + idCount + "件の受注を獲得しました。" + (comment ? " " + comment : "") + "。\n\n" + "次の受注も、期待しています！ おめでとうございます！";

    // Googleドライブに出力
    var folderId = "1_vcOgGdG9yBok6A9aqeX3smF0FTMqNeJ";
    var folder = DriveApp.getFolderById(folderId);
    folder.createFile("ALERT_" + new Date().getTime() + ".txt", messageText);

  } catch (e) {
    // エラー時は何もしない
  }
}
