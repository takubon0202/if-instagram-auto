/**
 * if(塾) Instagram ワークフロー ランナー
 *
 * 使用方法:
 *   node scripts/workflow_runner.js daily [--date YYYY-MM-DD]
 *   node scripts/workflow_runner.js weekly [--week YYYY-WNN]
 *   node scripts/workflow_runner.js validate
 *   node scripts/workflow_runner.js status
 */

const fs = require('fs');
const path = require('path');

// Colors
const c = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

// Paths
const ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT, 'data');
const SCRIPTS_DIR = path.join(ROOT, 'scripts');

// Day mapping
const DAY_NAMES = ['日', '月', '火', '水', '木', '金', '土'];
const WEEKLY_THEMES = {
  juku_0900: {
    '月': '安心・居場所',
    '火': '学習のハードルを下げる',
    '水': '保護者向け（声かけ）',
    '木': 'AI/ITスキル',
    '金': '無料体験の背中押し',
    '土': 'FAQ',
    '日': 'まとめ'
  },
  business_1230: {
    '月': '研修の失敗パターン',
    '水': 'ワークフロー設計',
    '金': 'LP改善チェック',
    '火': 'ローテーション',
    '木': 'ローテーション',
    '土': 'ローテーション',
    '日': 'ローテーション'
  },
  juku_2000: {
    '月': '共感・安心',
    '火': '小さく始める',
    '水': '家庭内の話',
    '木': '小中高別',
    '金': '背中押し',
    '土': 'FAQ',
    '日': 'まとめ'
  }
};

// Utilities
function log(msg, color = '') {
  console.log(`${color}${msg}${c.reset}`);
}

function loadJSON(filename) {
  const filepath = path.join(DATA_DIR, filename);
  try {
    return JSON.parse(fs.readFileSync(filepath, 'utf-8'));
  } catch (e) {
    return null;
  }
}

function saveJSON(filename, data) {
  const filepath = path.join(DATA_DIR, filename);
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
}

function getToday() {
  const now = new Date();
  return {
    date: now.toISOString().split('T')[0],
    dayOfWeek: DAY_NAMES[now.getDay()],
    dayIndex: now.getDay()
  };
}

function generatePostId(date, slot, track, type, index = 1) {
  const trackShort = track === 'business' ? 'biz' : track;
  return `${date}-${slot}-${trackShort}-${type}-${String(index).padStart(2, '0')}`;
}

// Commands
function showStatus() {
  log('\n========================================', c.cyan);
  log('  if(塾) Instagram ワークフロー Status', c.cyan);
  log('========================================\n', c.cyan);

  const today = getToday();
  log(`今日: ${today.date} (${today.dayOfWeek})`, c.bold);

  // Posts stats
  const posts = loadJSON('posts.json');
  if (posts && posts.posts) {
    log(`\n投稿数: ${posts.posts.length}件`, c.green);

    const todayPosts = posts.posts.filter(p => p.datetime.startsWith(today.date));
    log(`今日の投稿: ${todayPosts.length}件`, todayPosts.length >= 3 ? c.green : c.yellow);

    const jukuPosts = posts.posts.filter(p => p.track === 'juku').length;
    const bizPosts = posts.posts.filter(p => p.track === 'business').length;
    log(`比率: 塾${jukuPosts} : 企業${bizPosts}`);
  }

  // Stories stats
  const stories = loadJSON('stories.json');
  if (stories && stories.stories) {
    log(`\nストーリー数: ${stories.stories.length}件`, c.green);
  }

  // Today's themes
  log('\n今日のテーマ:', c.bold);
  log(`  09:00 (塾): ${WEEKLY_THEMES.juku_0900[today.dayOfWeek]}`);
  log(`  12:30 (企業): ${WEEKLY_THEMES.business_1230[today.dayOfWeek]}`);
  log(`  20:00 (塾): ${WEEKLY_THEMES.juku_2000[today.dayOfWeek]}`);

  log('\n');
}

function showDailyTemplate(targetDate) {
  const today = targetDate ? { date: targetDate, dayOfWeek: DAY_NAMES[new Date(targetDate).getDay()] } : getToday();

  log('\n========================================', c.cyan);
  log('  Daily Run テンプレート', c.cyan);
  log('========================================\n', c.cyan);

  log(`日付: ${today.date} (${today.dayOfWeek})`, c.bold);
  log('\n--- 以下をClaude Codeに貼り付けて実行 ---\n', c.yellow);

  const template = `
今日のDaily Runを実行してください。

## 入力情報
- 日付: ${today.date}
- 曜日: ${today.dayOfWeek}
- トレンドメモ: （ここに今日のトレンドを入力）

## 今日のテーマ
- 09:00 (塾カルーセル): ${WEEKLY_THEMES.juku_0900[today.dayOfWeek]}
- 12:30 (企業): ${WEEKLY_THEMES.business_1230[today.dayOfWeek]}
- 20:00 (塾リール): ${WEEKLY_THEMES.juku_2000[today.dayOfWeek]}

## 実行手順
1. 上記テーマに基づいて3投稿を企画
2. カルーセル/リールの構成を作成
3. キャプションとハッシュタグを生成
4. 画像プロンプトを生成
5. 安全性チェック
6. data/posts.json に追記
7. validate_data.js で検証

## 出力
posts.json への追記と、scripts/new_day_content.md への記録をお願いします。
`;

  console.log(template);
  log('\n--- テンプレート終わり ---\n', c.yellow);
}

function runValidation() {
  log('\n========================================', c.cyan);
  log('  データ検証', c.cyan);
  log('========================================\n', c.cyan);

  try {
    require('./validate_data.js');
  } catch (e) {
    log(`検証エラー: ${e.message}`, c.red);
  }
}

function showHelp() {
  log('\n========================================', c.cyan);
  log('  if(塾) Instagram ワークフロー ランナー', c.cyan);
  log('========================================\n', c.cyan);

  log('使用方法:', c.bold);
  log('  node scripts/workflow_runner.js <command> [options]\n');

  log('コマンド:', c.bold);
  log('  status              現在の状態を表示');
  log('  daily [--date]      Daily Run テンプレートを表示');
  log('  weekly [--week]     Weekly Review テンプレートを表示');
  log('  validate            データ検証を実行');
  log('  help                このヘルプを表示\n');

  log('例:', c.bold);
  log('  node scripts/workflow_runner.js status');
  log('  node scripts/workflow_runner.js daily');
  log('  node scripts/workflow_runner.js daily --date 2026-01-10');
  log('  node scripts/workflow_runner.js validate\n');
}

// Main
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'status':
      showStatus();
      break;
    case 'daily':
      const dateIdx = args.indexOf('--date');
      const targetDate = dateIdx >= 0 ? args[dateIdx + 1] : null;
      showDailyTemplate(targetDate);
      break;
    case 'weekly':
      log('Weekly Review テンプレートは scripts/weekly_review.md を参照してください。', c.yellow);
      break;
    case 'validate':
      runValidation();
      break;
    case 'help':
    default:
      showHelp();
      break;
  }
}

main();
