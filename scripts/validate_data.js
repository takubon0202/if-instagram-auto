/**
 * if(塾) Instagram風ブログ - データ検証スクリプト
 *
 * 使用方法:
 *   node scripts/validate_data.js
 *
 * 検証内容:
 *   - posts.json の必須フィールド
 *   - stories.json の必須フィールド
 *   - highlights.json の必須フィールド
 *   - config.json の必須フィールド
 */

const fs = require('fs');
const path = require('path');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m'
};

// Validation results
const results = {
  errors: [],
  warnings: [],
  passed: 0
};

// Helper functions
function error(msg) {
  results.errors.push(msg);
  console.log(`${colors.red}[ERROR]${colors.reset} ${msg}`);
}

function warning(msg) {
  results.warnings.push(msg);
  console.log(`${colors.yellow}[WARN]${colors.reset} ${msg}`);
}

function pass(msg) {
  results.passed++;
  console.log(`${colors.green}[PASS]${colors.reset} ${msg}`);
}

function info(msg) {
  console.log(`${colors.blue}[INFO]${colors.reset} ${msg}`);
}

// Load JSON file
function loadJSON(filePath) {
  try {
    const fullPath = path.resolve(__dirname, '..', filePath);
    const content = fs.readFileSync(fullPath, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    error(`Failed to load ${filePath}: ${e.message}`);
    return null;
  }
}

// Validate posts.json
function validatePosts(data) {
  info('Validating posts.json...');

  if (!data || !Array.isArray(data.posts)) {
    error('posts.json must contain a "posts" array');
    return;
  }

  const requiredFields = ['id', 'datetime', 'type', 'track', 'title', 'caption', 'cta_url', 'media'];
  const validTypes = ['carousel', 'reel', 'image'];
  const validTracks = ['juku', 'business'];

  data.posts.forEach((post, index) => {
    const prefix = `Post[${index}] (${post.id || 'no-id'})`;

    // Check required fields
    requiredFields.forEach(field => {
      if (!post[field]) {
        error(`${prefix}: missing required field "${field}"`);
      }
    });

    // Check type
    if (post.type && !validTypes.includes(post.type)) {
      error(`${prefix}: invalid type "${post.type}". Must be one of: ${validTypes.join(', ')}`);
    }

    // Check track
    if (post.track && !validTracks.includes(post.track)) {
      error(`${prefix}: invalid track "${post.track}". Must be one of: ${validTracks.join(', ')}`);
    }

    // Check media array
    if (post.media) {
      if (!Array.isArray(post.media) || post.media.length === 0) {
        error(`${prefix}: media must be a non-empty array`);
      } else {
        post.media.forEach((m, mi) => {
          if (!m.src) {
            error(`${prefix}: media[${mi}] missing "src"`);
          }
          if (!m.alt) {
            warning(`${prefix}: media[${mi}] missing "alt" (accessibility)`);
          }
        });
      }
    }

    // Check datetime format
    if (post.datetime) {
      const date = new Date(post.datetime);
      if (isNaN(date.getTime())) {
        error(`${prefix}: invalid datetime format "${post.datetime}"`);
      }
    }

    // Check hashtags
    if (post.hashtags && !Array.isArray(post.hashtags)) {
      error(`${prefix}: hashtags must be an array`);
    }

    // Check CTA URL
    if (post.cta_url && !post.cta_url.startsWith('https://')) {
      warning(`${prefix}: cta_url should use HTTPS`);
    }
  });

  pass(`posts.json: ${data.posts.length} posts validated`);
}

// Validate stories.json
function validateStories(data) {
  info('Validating stories.json...');

  if (!data || !Array.isArray(data.stories)) {
    error('stories.json must contain a "stories" array');
    return;
  }

  const requiredFields = ['id', 'datetime', 'type', 'src'];

  data.stories.forEach((story, index) => {
    const prefix = `Story[${index}] (${story.id || 'no-id'})`;

    // Check required fields
    requiredFields.forEach(field => {
      if (!story[field]) {
        error(`${prefix}: missing required field "${field}"`);
      }
    });

    // Check duration
    if (story.duration && (typeof story.duration !== 'number' || story.duration <= 0)) {
      warning(`${prefix}: duration should be a positive number`);
    }

    // Check alt
    if (!story.alt) {
      warning(`${prefix}: missing "alt" (accessibility)`);
    }
  });

  pass(`stories.json: ${data.stories.length} stories validated`);
}

// Validate highlights.json
function validateHighlights(data) {
  info('Validating highlights.json...');

  if (!data || !Array.isArray(data.highlights)) {
    error('highlights.json must contain a "highlights" array');
    return;
  }

  const requiredFields = ['id', 'name'];

  data.highlights.forEach((highlight, index) => {
    const prefix = `Highlight[${index}] (${highlight.id || 'no-id'})`;

    // Check required fields
    requiredFields.forEach(field => {
      if (!highlight[field]) {
        error(`${prefix}: missing required field "${field}"`);
      }
    });
  });

  pass(`highlights.json: ${data.highlights.length} highlights validated`);
}

// Validate config.json
function validateConfig(data) {
  info('Validating config.json...');

  if (!data) {
    error('config.json is empty or invalid');
    return;
  }

  if (!data.site) {
    error('config.json: missing "site" object');
  } else {
    if (!data.site.name) error('config.json: missing site.name');
    if (!data.site.url) error('config.json: missing site.url');
    if (!data.site.cta_primary) warning('config.json: missing site.cta_primary');
  }

  pass('config.json validated');
}

// Main
function main() {
  console.log('\n========================================');
  console.log('  if(塾) Data Validation');
  console.log('========================================\n');

  // Load and validate all files
  const posts = loadJSON('data/posts.json');
  const stories = loadJSON('data/stories.json');
  const highlights = loadJSON('data/highlights.json');
  const config = loadJSON('data/config.json');

  console.log('');

  if (posts) validatePosts(posts);
  if (stories) validateStories(stories);
  if (highlights) validateHighlights(highlights);
  if (config) validateConfig(config);

  // Summary
  console.log('\n========================================');
  console.log('  Summary');
  console.log('========================================');
  console.log(`${colors.green}Passed:${colors.reset} ${results.passed}`);
  console.log(`${colors.yellow}Warnings:${colors.reset} ${results.warnings.length}`);
  console.log(`${colors.red}Errors:${colors.reset} ${results.errors.length}`);
  console.log('');

  if (results.errors.length > 0) {
    console.log(`${colors.red}Validation FAILED${colors.reset}`);
    process.exit(1);
  } else {
    console.log(`${colors.green}Validation PASSED${colors.reset}`);
    process.exit(0);
  }
}

main();
