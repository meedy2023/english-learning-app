/* 英语学习小助手 Service Worker */
const CACHE = 'english-app-v2';
const ASSETS = [
  './',
  './index.html',
  './api-shim.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './data/words.json',
  './data/textbook.json',
  './data/ket.json',
  './data/phonics.json',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;

  const path = url.pathname;

  // index.html 与音频文件走网络优先（保证拿到最新版本，避免缓存旧文件名/旧页面）
  const isHtml = path.endsWith('/') || path.endsWith('/index.html') || path.endsWith('.html');
  const isAudio = /\.(wav|mp3|ogg|m4a|aac)$/i.test(path);

  if (isHtml || isAudio) {
    e.respondWith(
      fetch(e.request)
        .then((resp) => {
          if (resp && resp.status === 200) {
            const clone = resp.clone();
            caches.open(CACHE).then((c) => c.put(e.request, clone));
          }
          return resp;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // 其他静态资源（js/json/图标等）缓存优先，离线可用
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const network = fetch(e.request).then((resp) => {
        if (resp && resp.status === 200) {
          const clone = resp.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return resp;
      }).catch(() => cached);
      return cached || network;
    })
  );
});
