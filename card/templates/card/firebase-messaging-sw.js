self.addEventListener('notificationclick', function(e) {
  console.log(e)
  const url = e.notification.data.url
  if (url) {
    e.notification.close() // Android needs explicit close.
    e.waitUntil(
      clients.matchAll({type: 'window'}).then( windowClients => {
          // Check if there is already a window/tab open with the target URL
          for (var i = 0; i < windowClients.length; i++) {
              var client = windowClients[i]
              // If so, just focus it.
              if (client.url === url && 'focus' in client) {
                return client.focus()
              }
          }
          // If not, then open the target URL in a new window/tab.
          if (clients.openWindow) {
              return clients.openWindow(url)
          }
      })
    )
  }
})

importScripts('https://www.gstatic.com/firebasejs/9.1.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.1.2/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyD4e-HPWUbN7QMVbKh43L69Yn6ktCzVUgk",
  authDomain: "identicard-328401.firebaseapp.com",
  projectId: "identicard-328401",
  storageBucket: "identicard-328401.appspot.com",
  messagingSenderId: "508686565862",
  appId: "1:508686565862:web:c65bbbfb742b05f9bf9627"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload)
  const data = payload.data
  const notificationTitle = data.title
  const notificationOptions = {
    body: data.body,
    icon: data.icon,
    badge: data.badge,
    data,
  }

  self.registration.showNotification(notificationTitle, notificationOptions)
});

self.addEventListener('fetch', () => console.log(''))