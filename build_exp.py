# -*- coding: utf-8 -*-
"""Сборка ОПЫТНОЙ ленты для https://alkras1324.github.io/lenta-exp/

С 14.09.2026 шаблон берётся уже С ПЕРЕНЕСЁННЫМ рецептом (roma4u, PR #3309):
два режима, `black-translucent`, рама по видимому окну, два состояния кнопок.
Поэтому прежних подмен `позицияЛенты`/`shot.clientHeight`/`ДОКПРОКРУТКА` здесь
больше НЕТ — они живут в самом шаблоне, и дублировать их тут значило бы отлаживать
не то, что поедет в бой.

Опыту остаётся ровно оснастка: карточки-заглушки, плашка диагностики, полосы
«ВЕРХ/НИЗ КАРТОЧКИ» и один проверяемый опыт за раз (сейчас — заливка полосы,
которую iOS не отдала окну PWA).

Путь к шаблону: первым аргументом либо переменной окружения ROMA4U_TPL.
"""
import json, urllib.parse, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = (sys.argv[1] if len(sys.argv) > 1 else None) or os.environ.get('ROMA4U_TPL') or os.path.join(
    HERE, '..', 'roma4u', 'docs', 'design', 'prototypes', 'feed', 'index.template.html')
OUT = os.path.join(HERE, 'index.html')

html = open(TPL, encoding='utf-8').read()

colors = ['#c0392b', '#8e44ad', '#2980b9', '#16a085', '#d35400', '#27ae60', '#7f8c8d', '#e84393', '#f39c12', '#34495e']


def svg(i, c):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="956" viewBox="0 0 440 956">'
         f'<rect width="440" height="956" fill="{c}"/>'
         f'<rect x="0" y="0" width="440" height="40" fill="#fff" opacity=".35"/>'
         f'<rect x="0" y="916" width="440" height="40" fill="#fff" opacity=".35"/>'
         f'<text x="220" y="478" font-size="72" text-anchor="middle" fill="#fff" font-family="sans-serif">{i}</text>'
         f'<text x="220" y="30" font-size="22" text-anchor="middle" fill="#000" font-family="sans-serif">ВЕРХ КАДРА {i}</text>'
         f'<text x="220" y="945" font-size="22" text-anchor="middle" fill="#000" font-family="sans-serif">НИЗ КАДРА {i}</text></svg>')
    return 'data:image/svg+xml;charset=utf-8,' + urllib.parse.quote(s)


bq = [{'name': f'Букет {i}', 'desc': f'Экспериментальная карточка {i}', 'tags': ['тест'],
       'photos': [{'src': svg(i, colors[i - 1]), 'type': 'photo'}],
       'sizes': [{'n': 25, 'cm': 60, 'price': 5900}]} for i in range(1, 11)]
# чётные карточки — с роликом (живые ролики с media.neromashka.ru, CORS *)
VIDS = json.load(open(os.path.join(HERE, 'vids.json'), encoding='utf-8'))
for k, i in enumerate((2, 4, 6, 8)):
    bq[i - 1]['photos'] = [VIDS[k]] + bq[i - 1]['photos']
    bq[i - 1]['name'] = f'Букет {i} · видео'

# на github.io страница живёт в /lenta-exp/: без этого manifest.json ищется в корне
# сайта (404), и иконка на домашнем экране открывается по старому пути
assert html.count('<base href="/">') >= 1
html = html.replace('<base href="/">', '<base href="/lenta-exp/">', 1)

# `black-translucent` теперь в самом шаблоне — проверяем, что он там, и не дублируем
assert 'apple-mobile-web-app-status-bar-style' in html, 'в шаблоне нет строки состояния'

# ═══ ОТКАЧЕНО 14.09.2026, 22:10 — `100lvh` ЭКРАНОМ НЕ ЯВЛЯЕТСЯ ══════════════
# Заход был такой: `screen` зависит от «Вид: Увеличено» (Display Zoom), значит опереть
# таблицу высот часов и условие стеклянного режима на измеренный `100lvh`.
#
# Замер владельца это убил за один скриншот: у него `screen 440x956`, а `lvh 836`.
# `100lvh` — это БОЛЬШОЙ ВЬЮПОРТ, то есть окно со СЛОЖЕННЫМИ панелями Safari, и до
# экрана ему не хватает как раз зоны часов. В таблице 836 нет — условие не прошло, и
# стеклянный режим не включился вовсе: лента свалилась в классический там, где раньше
# работала. Хуже, чем было.
#
# Что остаётся верным: Display Zoom действительно меняет `screen` (владелец воспроизвёл
# полосу у себя переключателем). Но замены ему в опыте нет, а ломать работающее ради
# незакрытой гипотезы нельзя. Возвращаем `screen.height` — он проверен владельцем на
# трёх браузерах. Цена известна и мала: во вкладке при «Увеличено» часы берутся 44
# вместо ~58, карточка уезжает под них на полтора десятка точек меньше.

# ═══ ОПЫТ: РАМА КАДРА — ПО КАРТОЧКЕ (956), А НЕ ПО ВИДИМОМУ ОКНУ ════════════
# Владелец 14.09.2026, 23:55: «и тут сделай кадр длиной 956».
# В шаблоне рама считается по `100lvh` — это окно со сложенными панелями (836 при
# адресе снизу), и картинка вписывается в 836 при карточке 956: сверху и снизу
# остаются поля. Правило обрезки не трогаем, меняем только ВХОД: рама равна высоте
# самой карточки.
РАМА_OLD = """      return Math.min(shot.clientHeight, лвх());"""
assert html.count(РАМА_OLD) == 1, 'рама кадра'
html = html.replace(РАМА_OLD, """      return shot.clientHeight;   /* опыт: рама по карточке, 956 */""")

# ═══ ПОДЪЁМ = ВЫСОТА ЧАСОВ, КОНСТАНТОЙ (владелец 15.09.2026, 00:15) ═════════
# «Мне нравилось, когда в режиме адрес внизу всё красиво работало» — это сборка
# 19:32:56, где подъём был просто высотой часов.
#
# Дальше я дважды пытался считать его точнее: сперва «забранное минус часы» (дало 47
# вместо 62 — владелец увидел щель сверху), потом через `safe-area-inset-bottom`
# (дало 13 — стало хуже). Исследование объяснило, почему обе попытки обречены:
# разложить забранное на верх и низ браузер не даёт вовсе, штатного средства нет, и
# соответствующее предложение в CSSWG до сих пор не реализовано. Значит любая
# «точная» формула — подбор вслепую, а константа хотя бы предсказуема и проверена
# глазом владельца.
ПОДЪЁМ_OLD = """        const T=Math.max(0, Math.round(screen.height-окно-часы));"""
assert html.count(ПОДЪЁМ_OLD) == 1, 'формула подъёма'
html = html.replace(ПОДЪЁМ_OLD, """        const T=часы;   /* опыт: подъём = высота часов, как в сборке 19:32:56 */""")

# ═══ АДРЕС СВЕРХУ — ФОЛБЭК, И РАСПОЗНАЁМ ЭТО ПО `100lvh` (15.09.2026, 00:40) ═
# Владелец: «ты просто не знаешь, сколько затянуть наверх, когда адрес наверху» —
# и это правда. Высоту ВЕРХНЕЙ панели Safari отдельно от нижней браузер не сообщает,
# штатного средства нет, предложение в стандарт открыто и не реализовано. Значит
# честный выход не в том, чтобы подобрать число, а в том, чтобы распознать случай и
# уйти в фолбэк.
#
# Распознаётся он по `100lvh` — это высота окна со СВЁРНУТЫМИ панелями:
#   адрес СНИЗУ: lvh 836 при экране 956 — Safari держит 120 точек под нижнюю панель;
#   адрес СВЕРХУ: lvh 956 — панель сворачивается в ноль, окно равно экрану.
# Оба числа с живых замеров владельца на одной сборке.
#
# Правило: стеклянный режим только когда lvh МЕНЬШЕ экрана. Равен — фолбэк.
СВЕРХУ_OLD = "      && (screen.height - ОКНОБЕЗПАНЕЛЕЙ()) <= 175;"
assert html.count(СВЕРХУ_OLD) == 1, 'условие режима'
html = html.replace(СВЕРХУ_OLD,
    "      && (screen.height - ОКНОБЕЗПАНЕЛЕЙ()) <= 175\n"
    "      /* lvh равен экрану — адресная строка сверху, и на сколько затягивать\n"
    "         карточку под неё, мы не знаем: уходим в фолбэк. */\n"
    "      && ОКНОБЕЗПАНЕЛЕЙ() < screen.height - 1;")

# Слежение: на старте `lvh` бывает ещё не устоявшимся (замер при загрузке дал 894
# там, где живой пробник показывал 956). Поэтому не только решаем один раз, но и
# снимаем стеклянный режим на лету, если lvh дорос до экрана.
СЛЕД_ЯКОРЬ = """    pwaFix();
    addEventListener('resize', pwaFix);"""
assert html.count(СЛЕД_ЯКОРЬ) == 1, 'якорь слежения'
html = html.replace(СЛЕД_ЯКОРЬ, СЛЕД_ЯКОРЬ + """
    /* На старте `lvh` бывает ещё не устоявшимся: замер при загрузке давал 894 там,
       где живой пробник показывал 956. Поэтому следим и дальше — как только он
       дорос до экрана (адресная строка сверху), снимаем стеклянный режим. */
    const сверить=()=>{ try{
      const d=document.createElement('div');
      d.style.cssText='position:absolute;top:0;height:100lvh;visibility:hidden;pointer-events:none';
      (document.body||document.documentElement).appendChild(d);
      const v=d.offsetHeight; d.remove();
      if(v && v >= screen.height-1){
        const к=document.documentElement;
        к.classList.remove('xglass');
        к.style.removeProperty('--xT'); к.style.removeProperty('--xscr');
        window.__xT=0;
      }
    }catch(e){} };
    сверить();
    addEventListener('load', сверить);
    try{ if(window.visualViewport){
      window.visualViewport.addEventListener('resize', сверить, {passive:true}); } }catch(e){}""")

# ═══ ПОВОРОТ ЭКРАНА — УХОДИМ В ФОЛБЭК (владелец 15.09.2026, 00:20) ══════════
# Режим выбирается ОДИН раз при загрузке. Открыть страницу боком не страшно — 440 в
# таблице экранов нет, и стеклянный режим не включится. А вот повернуть УЖЕ открытую
# было дырой: карточка осталась бы ростом 956 при экране 440, и поехало бы всё.
# Чинить пересчётом режима на ходу нельзя — это перевёрстка ленты под пальцем.
# Поэтому при смене ориентации просто снимаем стеклянный режим: карточка становится
# равной окну, то есть тот же фолбэк, что у всех остальных.
ПОВОРОТ_ЯКОРЬ = """    pwaFix();
    addEventListener('resize', pwaFix);"""
assert html.count(ПОВОРОТ_ЯКОРЬ) == 1, 'якорь поворота'
html = html.replace(ПОВОРОТ_ЯКОРЬ, """    pwaFix();
    addEventListener('resize', pwaFix);
    /* ПОВОРОТ — В ФОЛБЭК. Ширина и высота меняются местами, таблица экранов и
       высота часов перестают что-либо значить. Снимаем стеклянный режим целиком:
       карточка становится равной окну, лента ведёт себя как в любом другом
       браузере. Обратно при возврате в портрет НЕ включаем — режим выбирается на
       загрузке, и менять его на ходу значит перевёрстывать ленту под пальцем. */
    const наБоку=()=>{ try{
      if(innerWidth>innerHeight){
        const к=document.documentElement;
        к.classList.remove('xglass');
        к.style.removeProperty('--xT'); к.style.removeProperty('--xscr');
        window.__xT=0;
      }
    }catch(e){} };
    наБоку();
    addEventListener('orientationchange', наБоку);
    addEventListener('resize', наБоку);""")

assert '/*__DATA__*/{}' in html and '<script src="data.js"></script>' in html
html = html.replace('/*__DATA__*/{}', json.dumps({'bouquets': bq}, ensure_ascii=False))
html = html.replace('<script src="data.js"></script>', '')

DIAG = r'''
<div id="xdiag" style="position:fixed;left:6px;top:32%;z-index:99999;pointer-events:none;
 background:rgba(0,0,0,.6);color:#0f0;font:8.5px/1.2 ui-monospace,Menlo,monospace;
 padding:4px 6px;border-radius:6px;white-space:pre-wrap;word-break:break-all;max-width:70vw"></div>
<div id="xprobe" style="position:absolute;left:-9999px;top:0;visibility:hidden">
 <div id="p-vh" style="height:100vh"></div><div id="p-svh" style="height:100svh"></div>
 <div id="p-lvh" style="height:100lvh"></div><div id="p-dvh" style="height:100dvh"></div>
 <div id="p-sat" style="height:env(safe-area-inset-top,0px)"></div>
 <div id="p-sab" style="height:env(safe-area-inset-bottom,0px)"></div></div>
<script>
(function(){
  const el=document.getElementById('xdiag');
  try{
    const st=document.createElement('style');
    st.textContent=
      /* ═══ ОПЫТ 14.09.2026: ЗАЛИТЬ ПОЛОСУ, КОТОРУЮ iOS НЕ ОТДАЛА ОКНУ ═══════
         На трёх телефонах из четырёх iOS даёт иконке окно ровно на высоту часов
         меньше экрана (956→894, 812→768), и снизу остаётся глухая чёрная полоса.
         Ключ к ней — `100vh`: он на этих же телефонах равен ЭКРАНУ (956), а не
         окну (894). Значит слой `100vh`, прибитый к верху окна, физически
         накрывает полосу — проверяем именно это.

         Геометрия ленты НЕ трогается: слой лежит ПОД всем (`z-index:-1`), высоту
         карточки, снап и обвязку не меняет. Не сработает — пропадёт только
         заливка, лента останется прежней. */
      'html.xpwawin #xfill{position:fixed;left:0;right:0;top:0;height:100vh;z-index:-1;'+
        'pointer-events:none;background:#0b0a09 center/cover no-repeat;'+
        'background-image:var(--xfill-src,none);filter:blur(30px) brightness(.82) saturate(1.2);'+
        'transform:scale(1.15)}'+
      'html:not(.xpwawin) #xfill{display:none}';

    document.head.appendChild(st);
    const fill=document.createElement('div'); fill.id='xfill';
    document.body.insertBefore(fill, document.body.firstChild);
  }catch(e){}
  /* В ПЛИТКЕ ПЛАШКА ТОЖЕ НУЖНА (владелец 15.09.2026: «поставь на плитку
     индикаторы те же, что на ленту, будем разбираться»). В ленте она живёт внутри
     обвязки `#feedchrome`, а в плитке обвязка скрыта — вместе с ней пропадала и
     плашка. В плитке держим её прямо в теле и прибиваем к окну. */
  function hostIt(){
    const плитка=document.body.classList.contains('gridmode');
    if(плитка){
      if(el.parentNode!==document.body){ document.body.appendChild(el); }
      el.style.position='fixed'; el.style.top='32%'; el.style.left='6px';
      return;
    }
    const host=document.getElementById('feedchrome');
    if(host&&el.parentNode!==host){ host.appendChild(el);
      el.style.position='absolute'; el.style.top='150px'; el.style.left='8px'; }
  }
  hostIt(); setInterval(hostIt,1000);
  const h=id=>{const e=document.getElementById(id);return e?Math.round(e.getBoundingClientRect().height):'?';};
  const R=v=>Math.round(v*10)/10;
  const yn=b=>b?'да':'НЕТ';
  function where(){
    const u=navigator.userAgent;
    /* `navigator.standalone` у ВСТРОЕННОГО Safari внутри приложения тоже true —
       называть это «иконкой» значило бы врать в единственном месте, ради которого
       плашка и заведена. Иконку от встроенного отличаем по обвязке вокруг
       страницы: у иконки браузер забирает разве что часы, у встроенного — 218. */
    const сам=matchMedia('(display-mode:standalone)').matches||navigator.standalone;
    if(сам) return (screen.height-innerHeight)<=80 ? 'иконка (PWA)' : 'Safari внутри приложения';
    if(/WhatsApp/i.test(u)) return 'WhatsApp';
    if(/Telegram/i.test(u)) return 'Telegram';
    if(/Instagram/i.test(u)) return 'Instagram';
    if(/FBAN|FBAV/i.test(u)) return 'Facebook';
    if(/YaBrowser/i.test(u)) return 'Яндекс.Браузер';
    if(/CriOS/i.test(u)) return 'Chrome iOS';
    if(/FxiOS/i.test(u)) return 'Firefox iOS';
    if(/EdgiOS/i.test(u)) return 'Edge iOS';
    if(/iPhone|iPad/.test(u)&&/Safari/.test(u)&&/Version\//.test(u)) return 'Safari';
    if(/iPhone|iPad/.test(u)) return 'встроенный (WebView)';
    if(/Chrome/.test(u)) return 'Chrome';
    return 'другое';
  }
  function vstate(){
    try{
      const f=k=>{const s=слайдПо(k);const v=s&&s.querySelector('video.fg[src]');
        return v?(v.paused?'пауза':'ИГРАЕТ')+' '+v.currentTime.toFixed(1):'—';};
      return 'тек '+f(idx)+' · след '+f(idx+1);
    }catch(e){return '-';}
  }
  function draw(){
    try{
      const vv=window.visualViewport||{};
      const d=document.documentElement;
      let sl=null,st='-',sh='-',sb='-',ix='-';
      try{ ix=(typeof idx!=='undefined')?idx:'-'; sl=(typeof слайдПо==='function')&&слайдПо(idx); }catch(e){}
      if(sl){const r=sl.getBoundingClientRect(); st=R(r.top); sh=R(r.height); sb=R(r.bottom);}
      el.textContent=
        'innerW×H   '+innerWidth+'×'+innerHeight+'\n'+
        'visualVP   '+R(vv.width||0)+'×'+R(vv.height||0)+'\n'+
        'vv.offTop  '+R(vv.offsetTop||0)+'  pageTop '+R(vv.pageTop||0)+'\n'+
        'screen     '+screen.width+'×'+screen.height+'\n'+
        'забрал бр. '+(screen.height-innerHeight)+' (экран−окно: часы+панели)\n'+
        'забрал lvh '+(screen.height-(window.__lvh||0))+'  (по нему и решаем)\n'+
        'сборка     '+(window.__СБОРКА||'старая')+'\n'+
        'clientH    '+d.clientHeight+'\n'+
        'vh/svh     '+h('p-vh')+' / '+h('p-svh')+'\n'+
        'lvh/dvh    '+h('p-lvh')+' / '+h('p-dvh')+'\n'+
        'safe t/b   '+h('p-sat')+' / '+h('p-sab')+'\n'+
        'scrollY    '+R(scrollY)+'\n'+
        'docH       '+d.scrollHeight+'\n'+
        'idx        '+ix+'  поз '+(typeof позицияЛенты==='function'?R(позицияЛенты()*1000)/1000:'-')+'\n'+
        'видео      '+vstate()+'\n'+
        'slide top  '+st+'\n'+
        'slide h    '+sh+'\n'+
        'slide bot  '+sb+'\n'+
        'docscroll  '+d.classList.contains('docscroll')+'\n'+
        /* ── ПЛИТКА ── (владелец 15.09.2026: разбираемся, почему каталог не до низа) */
        (document.body.classList.contains('gridmode') ? (()=>{
          const п=(s)=>{const e=document.querySelector(s); if(!e) return '—';
            const r=e.getBoundingClientRect();
            return Math.round(r.top)+'…'+Math.round(r.bottom)+' h'+Math.round(r.height);};
          const c=document.querySelector('.catin');
          return 'ПЛИТКА\n'+
            'cat        '+п('.cat')+'\n'+
            'catin      '+п('.catin')+'\n'+
            'catin скр  '+(c?Math.round(c.scrollTop)+' / '+Math.round(c.scrollHeight):'—')+'\n'+
            'таблетка   '+п('.tabbar')+'\n'+
            'до низа    '+(()=>{const t=document.querySelector('.tabbar');
              if(!t) return '—';
              /* в экранных точках: окно начинается ниже часов, если полоса сверху */
              const сверху=(d.classList.contains('xpwawin')&&!d.classList.contains('xpwadown'))?screen.height-innerHeight:0;
              return Math.round(screen.height-сверху-t.getBoundingClientRect().bottom);})()+' (экран−низ таблетки)\n'+
            'полоса     '+(d.classList.contains('xpwawin')?(d.classList.contains('xpwadown')?'снизу':'сверху'):'—')+'\n';
        })() : '')+
        'заливка    '+d.classList.contains('xpwawin')+'\n'+
        'coarse     '+matchMedia('(hover:none) and (pointer:coarse)').matches+'\n'+
        'standalone '+matchMedia('(display-mode:standalone)').matches+'\n'+
        '── браузер ──\n'+
        'где        '+where()+(d.classList.contains('xglass')?'  [под панели]':'  [в окно]')+'\n'+
        'iOS        '+(((/OS (\d+)_(\d+)(?:_(\d+))?/.exec(navigator.userAgent)||[]).slice(1).filter(Boolean).join('.'))||'-')+'\n'+
        'Safari ver '+(((/Version\/([\d.]+)/.exec(navigator.userAgent))||[])[1]||'-')+'\n'+
        'DPR        '+devicePixelRatio+'  zoom '+R(vv.scale||1)+'\n'+
        'ориент.    '+((screen.orientation&&screen.orientation.type)||(innerWidth>innerHeight?'land':'port'))+'\n'+
        'тир        '+((typeof TIER!=='undefined')?TIER:'-')+'\n'+
        'ядра/пам   '+(navigator.hardwareConcurrency||'-')+' / '+(navigator.deviceMemory||'-')+'\n'+
        'сеть       '+(((navigator.connection||{}).effectiveType)||'-')+(((navigator.connection||{}).saveData)?' saveData':'')+'\n'+
        'движение   '+(matchMedia('(prefers-reduced-motion:reduce)').matches?'УМЕНЬШ.':'обычн.')+
          '  тема '+(matchMedia('(prefers-color-scheme:dark)').matches?'тёмн':'светл')+'\n'+
        'контраст   '+(matchMedia('(prefers-contrast:more)').matches?'повыш':'обычн')+
          '  прозр '+(matchMedia('(prefers-reduced-transparency:reduce)').matches?'УМЕНЬШ':'обычн')+'\n'+
        'умеет      dvh:'+yn(CSS.supports('height','100dvh'))+' snap:'+yn(CSS.supports('scroll-snap-type','y mandatory'))+
          ' blur:'+yn(CSS.supports('backdrop-filter','blur(1px)')||CSS.supports('-webkit-backdrop-filter','blur(1px)'))+
          ' cv:'+yn(CSS.supports('content-visibility','auto'))+'\n'+
        'касания    '+(navigator.maxTouchPoints||0)+'  язык '+navigator.language+'\n'+
        'viewport   '+(((document.querySelector('meta[name=viewport]')||{}).content)||'-').replace(/\s+/g,'')+'\n'+
        'UA '+navigator.userAgent.replace(/Mozilla\/5\.0 /,'');
      el.textContent=el.textContent.split('\n').map(l=>(l.match(/.{1,46}/g)||['']).join('\n   ')).join('\n');
    }catch(e){ el.textContent='diag err '+e; }
  }
  function edges(){
    document.querySelectorAll('.feed .slide').forEach((s,k)=>{
      if(s.querySelector(':scope>.xedge')) return;
      const d=document.createElement('div'); d.className='xedge';
      d.style.cssText='position:absolute;left:0;right:0;top:0;bottom:0;z-index:60;pointer-events:none;'+
        'border-top:8px solid #ff0;border-bottom:8px solid #0ff;box-sizing:border-box';
      const n=(typeof номерСлайда==='function')?номерСлайда(s)+1:k+1;
      d.innerHTML='<b style="position:absolute;top:8px;left:50%;transform:translateX(-50%);background:#ff0;color:#000;font:700 13px sans-serif;padding:1px 6px">ВЕРХ КАРТОЧКИ '+n+'</b>'+
        '<b style="position:absolute;bottom:8px;left:50%;transform:translateX(-50%);background:#0ff;color:#000;font:700 13px sans-serif;padding:1px 6px">НИЗ КАРТОЧКИ '+n+'</b>';
      if(getComputedStyle(s).position==='static') s.style.position='relative';
      s.appendChild(d);
    });
  }
  /* Заливка берёт кадр ТЕКУЩЕЙ карточки: под полосой должно быть продолжение
     того, что человек видит, а не случайная картинка. */
  function fillSrc(){
    try{
      const d=document.documentElement;
      if(!d.classList.contains('xpwawin')) return;
      const s=слайдПо(idx); if(!s) return;
      const m=s.querySelector('video.fg[poster]')||s.querySelector('img.fg')||s.querySelector('.bg>img');
      const u=m?(m.getAttribute('poster')||m.currentSrc||m.src):'';
      if(!u) return;
      const было=d.style.getPropertyValue('--xfill-src');
      const надо='url("'+u+'")';
      if(было!==надо) d.style.setProperty('--xfill-src',надо);
    }catch(e){}
  }
  function cur(){
    try{ const s=слайдПо(idx);
      document.querySelectorAll('.feed .slide.xcur').forEach(x=>{ if(x!==s) x.classList.remove('xcur'); });
      if(s&&!s.classList.contains('xcur')) s.classList.add('xcur'); }catch(e){}
  }
  /* плашка — 4 раза в секунду, не каждый кадр: не мешать листанию */
  setInterval(()=>{draw();edges();cur();fillSrc();},250);
})();
</script>
'''
import datetime
МЕТКА = datetime.datetime.now().strftime('%H:%M:%S')
html = html.replace('</body>', '<script>window.__СБОРКА=' + repr(МЕТКА) + ';</script>' + DIAG + '</body>') \
    if '</body>' in html else html + DIAG
open(OUT, 'w', encoding='utf-8').write(html)
print('ok', len(html))
