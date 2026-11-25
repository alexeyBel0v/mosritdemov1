(()=>{
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const S=window.SITE||{};
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const store={get:k=>{try{return localStorage.getItem(k)}catch(e){return null}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}}};

const goal=n=>{try{if(window.ym&&S.ym)window.ym(S.ym,'reachGoal',n)}catch(e){}};
document.addEventListener('click',e=>{
  if(e.target.closest('a[href^="tel:"]'))goal('call');
  const g=e.target.closest('[data-goal]');if(g)goal(g.dataset.goal);
});

const header=$('#header'),fab=$('#fab');
const onScroll=()=>{const y=scrollY;header&&header.classList.toggle('scrolled',y>8);fab&&fab.classList.toggle('show',y>600)};
addEventListener('scroll',onScroll,{passive:true});onScroll();

const big=$('#bigText');
if(store.get('mr-large')==='1')document.documentElement.classList.add('large');
big&&big.addEventListener('click',()=>{const on=document.documentElement.classList.toggle('large');big.setAttribute('aria-pressed',on);store.set('mr-large',on?'1':'0')});

const lock=o=>{document.body.style.overflow=o?'hidden':''};
const menu=$('#menu'),mOpen=$('#menuOpen');
const setMenu=o=>{if(!menu)return;menu.classList.toggle('open',o);menu.setAttribute('aria-hidden',!o);mOpen.setAttribute('aria-expanded',o);lock(o);if(o)setTimeout(()=>menu.querySelector('[data-menu-close]').focus(),300);else mOpen.focus()};
mOpen&&mOpen.addEventListener('click',()=>setMenu(true));
$$('[data-menu-close]').forEach(b=>b.addEventListener('click',()=>setMenu(false)));

const help=$('#help'),orb=$('#orb');
const setHelp=o=>{if(!help)return;help.classList.toggle('open',o);help.setAttribute('aria-hidden',!o);lock(o);if(o)setTimeout(()=>$('#helpPhone').focus(),200);else orb&&orb.focus()};
orb&&orb.addEventListener('click',()=>setHelp(true));
$$('[data-help-close]').forEach(b=>b.addEventListener('click',()=>setHelp(false)));
addEventListener('keydown',e=>{if(e.key!=='Escape')return;if(help&&help.classList.contains('open'))setHelp(false);else if(menu&&menu.classList.contains('open'))setMenu(false)});
const copyBtn=$('#copyBtn');
copyBtn&&copyBtn.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(S.phone);copyBtn.textContent='Номер скопирован'}catch(e){const r=document.createRange();r.selectNodeContents($('#helpPhone'));getSelection().removeAllRanges();getSelection().addRange(r);copyBtn.textContent='Номер выделен, скопируйте его'}});

const clock=$('#clock');
if(clock){const tick=()=>{try{clock.textContent=new Intl.DateTimeFormat('ru-RU',{hour:'2-digit',minute:'2-digit',timeZone:'Europe/Moscow'}).format(new Date())}catch(e){}};tick();setInterval(tick,15000)}

$$('.case-btn').forEach(b=>b.addEventListener('click',()=>{const c=b.closest('.case'),o=!c.classList.contains('open');c.classList.toggle('open',o);b.setAttribute('aria-expanded',o)}));

$$('.q button').forEach(b=>b.addEventListener('click',()=>{const q=b.parentElement,o=!q.classList.contains('open');
  q.parentElement.querySelectorAll('.q.open').forEach(x=>{x.classList.remove('open');x.querySelector('button').setAttribute('aria-expanded','false')});
  q.classList.toggle('open',o);b.setAttribute('aria-expanded',o)}));

const place=(ind,b)=>{ind.style.width=b.offsetWidth+'px';ind.style.transform=`translateX(${b.offsetLeft-5}px)`};
const plist=$('#plist'),segBtns=$$('#seg button'),segInd=$('#segInd');
if(plist&&S.packs){
  const draw=k=>{plist.innerHTML=S.packs[k].map(p=>`<article class="plan${p.mid?' mid':''}"><span class="tag">${p.tag||''}</span><h3>${p.name}</h3><p class="desc">${p.desc}</p><div class="price num"><small>от</small>${p.price} ₽</div><ul>${p.items.map(i=>`<li>${i}</li>`).join('')}</ul><a href="#contact" class="pill ${p.mid?'pill-ink':'pill-line'}">Обсудить с агентом</a></article>`).join('')};
  const setK=(b,first)=>{segBtns.forEach(x=>x.setAttribute('aria-pressed',x===b));place(segInd,b);
    if(first){draw(b.dataset.k);return}
    plist.classList.add('swap');setTimeout(()=>{draw(b.dataset.k);requestAnimationFrame(()=>requestAnimationFrame(()=>plist.classList.remove('swap')))},300)};
  segBtns.forEach(b=>b.addEventListener('click',()=>{if(b.getAttribute('aria-pressed')!=='true')setK(b)}));
  setK(segBtns[0],true);
  const re=()=>place(segInd,segBtns.find(b=>b.getAttribute('aria-pressed')==='true'));
  addEventListener('resize',re);document.fonts&&document.fonts.ready.then(re);
}

const fmt=n=>new Intl.NumberFormat('ru-RU',{minimumFractionDigits:n%1?2:0,maximumFractionDigits:2}).format(n)+' ₽';
if($('#calc')&&S.calc){
  const P=S.calc,C={kind:'crem',hall:'0',who:'msk'};
  const cBody=$('#cBody'),cBus=$('#cBus'),cG=$('#cGuests');let used=false;
  const calc=()=>{
    const g=+cG.value;
    const lines=[[C.kind==='crem'?'Кремация: документы, гроб, катафалк, урна':'Захоронение: документы, гроб, катафалк, копка',P.base[C.kind]]];
    if(P.hall[C.hall])lines.push(['Зал прощания, '+C.hall+' минут',P.hall[C.hall]]);
    if(cBody.checked)lines.push(['Подготовка тела и одежда',P.body]);
    if(cBus.checked)lines.push(['Автобус для родных',P.bus]);
    if(g)lines.push(['Поминальный обед, '+g+' человек',g*P.guest]);
    const total=lines.reduce((s,l)=>s+l[1],0),ben=P.benefit[C.who];
    $('#cTotal').textContent=fmt(total);
    $('#cLines').innerHTML=lines.map(l=>`<li><span>${l[0]}</span><b class="num">${fmt(l[1])}</b></li>`).join('');
    $('#cBenefit').textContent=(C.who==='reg'?'от −':'−')+fmt(ben);
    $('#cNet').textContent=fmt(Math.max(0,Math.round((total-ben)*100)/100));
    $('#gOut').textContent=g?g+' человек':'не нужен';
  };
  const touch=()=>{if(!used){used=true;goal('calc_use')}};
  $$('.chips').forEach(ch=>ch.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;ch.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));C[ch.dataset.name]=b.dataset.v;calc();touch()}));
  [cBody,cBus,cG].forEach(i=>i.addEventListener('input',()=>{calc();touch()}));
  const cta=$('#cCta');cta&&cta.addEventListener('click',()=>{const t=$('#fTopic');if(t)t.value='Узнать цены'});
  calc();
}

const tr=$('#rvTrack');
if(tr){
  const prev=$('#rvPrev'),next=$('#rvNext'),step=()=>tr.querySelector('.rv').offsetWidth+24;
  const upd=()=>{prev.disabled=tr.scrollLeft<4;next.disabled=tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-4};
  prev.addEventListener('click',()=>tr.scrollBy({left:-step(),behavior:'smooth'}));
  next.addEventListener('click',()=>tr.scrollBy({left:step(),behavior:'smooth'}));
  tr.addEventListener('scroll',upd,{passive:true});upd();
}

const digits=v=>v.replace(/\D/g,'').replace(/^[78]/,'').slice(0,10);
const formatPhone=v=>{const d=digits(v);if(!d)return'';let s='+7 ('+d.slice(0,3);if(d.length>3)s+=') '+d.slice(3,6);if(d.length>6)s+='-'+d.slice(6,8);if(d.length>8)s+='-'+d.slice(8,10);return s};
const esc=s=>String(s).replace(/[<>&"]/g,'');
$$('form[data-lead]').forEach(f=>{
  const ph=f.querySelector('[data-phone]'),agree=f.querySelector('[data-agree]'),msg=f.querySelector('[data-msg]'),btn=f.querySelector('[type=submit]');
  const say=(t,bad)=>{msg.textContent=t;msg.classList.toggle('bad',!!bad)};
  ph.addEventListener('input',()=>{ph.value=formatPhone(ph.value);ph.classList.remove('bad')});
  f.addEventListener('submit',async e=>{
    e.preventDefault();
    if(digits(ph.value).length!==10){ph.classList.add('bad');say('Введите номер полностью: 10 цифр после +7.',true);ph.focus();return}
    if(agree&&!agree.checked){say('Отметьте согласие на обработку данных, без него заявку принять нельзя.',true);return}
    const data={phone:'+7'+digits(ph.value),name:(f.elements.name||{}).value||'',topic:(f.elements.topic||{}).value||'',page:location.pathname,hp:(f.elements.hp||{}).value||''};
    btn.disabled=true;say('Отправляем…');
    try{
      const r=await fetch(S.lead,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
      if(!r.ok)throw new Error(r.status);
      goal('lead');
      f.innerHTML=`<div class="done"><h3>Заявка принята${data.name?', '+esc(data.name):''}</h3><p>Дежурный перезвонит на номер ${esc(ph.value)} в течение пяти минут.</p></div>`;
    }catch(err){
      btn.disabled=false;
      say(`Не получилось отправить заявку. Позвоните нам: ${S.phone}, мы на связи круглосуточно.`,true);
    }
  });
});

const ck=$('#cookie');
if(ck&&S.ym&&store.get('mr-ck')!=='1'){setTimeout(()=>{ck.hidden=false},1800);$('#cookieOk').addEventListener('click',()=>{ck.hidden=true;store.set('mr-ck','1')})}

const say=$('#say');
if(say){
  say.innerHTML=say.textContent.trim().split(/\s+/).map(w=>`<span class="w">${w}</span>`).join(' ');
  const words=$$('#say .w');
  if(reduce)words.forEach(w=>w.classList.add('on'));
  else{
    const run=()=>{const r=say.getBoundingClientRect(),vh=innerHeight;const p=Math.min(1,Math.max(0,(vh*.85-r.top)/(r.height+vh*.4)));const n=Math.round(p*words.length);words.forEach((w,i)=>w.classList.toggle('on',i<n))};
    addEventListener('scroll',run,{passive:true});run();
  }
}
const fill=$('#trackFill');
if(fill&&!reduce){
  const tk=$('#track');fill.style.setProperty('--p',0);
  const run=()=>{const r=tk.getBoundingClientRect(),vh=innerHeight;fill.style.setProperty('--p',Math.min(1,Math.max(0,(vh*.8-r.top)/(vh*.5))))};
  addEventListener('scroll',run,{passive:true});run();
}
})();
