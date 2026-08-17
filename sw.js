const CACHE_NAME = 'aeterna-sovereign-v1.0';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './CLINICAL_DOCTOR_PORTAL.html',
  './clinical-oncology.html',
  './vht_diabet.html',
  './vht_cardio.html',
  './vht_longevity.html',
  './vht_suite.html',
  './sovereign-hud.html',
  './SovereignHUD.html',
  './SovereignHUD_v2.html',
  './smart_cables_hud.html',
  './smart_city.html',
  './ukame-matrix.html',
  './aeterna_cohort_sim.html',
  './aeterna_pharma_shadow.html',
  './oncology_hud.html',
  './hud.html',
  './aeterna.html',
  './docs.html',
  './qantum.html',
  './qantum-mailer.html',
  './IP_FINDER.html',
  './manifest.json',
  './assets/aeterna_logo.svg',
  './assets/VHT_HUD_MOA_PREVIEW.png',
  './assets/VHT_HUD_ONCOCALC_APPLIED.png',
  './assets/vht_brain_hud_preview.png',
  './assets/vht_diabet_hud_preview.png',
  './assets/refined_purple_twins_signed.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[AETERNA SW] Pre-caching offline sovereign assets...');
      return cache.addAll(ASSETS_TO_CACHE).catch(err => {
        console.warn('[AETERNA SW] Some optional assets failed to cache:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[AETERNA SW] Removing old cache:', key);
          return caches.delete(key);
        }
      }));
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });
        return networkResponse;
      }).catch(() => {
        // Offline fallback
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('./index.html');
        }
      });
    })
  );
});
