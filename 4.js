(function () {
  'use strict';

  if (window.__LAMPA_TORR_DOWNLOAD_PLUGIN_V4__) return;
  window.__LAMPA_TORR_DOWNLOAD_PLUGIN_V4__ = true;

  function fileName(element) {
    var name = (element && (element.path || element.path_human || element.title || element.fname)) || 'video.mkv';
    name = String(name).split('\\').pop().split('/').pop();
    return name.replace(/[\u0000-\u001f<>:"|?*]/g, '_');
  }

  function directPlayUrl(element) {
    try {
      var u = new URL(String(element.url || ''));
      var hash = element.torrent_hash || u.searchParams.get('link');
      var id = element.id != null ? element.id : u.searchParams.get('index');

      if (hash && id != null && id !== '') {
        return u.protocol + '//' + u.host + '/play/' + encodeURIComponent(hash) + '/' + encodeURIComponent(String(id));
      }
    } catch (e) {}

    return String(element.url || '').replace('&preload', '&play');
  }

  function vlcDownloadUrl(element) {
    var src = directPlayUrl(element);
    var name = fileName(element);

    return 'vlc-x-callback://x-callback-url/download?url=' +
      encodeURIComponent(src) +
      '&filename=' +
      encodeURIComponent(name);
  }

  function injectStyle() {
    if (document.getElementById('lampa-torr-download-style-v4')) return;

    var style = document.createElement('style');
    style.id = 'lampa-torr-download-style-v4';
    style.textContent = [
      '.lampa-torr-download-btn-v4{',
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
      '.lampa-torr-download-btn-v4:active{background:rgba(255,255,255,.3);}',
      '@media screen and (max-width:600px){',
      '  .lampa-torr-download-btn-v4{font-size:.95em;padding:.45em .55em;}',
      '}'
    ].join('');
    document.head.appendChild(style);
  }

  function onTorrentFile(e) {
    if (!e || e.type !== 'render' || !e.item || !e.element || !e.element.url) return;

    try {
      var item = e.item;
      if (item.find && item.find('.lampa-torr-download-btn-v4').length) return;

      var a = document.createElement('a');
      a.className = 'lampa-torr-download-btn-v4';
      a.textContent = '↓ Скачать';
      a.href = vlcDownloadUrl(e.element);

      a.addEventListener('click', function (ev) {
        ev.stopPropagation();
      }, true);

      var node = item[0] || (item.get && item.get(0));
      if (node) node.appendChild(a);
    } catch (err) {
      if (window.Lampa && Lampa.Noty) {
        Lampa.Noty.show('Download: ' + (err && err.message ? err.message : String(err)));
      }
    }
  }

  function init() {
    injectStyle();
    if (!window.Lampa || !Lampa.Listener) return;
    Lampa.Listener.follow('torrent_file', onTorrentFile);
    if (Lampa.Noty) Lampa.Noty.show('Torr Download v4 загружен');
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