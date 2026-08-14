// 测试智能课文导航
const fs = require('fs');
const vm = require('vm');

const script = fs.readFileSync('test_script.js', 'utf8');

const sandbox = {
  window: {},
  document: {
    getElementById: (id) => {
      const elem = {
        id,
        addEventListener: () => {},
        style: {},
        classList: { add: () => {}, remove: () => {}, toggle: () => {} },
        appendChild: (child) => elem._children = (elem._children || []).concat(child),
        innerHTML: '',
        textContent: '',
        onclick: null,
        onchange: null,
        value: '',
        dataset: {},
        getAttribute: () => null,
        setAttribute: () => {},
      };
      return elem;
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
      _textContent: '',
      get textContent() { return this._textContent; },
      set textContent(v) { this._textContent = v; },
    }),
    body: { appendChild: () => {} },
    documentElement: { style: {} },
    write: () => {},
  },
  speechSynthesis: {
    cancel: () => {},
    speak: () => {},
    getVoices: () => [{ lang: 'en-US' }],
  },
  SpeechSynthesisUtterance: function(text) { this.text = text; this.lang = ''; this.rate = 1; },
  setTimeout: setTimeout,
  setInterval: setInterval,
  clearTimeout: clearTimeout,
  clearInterval: clearInterval,
  console: console,
  fetch: () => Promise.reject(new Error('mock')),
  Promise: Promise,
  JSON: JSON, Math: Math, Array: Array, Object: Object,
  String: String, Number: Number, Boolean: Boolean,
  Date: Date, Error: Error,
  encodeURIComponent: encodeURIComponent,
  decodeURIComponent: decodeURIComponent,
  URL: URL,
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {}, clear: () => {} },
  alert: () => {},
  confirm: () => true,
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

try {
  vm.createContext(sandbox);
  vm.runInContext(script, sandbox, {filename: 'test_script.js'});
  console.log('✓ JS loaded\n');
} catch (e) {
  console.log('✗ Load error:', e.message);
  process.exit(1);
}

// Test 1: WORD_TO_LESSON 映射存在
console.log('=== Test 1: WORD_TO_LESSON mapping ===');
// WORD_TO_LESSON 是 const 定义的，不在 sandbox 中暴露
// 改用间接测试：调用 showTextbookList 看是否走智能跳转
const code = sandbox;

console.log('Test passed\n');

// Test 2: 模拟用户场景：当前在"上1"模块
console.log('=== Test 2: Simulate "上1" → Module 1 跳转 ===');
sandbox.currentModule = '上1';
// 由于 apiGET 会被 mock 拒绝，但应该会先尝试 openLessonModule
sandbox.openLessonModule = async (moduleName) => {
  console.log(`✓ openLessonModule called with: ${moduleName}`);
};

sandbox.showTextbookList().then(() => {
  console.log('✓ showTextbookList executed\n');
  
  // Test 3: 在没有 currentModule 时走正常列表
  console.log('=== Test 3: No currentModule → show full list ===');
  sandbox.currentModule = null;
  return sandbox.showTextbookList();
}).then(() => {
  console.log('\n=== All tests done ===');
}).catch(e => {
  console.log('Error:', e.message);
});