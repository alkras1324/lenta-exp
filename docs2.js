(function () {
  'use strict';

  if (window.__LAMPA_DOCUMENTS_DOWNLOAD_V2__) return;
  window.__LAMPA_DOCUMENTS_DOWNLOAD_V2__ = true;

  function sourceUrl(element) {
    // Keep TorrServer's original URL and filename in /stream/<name>.
    // Do NOT rewrite TSArea :8880 to :8443 here: the HTTPS route can
    // redirect to a long signed URL and Documents then uses that token
    // as the filename.
    return String(element && element.url || '').replace('&preload', '&play');
  }

  function documentsUrl(element) {
    var src = sourceUrl(element);

    // Documents by Readdle URL scheme.
    if (src.indexOf('https://') === 0) return 'rhttps://' + src.slice(8);
    if (src.indexOf('http://') === 0) return 'rhttp://' + src.slice(7);

    return src;
  }

  function injectStyle() {
    if (document.getElementById('lampa-documents-download-style-v2')) return;

    var style = document.createElement('style');
    style.id = 'lampa-documents-download-style-v2';
    style.textContent = [
      '.lampa-documents-download-btn-v2{',
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
      '.lampa-documents-download-btn-v2:active{background:rgba(255,255,255,.3);}',
      '@media screen and (max-width:600px){',
      '  .lampa-documents-download-btn-v2{font-size:.95em;padding:.45em .55em;}',
      '}'
    ].join('');
    document.head.appendChild(style);
  }

  function onTorrentFile(e) {
    if (!e || e.type !== 'render' || !e.item || !e.element || !e.element.url) return;

    try {
      var item = e.item;
      if (item.find && item.find('.lampa-documents-download-btn-v2').length) return;

      var a = document.createElement('a');
      a.className = 'lampa-documents-download-btn-v2';
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
    if (Lampa.Noty) Lampa.Noty.show('Documents Download v2 загружен');
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