// 验证整篇朗读按钮的事件绑定是否在函数内正确执行
const fs = require('fs');
const vm = require('vm');

const script = fs.readFileSync('test_script.js', 'utf8');

// 增强版沙箱，跟踪 onclick 设置
const onclickRegistry = {};
const sandbox = {
  window: {},
  document: {
    getElementById: (id) => {
      const elem = {
        id,
        addEventListener: (event, fn) => {
          if (event === 'click') elem._clickHandler = fn;
        },
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
        get onclick() { return this._onclick; },
        set onclick(fn) {
          this._onclick = fn;
          onclickRegistry[id] = fn;
        },
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
    }),
    body: { appendChild: () => {} },
    documentElement: { style: {} },
    write: () => {},
  },
  speechSynthesis: {
    cancel: () => {},
    speak: (utter) => console.log(`  [朗读] "${utter.text}"`),
    getVoices: () => [{ lang: 'en-US' }],
  },
  SpeechSynthesisUtterance: function(text) {
    this.text = text; this.lang = ''; this.rate = 1;
  },
  setTimeout: setTimeout,
  setInterval: setInterval,
  clearTimeout: clearTimeout,
  clearInterval: clearInterval,
  console: console,
  fetch: () => Promise.reject(new Error('no api')),
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
} catch (e) {
  console.log('Load error:', e.message);
  process.exit(1);
}

// 直接调用 showLessonDetail 函数（跳过 UI 渲染）
console.log('=== Test: 直接调用 showLessonDetail ===');
const testUnit = {
  unit: "Unit 1 I'm Sam",
  content: [
    { role: 'Sam', text: 'Hello, I am Sam.', translation: '你好，我是Sam。' },
    { role: 'Amy', text: 'Hi, I am Amy.', translation: '嗨，我是Amy。' },
  ],
};

try {
  sandbox.showLessonDetail(testUnit);
  console.log('✓ showLessonDetail called');
  
  // 检查按钮事件是否绑定
  if (onclickRegistry['lesson-full-speak-btn']) {
    console.log('✓ lesson-full-speak-btn has onclick handler bound');
    console.log('  → Simulating button click...');
    onclickRegistry['lesson-full-speak-btn']();
    console.log('✓ Click handler executed (should trigger speakAllLessonLines)');
  } else {
    console.log('✗ lesson-full-speak-btn does NOT have onclick handler');
  }
} catch (e) {
  console.log('Error:', e.message);
}

console.log('\n=== Done ===');