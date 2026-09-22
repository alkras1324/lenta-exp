(function () {
  'use strict';

  if (window.__LAMPA_DOCUMENTS_DOWNLOAD_V1__) return;
  window.__LAMPA_DOCUMENTS_DOWNLOAD_V1__ = true;

  function sourceUrl(element) {
    var src = String(element && element.url || '').replace('&preload', '&play');

    try {
      var u = new URL(src);

      // TSArea's current HTTPS endpoint.
      if (/\.tsarea\.tv$/i.test(u.hostname) && u.port === '8880') {
        u.protocol = 'https:';
        u.port = '8443';
      }

      src = u.toString();
    } catch (e) {}

    return src;
  }

  function documentsUrl(element) {
    var src = sourceUrl(element);

    // Documents by Readdle: http(s) -> rhttp(s) opens the URL
    // in Documents' built-in browser/download manager.
    if (src.indexOf('https://') === 0) return 'rhttps://' + src.slice(8);
    if (src.indexOf('http://') === 0) return 'rhttp://' + src.slice(7);

    return src;
  }

  function injectStyle() {
    if (document.getElementById('lampa-documents-download-style-v1')) return;

    var style = document.createElement('style');
    style.id = 'lampa-documents-download-style-v1';
    style.textContent = [
      '.lampa-documents-download-btn-v1{',
      '  flex-shrink:0;',
      '  margin-left:.7em;',
      '  padding:.38em .65em;',
      '  border-radius:.3em;',
      '  background:rgba(255,255,255,.16);',
      '  font-size:1.05em;',
      '  line-height:1.2;',
      '  white-space:nowrap;',
      '  cursor:pointer;',
      '  color:inherit;',
      '  text-decoration:none;',
      '  -webkit-user-select:none;',
      '  user-select:none;',
      '}',
      '.lampa-documents-download-btn-v1:active{background:rgba(255,255,255,.3);}',
      '@media screen and (max-width:600px){',
      '  .lampa-documents-download-btn-v1{font-size:.95em;padding:.45em .55em;}',
      '}'
    ].join('');
    document.head.appendChild(style);
  }

  function onTorrentFile(e) {
    if (!e || e.type !== 'render' || !e.item || !e.element || !e.element.url) return;

    try {
      var item = e.item;
      if (item.find && item.find('.lampa-documents-download-btn-v1').length) return;

      var a = document.createElement('a');
      a.className = 'lampa-documents-download-btn-v1';
      a.textContent = '↓ Скачать';
      a.href = documentsUrl(e.element);

      a.addEventListener('click', function (ev) {
        ev.stopPropagation();
      }, true);

      var node = item[0] || (item.get && item.get(0));
      if (node) node.appendChild(a);
    } catch (err) {
      if (window.Lampa && Lampa.Noty) {
        Lampa.Noty.show('Documents: ' + (err && err.message ? err.message : String(err)));
      }
    }
  }

  function init() {
    injectStyle();
    if (!window.Lampa || !Lampa.Listener) return;
    Lampa.Listener.follow('torrent_file', onTorrentFile);
    if (Lampa.Noty) Lampa.Noty.show('Documents Download v1 загружен');
  }

  if (window.Lampa && Lampa.Listener) init();
  else {
    var timer = setInterval(function () {
      if (window.Lampa && Lampa.Listener) {
        clearInterval(timer);
        init();
      }
    }, 250);
    setTimeout(function () { clearInterval(timer); }, 15000);
  }
})();