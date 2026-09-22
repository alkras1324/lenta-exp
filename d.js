(function () {
  'use strict';

  if (window.__LAMPA_TORR_DOWNLOAD_PLUGIN__) return;
  window.__LAMPA_TORR_DOWNLOAD_PLUGIN__ = true;

  function playUrl(url) {
    return String(url || '').replace('&preload', '&play');
  }

  function fileName(element) {
    var name = (element && (element.path || element.title || element.fname)) || 'video';
    name = String(name).split('\\').pop().split('/').pop();
    return name.replace(/[\u0000-\u001f<>:"|?*]/g, '_');
  }

  function startDownload(element) {
    if (!element || !element.url) {
      if (window.Lampa && Lampa.Noty) Lampa.Noty.show('Нет ссылки на файл');
      return;
    }

    var url = playUrl(element.url);
    var a = document.createElement('a');
    a.href = url;
    a.download = fileName(element);
    a.rel = 'noopener';
    a.style.display = 'none';

    document.body.appendChild(a);
    a.click();

    setTimeout(function () {
      if (a.parentNode) a.parentNode.removeChild(a);
    }, 1000);
  }

  function injectStyle() {
    if (document.getElementById('lampa-torr-download-style')) return;

    var style = document.createElement('style');
    style.id = 'lampa-torr-download-style';
    style.textContent = [
      '.lampa-torr-download-btn{',
      '  flex-shrink:0;',
      '  margin-left:.7em;',
      '  padding:.38em .65em;',
      '  border-radius:.3em;',
      '  background:rgba(255,255,255,.16);',
      '  font-size:1.05em;',
      '  line-height:1.2;',
      '  white-space:nowrap;',
      '  cursor:pointer;',
      '  -webkit-user-select:none;',
      '  user-select:none;',
      '}',
      '.lampa-torr-download-btn:active{background:rgba(255,255,255,.3);}',
      '@media screen and (max-width:600px){',
      '  .lampa-torr-download-btn{font-size:.95em;padding:.45em .55em;}',
      '}'
    ].join('');
    document.head.appendChild(style);
  }

  function onTorrentFile(e) {
    if (!e || e.type !== 'render' || !e.item || !e.element || !e.element.url) return;

    var item = e.item;
    if (item.find && item.find('.lampa-torr-download-btn').length) return;

    var btn = $('<div class="lampa-torr-download-btn">↓ Скачать</div>');

    function run(ev) {
      if (ev) {
        if (ev.preventDefault) ev.preventDefault();
        if (ev.stopPropagation) ev.stopPropagation();
        if (ev.stopImmediatePropagation) ev.stopImmediatePropagation();
      }
      startDownload(e.element);
      return false;
    }

    btn.on('click', run);
    btn.on('touchend', run);
    btn.on('hover:enter', run);

    item.append(btn);
  }

  function init() {
    injectStyle();

    if (!window.Lampa || !Lampa.Listener) return;

    Lampa.Listener.follow('torrent_file', onTorrentFile);

    if (Lampa.Noty) Lampa.Noty.show('Torr Download: плагин загружен');
  }

  if (window.Lampa && Lampa.Listener) {
    init();
  } else {
    var timer = setInterval(function () {
      if (window.Lampa && Lampa.Listener) {
        clearInterval(timer);
        init();
      }
    }, 250);

    setTimeout(function () {
      clearInterval(timer);
    }, 15000);
  }
})();
