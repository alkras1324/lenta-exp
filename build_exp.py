import json, urllib.parse, sys, os
TPL = r'D:\Работа\ИИ\roma4u\.claude\worktrees\feed-3267-debug\docs\design\prototypes\feed\index.template.html'
OUT = r'C:\Users\yanus\AppData\Local\Temp\claude\D------------roma4u\c46718c0-fb1f-440f-be6f-0bb617195067\scratchpad\lenta-exp\index.html'
html = open(TPL, encoding='utf-8').read()
colors = ['#c0392b','#8e44ad','#2980b9','#16a085','#d35400','#27ae60','#7f8c8d','#e84393','#f39c12','#34495e']
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
       'photos': [{'src': svg(i, colors[i-1]), 'type': 'photo'}],
       'sizes': [{'n': 25, 'cm': 60, 'price': 5900}]} for i in range(1, 11)]
# чётные карточки — с роликом (живые ролики с media.neromashka.ru, CORS *)
VIDS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vids.json'), encoding='utf-8'))
for k, i in enumerate((2, 4, 6, 8)):
    bq[i-1]['photos'] = [VIDS[k]] + bq[i-1]['photos']
    bq[i-1]['name'] = f'Букет {i} · видео'
POS_OLD = 'const позицияЛенты=()=>{ const h=высотаСлайда(); return окноОт+(h?ПРОКРУТЧИК.scrollTop/h:0); };'
POS_NEW = ('const позицияЛенты=()=>{ const h=высотаСлайда(); if(!h) return окноОт; '
           'let E=0; try{ if(ДОКПРОКРУТКА&&document.documentElement.classList.contains("xglass")) E=parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--xT"))||0; }catch(e){} '
           'return окноОт+(ПРОКРУТЧИК.scrollTop-E)/h; };')
assert POS_OLD in html; html = html.replace(POS_OLD, POS_NEW)
# рама кадра — по видимому окну, а не по карточке-экрану (правило обрезки то же, меняется только вход)
RAMA_OLD = 'shot.clientWidth/shot.clientHeight'
RAMA_NEW = 'shot.clientWidth/((ДОКПРОКРУТКА&&document.documentElement.classList.contains("xglass"))?Math.min(shot.clientHeight,innerHeight):shot.clientHeight)'
assert html.count(RAMA_OLD) >= 2; html = html.replace(RAMA_OLD, RAMA_NEW)
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
  /* досылка позиции скриптом стаскивала бы карточку к краю окна — на опыте выключена */
  try{ переложитьНаСлайд=function(){}; }catch(e){}
  try{
    const st=document.createElement('style');
    const u=navigator.userAgent, ver=+((/Version\/(\d+)/.exec(u)||[])[1]||0);
    const GLASS=/iPhone|iPad/.test(u)&&/Safari/.test(u)&&ver>=26&&!/CriOS|FxiOS|EdgiOS|YaBrowser|OPiOS|GSA|Telegram|Instagram|FBAN|FBAV|WhatsApp/.test(u)
      &&!(matchMedia('(display-mode:standalone)').matches||navigator.standalone);
    if(GLASS) document.documentElement.classList.add('xglass');
    const u=navigator.userAgent, ver=+((/Version\/(\d+)/.exec(u)||[])[1]||0);
    const GLASS=/iPhone|iPad/.test(u)&&/Safari/.test(u)&&ver>=26&&!/CriOS|FxiOS|EdgiOS|YaBrowser|OPiOS|GSA|Telegram|Instagram|FBAN|FBAV|WhatsApp/.test(u)
      &&!(matchMedia('(display-mode:standalone)').matches||navigator.standalone);
    if(GLASS) document.documentElement.classList.add('xglass');
    const u=navigator.userAgent, ver=+((/Version\/(\d+)/.exec(u)||[])[1]||0);
    const GLASS=/iPhone|iPad/.test(u)&&/Safari/.test(u)&&ver>=26&&!/CriOS|FxiOS|EdgiOS|YaBrowser|OPiOS|GSA|Telegram|Instagram|FBAN|FBAV|WhatsApp/.test(u)
      &&!(matchMedia('(display-mode:standalone)').matches||navigator.standalone);
    if(GLASS) document.documentElement.classList.add('xglass');
    const H=screen.height+'px', E='('+H+' - 100dvh)';
    /* высота часов (верхняя зона): Safari её не сообщает — по таблице экранов iPhone */
    const TT={956:62,932:59,874:62,852:59,926:47,844:47,896:44,812:44,667:20,736:20}[screen.height];
    const T=(TT!=null?TT:Math.round((screen.height-innerHeight)*0.4))+'px';
    document.documentElement.style.setProperty('--xT',T);
    st.textContent=
      /* карточка = окно + 2 × запас; запас = screen − окно (закрывает зоны часов и нижней строки) */
      /* только телефон с прокруткой документом: на десктопе карточка в рамке, панелей поверх нет */
      '@media (hover:none) and (pointer:coarse){'+
      'html.docscroll.xglass .slide{height:'+H+'!important;'+
      /* снап останавливает по видимой середине: отрицательные поля на запас */
      'scroll-snap-align:start!important;scroll-margin-top:calc(-1 * '+T+')!important;scroll-margin-bottom:0!important}'+
      /* подпись поднимается на запас, чтобы стоять над «Купить» */
      'html.docscroll.xglass{--окно-добор:calc'+E+'!important}'+
      /* подпись прибита к кнопкам, а не к картинке: стоит на месте, при листании только гаснет */
      'html.docscroll.xglass .slide:not(.hero) .cap{--окно-добор:calc('+H+' - '+T+' - 100dvh)!important}'+
      'html.docscroll .slide:not(.xcur) .cap{opacity:0!important;visibility:hidden!important}}'+
      ':root{--cap-добор:0px!important}'+
      '.slide .cap{transition:opacity .25s ease}body.swiping .slide .cap{opacity:0!important}'+
      /* кнопки и таблетка — одно состояние: не гаснут при листании, стекло не пропадает */
      /* контейнер не гасим (иначе стекло кнопок пропадает и впрыгивает третьим шагом) —
         гаснет каждая кнопка сама: два состояния, стекло цело */
      '#feedacts{transition:none!important}body.swiping #feedacts{opacity:1!important}'+
      '#feedacts .rail button,#feedacts .acts button,.tabbar{transition:opacity .3s ease!important}'+
      'body.swiping #feedacts .rail button,body.swiping #feedacts .acts button,body.swiping .tabbar{opacity:.34!important}';
    document.head.appendChild(st);
  }catch(e){}
  function hostIt(){
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
    if(matchMedia('(display-mode:standalone)').matches||navigator.standalone) return 'иконка (PWA)';
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
        'coarse     '+matchMedia('(hover:none) and (pointer:coarse)').matches+'\n'+
        'standalone '+matchMedia('(display-mode:standalone)').matches+'\n'+
        '── браузер ──\n'+
        'где        '+where()+'\n'+
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
  function cur(){
    try{ const s=слайдПо(idx);
      document.querySelectorAll('.feed .slide.xcur').forEach(x=>{ if(x!==s) x.classList.remove('xcur'); });
      if(s&&!s.classList.contains('xcur')) s.classList.add('xcur'); }catch(e){}
  }
  const tick=()=>{draw();edges();cur();requestAnimationFrame(tick);};
  requestAnimationFrame(tick);
})();
</script>
'''
html = html.replace('</body>', DIAG + '</body>') if '</body>' in html else html + DIAG
open(OUT, 'w', encoding='utf-8').write(html)
print('ok', len(html))
