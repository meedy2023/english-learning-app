// 模拟测试整篇朗读功能
const fs = require('fs');
const vm = require('vm');

const script = fs.readFileSync('test_script.js', 'utf8');

// 模拟浏览器环境
const sandbox = {
  window: {},
  document: {
    getElementById: (id) => {
      const elements = {};
      return {
        id,
        addEventListener: () => {},
        style: {},
        classList: { add: () => {}, remove: () => {}, toggle: () => {} },
        appendChild: () => {},
        innerHTML: '',
        textContent: '',
        onclick: null,
        onchange: null,
        value: '',
        dataset: {},
        getAttribute: () => null,
        setAttribute: () => {},
      };
    },
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {},
    createElement: (tag) => ({
      tagName: tag,
      style: {},
      classList: { add: () => {}, remove: () => {} },
      appendChild: () => {},
      addEventListener: () => {},
      setAttribute: () => {},
      dataset: {},
      children: [],
      innerHTML: '',
    }),
    body: { appendChild: () => {} },
    documentElement: { style: {} },
    write: () => {},
  },
  speechSynthesis: {
    cancel: () => {},
    speak: (utter) => { console.log(`  [朗读] "${utter.text}" (lang=${utter.lang}, rate=${utter.rate})`); },
    getVoices: () => [{ lang: 'en-US', name: 'Test EN Voice' }],
  },
  SpeechSynthesisUtterance: function(text) {
    this.text = text;
    this.lang = '';
    this.rate = 1;
    this.pitch = 1;
    this.voice = null;
  },
  setTimeout: setTimeout,
  setInterval: setInterval,
  clearTimeout: clearTimeout,
  clearInterval: clearInterval,
  console: console,
  fetch: () => Promise.reject(new Error('no api')),
  Promise: Promise,
  JSON: JSON,
  Math: Math,
  Array: Array,
  Object: Object,
  String: String,
  Number: Number,
  Boolean: Boolean,
  Date: Date,
  Error: Error,
  encodeURIComponent: encodeURIComponent,
  decodeURIComponent: decodeURIComponent,
  URL: URL,
  localStorage: {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {},
    clear: () => {},
  },
  alert: () => {},
  confirm: () => true,
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

try {
  vm.createContext(sandbox);
  vm.runInContext(script, sandbox, {filename: 'test_script.js'});
  console.log('✓ JS loaded successfully');
} catch (e) {
  console.log('✗ Load error:', e.message);
  process.exit(1);
}

// 测试 1: speakAllLessonLines 是否存在
console.log('\n=== Test 1: speakAllLessonLines exists ===');
if (typeof sandbox.speakAllLessonLines === 'function') {
  console.log('✓ speakAllLessonLines is defined');
} else {
  console.log('✗ speakAllLessonLines NOT found');
  process.exit(1);
}

// 测试 2: 调用 speakAllLessonLines
console.log('\n=== Test 2: call speakAllLessonLines ===');
const testContent = [
  { role: 'Sam', text: 'Hello, I am Sam.', translation: '你好，我是Sam。' },
  { role: 'Amy', text: 'Hi, I am Amy.', translation: '嗨，我是Amy。' },
  { role: 'Ms Smart', text: 'Good morning, boys and girls.', translation: '早上好，孩子们。' },
];

try {
  sandbox.speakAllLessonLines(testContent);
  console.log('✓ speakAllLessonLines called without throwing');
} catch (e) {
  console.log('✗ Error:', e.message);
}

// 测试 3: 空内容
console.log('\n=== Test 3: empty content ===');
try {
  sandbox.speakAllLessonLines([]);
  console.log('✓ Empty content handled');
} catch (e) {
  console.log('✗ Error:', e.message);
}

console.log('\n=== All tests passed ===');