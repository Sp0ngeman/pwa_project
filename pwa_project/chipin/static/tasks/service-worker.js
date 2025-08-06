const CACHE_NAME = 'task-manager-v1';
const urlsToCache = [
  '/',
  '/static/tasks/styles.css',
  '/static/tasks/tasks.js',
  '/static/tasks/manifest.json',
  '/static/tasks/icon-192x192.png',
  '/static/tasks/icon-512x512.png'
];

// Install event - cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
      .catch(() => {
        // If both cache and network fail, return offline page
        if (event.request.destination === 'document') {
          return caches.match('/offline.html');
        }
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for offline tasks
self.addEventListener('sync', event => {
  if (event.tag === 'sync-tasks') {
    event.waitUntil(syncTasks());
  }
});

// Sync tasks from IndexedDB to server
async function syncTasks() {
  try {
    // This would typically involve reading from IndexedDB
    // and sending to the server when back online
    console.log('Syncing tasks...');
    
    // For now, just log that sync was attempted
    // In a real implementation, you would:
    // 1. Read pending tasks from IndexedDB
    // 2. Send them to the server
    // 3. Remove them from IndexedDB on success
    
  } catch (error) {
    console.error('Error syncing tasks:', error);
  }
}

// Push notification handling
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'You have a new task reminder!',
    icon: '/static/tasks/icon-192x192.png',
    badge: '/static/tasks/icon-192x192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Tasks',
        icon: '/static/tasks/icon-192x192.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/tasks/icon-192x192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Task Manager', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
}); 