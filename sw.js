/* CashFlow AI service worker — offline app shell + runtime caching. */
const CACHE = 'cashflow-v1';
const CORE = ['/', '/manifest.json', '/icons/icon-192.png', '/icons/icon-512.png',
  '/icons/maskable-512.png', '/icons/apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

const RUNTIME_OK = u => u.origin === self.location.origin
  || u.hostname.endsWith('jsdelivr.net')
  || u.hostname.endsWith('googleapis.com')
  || u.hostname.endsWith('gstatic.com');

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => {
      const copy = r.clone();
      caches.open(CACHE).then(c => c.put('/', copy));
      return r;
    }).catch(() => caches.match('/')));
    return;
  }

  if (!RUNTIME_OK(url)) return;

  e.respondWith(caches.open(CACHE).then(async c => {
    const cached = await c.match(req);
    const network = fetch(req).then(r => {
      if (r.ok || r.type === 'opaque') c.put(req, r.clone()).catch(() => {});
      return r;
    }).catch(() => cached);
    return cached || network;
  }));
});
