importScripts('https://www.gstatic.com/firebasejs/9.5.0/firebase-app-compat.js')
importScripts('https://www.gstatic.com/firebasejs/9.5.0/firebase-messaging-compat.js')

// firebase.initializeApp({
//   apiKey: 'AIzaSyBfyMeRTF5FwGdpTxuVssfSsRS2y9lHkoI',
//   authDomain: 'prodac-7738f.firebaseapp.com',
//   projectId: 'prodac-7738f',
//   storageBucket: 'prodac-7738f.appspot.com',
//   messagingSenderId: '572770346423',
//   appId: '1:572770346423:web:83800ad9cb3a61a1a0f432',
// })

// const messaging = getMessaging()

// messaging.onBackgroundMessage(function(payload) {
//   console.log('[firebase-messaging-sw.js] Received background message ', payload)
//   const data = payload.data
//   const notificationTitle = data.title
//   const notificationOptions = {
//     body: data.body,
//     icon: data.icon,
//   }

//   self.registration.showNotification(notificationTitle, notificationOptions)
// })

self.addEventListener('fetch', () => console.log(''))