/**
 * service-worker.js — CMTA Islamabad Metro PWA
 * Strategy:
 *   • Static assets  → Cache-first (serve from cache, update in background)
 *   • API calls      → Network-first (try network, fall back to cache)
 *   • Everything else → Network-first with offline fallback
 */

const CACHE_NAME    = 'cmta-v1';
const API_CACHE     = 'cmta-api-v1';

// Assets to pre-cache on install
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/routes.html',
  '/fares.html',
  '/timings.html',
  '/help.html',
  '/static/shared.js',
  '/static/shared.css',
  '/static/manifest.json',
  '/static/favicon.svg',
  // Offline fallback page (inline, no extra file needed — we cache index.html)
];

// ── Install: pre-cache all static assets ──────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())   // activate immediately
  );
});

// ── Activate: clean up old caches ─────────────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== CACHE_NAME && k !== API_CACHE)
          .map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())  // take control of all tabs immediately
  );
});

// ── Fetch: routing logic ───────────────────────────────────────────────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // 1. API requests → Network-first, cache response for offline fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstThenCache(request, API_CACHE));
    return;
  }

  // 2. Static assets (JS, CSS, images, fonts) → Cache-first
  if (
    url.pathname.startsWith('/static/') ||
    request.destination === 'font'     ||
    request.destination === 'style'    ||
    request.destination === 'script'   ||
    request.destination === 'image'
  ) {
    event.respondWith(cacheFirstThenNetwork(request, CACHE_NAME));
    return;
  }

  // 3. HTML navigation → Network-first, fallback to cached page or index
  if (request.mode === 'navigate') {
    event.respondWith(networkFirstThenCache(request, CACHE_NAME));
    return;
  }

  // 4. Everything else → network only (CDN fonts etc.)
  event.respondWith(fetch(request));
});

// ── Helpers ────────────────────────────────────────────────────────────────

async function cacheFirstThenNetwork(request, cacheName) {
  const cached = await caches.match(request, { cacheName });
  if (cached) {
    // Update cache in background (stale-while-revalidate)
    fetch(request).then(response => {
      if (response && response.ok) {
        caches.open(cacheName).then(cache => cache.put(request, response));
      }
    }).catch(() => {/* silent — offline */});
    return cached;
  }
  try {
    const response = await fetch(request);
    if (response && response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    // Offline fallback: return index.html for navigation requests
    return (await caches.match('/index.html')) || new Response(
      '<h1>You are offline</h1><p>Please reconnect to use Islamabad Metro.</p>',
      { headers: { 'Content-Type': 'text/html' } }
    );
  }
}

async function networkFirstThenCache(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response && response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request, { cacheName });
    if (cached) return cached;
    // For API failures, return a JSON error so the UI can handle it gracefully
    if (new URL(request.url).pathname.startsWith('/api/')) {
      return new Response(
        JSON.stringify({ detail: 'Offline — please reconnect to load live data.' }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }
    return (await caches.match('/index.html')) || Response.error();
  }
}

// ── PWA Install prompt helper ─────────────────────────────────────────────
// The browser controls the A2HS prompt; we just make sure the SW is healthy.
// The manifest.json already declares start_url, icons, display:standalone.
