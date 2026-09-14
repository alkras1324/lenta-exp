/* опытная страница: пустой сервис-воркер, ничего не кэширует — только чтобы регистрация не падала 404, как на стейдже */
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
