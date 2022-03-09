
self.addEventListener('install', function () {
  self.skipWaiting()
})

self.addEventListener('push', function (event) {
  try {
    const response = event.data.json()
    const title = response.title
    const message = response.message
    self.registration.showNotification(title, {
      body: message,
      icon: 'icon.png',
      vibrate: [100, 50, 100]
    })
    self.clients.matchAll({ includeUncontrolled: true, type: 'window' }).then(function (clients) {
      clients.forEach(function (client) {
        client.postMessage({ title, message })
      })
    })
  } catch (e) { }
})
