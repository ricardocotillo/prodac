{% load static %}
importScripts('https://www.gstatic.com/firebasejs/9.1.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.1.2/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: 'AIzaSyBfyMeRTF5FwGdpTxuVssfSsRS2y9lHkoI',
  authDomain: 'prodac-7738f.firebaseapp.com',
  projectId: 'prodac-7738f',
  storageBucket: 'prodac-7738f.appspot.com',
  messagingSenderId: '572770346423',
  appId: '1:572770346423:web:83800ad9cb3a61a1a0f432',
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notification = payload.notification
  const notificationTitle = notification.title;
  const notificationOptions = {
    body: notification.body,
    icon: "{% static 'card/img/logo-512.png' %}",
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});

self.addEventListener('fetch', () => console.log(''))