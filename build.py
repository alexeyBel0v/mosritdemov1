import re, json, html, shutil, sys, datetime
from pathlib import Path
from content_a import SITE, P, SERVICES
from content_b import GOODS, MEMORIAL, COMPANY, ARTICLES, DISTRICTS
from content_c import EXTRA, crematorium_pages
from content_legal import LEGAL

ROOT = Path(__file__).parent
TODAY = datetime.date.today().isoformat()
H = html.escape


def hubs():
    def cards(slugs):
        return [(PAGES[s]["crumb"], PAGES[s]["desc"].split(".")[0] + ".", s, PAGES[s].get("price") and f"от {PAGES[s]['price']} ₽") for s in slugs]
    svc = [p["slug"] for p in SERVICES] + ["ritualnyj-transport"]
    return [
        {"slug": "uslugi", "crumb": "Услуги", "title": "Ритуальные услуги в Москве: полный список и цены | Мосритуалист",
         "h1": "Ритуальные услуги в Москве", "desc": "Все ритуальные услуги в Москве и области: организация похорон, кремация, захоронение, перевозка, груз 200, отпевание, поминки. Цены от, круглосуточно.",
         "lead": "Можно заказать похороны под ключ или отдельные услуги. Цена каждой услуги фиксируется в договоре.",
         "facts": [("24/7", "принимаем звонки"), ("0 ₽", "выезд агента"), ("Договор", "цена не меняется")],
         "body": [("cards", lambda: cards(svc))], "faq": [], "related": []},
        {"slug": "tovary", "crumb": "Ритуальные товары", "title": "Ритуальные товары в Москве: гробы, урны, венки, кресты | Мосритуалист",
         "h1": "Ритуальные товары", "desc": "Гробы, урны для праха, венки, одежда для покойного, кресты и таблички в Москве. Доставка в морг, подбор по видеосвязи.",
         "lead": "Всё нужное для прощания с доставкой в морг или к месту похорон. Покажем товары по видеосвязи, если не хотите ехать в офис.",
         "facts": [], "body": [("cards", lambda: cards([g["slug"] for g in GOODS]))], "faq": [], "related": []},
        {"slug": "poleznoe", "crumb": "Полезное", "title": "Полезное: инструкции и ответы о похоронах | Мосритуалист",
         "h1": "Полезное в трудный момент", "desc": "Что делать, если умер человек, какие документы нужны, как получить пособие, кремация или захоронение, памятники.",
         "lead": "Короткие и понятные инструкции. Без рекламы и лишних слов.",
         "facts": [], "body": [("cards", lambda: cards([a["slug"] for a in ARTICLES + [EXTRA[1]]] + ["posobie-na-pogrebenie", "socialnye-pohorony"]))], "faq": [], "related": []},
        {"slug": "kladbishcha-moskvy", "crumb": "Кладбища Москвы", "title": "Кладбища Москвы по округам: открытые и закрытые | Мосритуалист",
         "h1": "Кладбища Москвы по округам", "desc": "Кладбища Москвы по округам, какие открыты для новых захоронений, где возможны только родственные подзахоронения. Организуем похороны на любом кладбище.",
         "lead": "Большинство кладбищ Москвы закрыты для новых захоронений, но принимают подзахоронения в родственные могилы. Бесплатное место дают на открытых кладбищах.",
         "facts": [("5", "открытых кладбищ с бесплатными местами"), ("15 лет", "до подзахоронения гробом"), ("Без срока", "для урны")],
         "body": [("h2", "Открытые кладбища"), ("ul", ["Алабушевское (Зеленоград)", "Домодедовское (Южное)", "Хованское (Центральное)", "Захарьинское", "Ястребковское"]),
                  ("p", "Список по данным портала mos.ru. Наличие мест меняется, агент проверит его в день обращения."),
                  ("h2", "Кладбища по округам"), ("cards", lambda: cards([f"rajony/{d[0]}" for d in DISTRICTS])),
                  ("p", "Крематории — на странице [[krematorii|крематориев Москвы]].")],
         "faq": [], "related": ["zahoronenie", "krematorii"]},
    ]


def district_pages():
    out = []
    for slug, name, where, cems, crem, note in DISTRICTS:
        out.append({
            "slug": f"rajony/{slug}", "crumb": name, "parent": "kladbishcha-moskvy",
            "title": f"Ритуальные услуги {where}, похороны 24/7 | Мосритуалист",
            "h1": f"Ритуальные услуги {where}",
            "desc": f"Организация похорон {where} от {P['org']} ₽: агент приедет за 60 минут, кладбища {where}, кремация, пособие до 25 988 ₽. Круглосуточно.",
            "lead": f"Агент приезжает {where} в течение часа. Оформим документы, договоримся с моргом и кладбищем, организуем прощание и поминки.",
            "facts": [("60 минут", "до приезда агента"), (f"от {P['org']} ₽", "похороны под ключ"), ("24/7", "без выходных")],
            "body": [
                ("h2", f"Кладбища {where}"),
                ("ul", [c + " кладбище" for c in cems]),
                ("p", note),
                ("h2", "Кремация"),
                ("p", crem + " Подробнее — на странице [[krematorii|крематориев Москвы]]."),
                ("h2", "Что мы делаем"),
                ("ul", ["[[organizaciya-pohoron|организация похорон под ключ]]", "[[kremaciya|кремация]] и [[kolumbarij|место в колумбарии]]", "[[zahoronenie|захоронение]] и подзахоронение в родственную могилу", "[[perevozka-umershego|перевозка умершего]]", "[[pamyatniki|памятники]] и [[blagoustrojstvo-mogil|благоустройство]]"]),
            ],
            "faq": [], "related": ["organizaciya-pohoron", "zahoronenie", "posobie-na-pogrebenie"],
        })
    return out


CENY = {
    "slug": "ceny", "crumb": "Цены", "title": "Цены на похороны в Москве 2026: калькулятор и комплексы | Мосритуалист",
    "h1": "Цены на похороны в Москве", "desc": f"Цены на ритуальные услуги в Москве 2026: похороны от {P['org']} ₽, кремация от {P['crem']} ₽. Калькулятор стоимости с учётом пособия до 25 988 ₽.",
    "lead": "Цена фиксируется в договоре и после подписания не меняется. Прикиньте сумму в калькуляторе или посмотрите готовые комплексы.",
    "facts": [(f"от {P['org']} ₽", "похороны под ключ"), ("до 25 988 ₽", "вернёт пособие"), ("0 ₽", "предоплата")],
    "special": "ceny", "body": [], "faq": [], "related": ["posobie-na-pogrebenie", "socialnye-pohorony", "uslugi"],
}

ALL = SERVICES + EXTRA + GOODS + MEMORIAL + COMPANY + ARTICLES + LEGAL + crematorium_pages() + district_pages() + [CENY]
PAGES = {p["slug"]: p for p in ALL}
for h in hubs():
    PAGES[h["slug"]] = h
PAGES["voprosy"] = {"slug": "voprosy", "crumb": "Вопросы и ответы", "title": "Вопросы и ответы о похоронах в Москве | Мосритуалист",
                    "h1": "Вопросы и ответы", "desc": "Ответы на частые вопросы о похоронах, кремации, документах, пособии и ценах в Москве.",
                    "lead": "Собрали ответы со всех страниц сайта. Не нашли свой вопрос — позвоните, дежурный ответит в любое время.",
                    "facts": [], "special": "voprosy", "body": [], "faq": [], "related": []}

PARENTS = {"tovary/": "tovary", "poleznoe/": "poleznoe", "krematorii/": "krematorii", "rajony/": "kladbishcha-moskvy", "pamyatniki/": "pamyatniki"}
for s, p in PAGES.items():
    if "parent" not in p:
        for pre, par in PARENTS.items():
            if s.startswith(pre):
                p["parent"] = par
        if s in [x["slug"] for x in SERVICES + EXTRA[:1]]:
            p["parent"] = "uslugi"


class B:
    def __init__(self, mode):
        self.mode = mode

    def url(self, slug):
        anchor = ""
        if "#" in slug:
            slug, anchor = slug.split("#", 1)
            anchor = "#" + anchor
        if slug.startswith("http"):
            return slug
        if self.mode == "prod":
            return ("/" if not slug else f"/{slug}/") + anchor
        return ("index.html" if not slug else slug.replace("/", "--") + ".html") + anchor

    def asset(self, f):
        return ("/assets/" if self.mode == "prod" else "assets/") + f

    def ext(self, key):
        return SITE[key] or self.url("kontakty")

    def links(self, text):
        def rep(m):
            slug, label = m.group(1), m.group(2)
            base = slug.split("#")[0]
            if base and base not in PAGES:
                raise SystemExit(f"broken link: {slug}")
            return f'<a href="{self.url(slug)}">{label}</a>'
        return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", rep, text)


ICONS = open(ROOT / "parts/icons.svg").read()

MENU = [
    ("Услуги", [p["slug"] for p in SERVICES] + ["ritualnyj-transport"]),
    ("Товары и памятники", ["tovary/groby", "tovary/urny", "tovary/venki", "tovary/odezhda", "tovary/kresty-tablichki", "pamyatniki", "pamyatniki/nashi-raboty", "blagoustrojstvo-mogil", "uhod-za-mogiloj"]),
    ("Справочник", ["poleznoe/chto-delat-esli-umer-chelovek", "poleznoe/dokumenty-dlya-pohoron", "posobie-na-pogrebenie", "socialnye-pohorony", "kladbishcha-moskvy", "krematorii", "poleznoe"]),
    ("Компания", ["o-nas", "ceny", "ritualnyj-agent", "otzyvy", "voprosy", "kontakty"]),
]


def header(b):
    nav = [("uslugi", "Услуги"), ("ceny", "Цены"), ("posobie-na-pogrebenie", "Пособие"), ("poleznoe/chto-delat-esli-umer-chelovek", "Что делать"), ("kontakty", "Контакты")]
    navh = "".join(f'<a href="{b.url(s)}">{t}</a>' for s, t in nav)
    cols = "".join(
        f'<div class="menu-col"><h3>{t}</h3>' + "".join(f'<a href="{b.url(s)}">{H(PAGES[s]["crumb"])}<svg class="arrow"><use href="#arr"/></svg></a>' for s in sl) + "</div>"
        for t, sl in MENU)
    return f'''{ICONS}
<header class="header" id="header">
  <div class="wrap">
    <a href="{b.url('')}" class="brand" aria-label="Мосритуалист, на главную"><b>Мосритуалист</b><span>Ритуальная служба</span></a>
    <nav class="nav" aria-label="Основные разделы">{navh}</nav>
    <div class="tools">
      <button class="round eye" aria-label="Крупный шрифт" id="bigText"><svg><use href="#eye"/></svg></button>
      <a class="phone-pill" href="tel:{SITE['tel']}" aria-label="Позвонить {SITE['phone']}"><span class="status" aria-hidden="true"></span><svg><use href="#tel"/></svg><span class="txt num">{SITE['phone']}</span></a>
      <button class="round" id="menuOpen" aria-label="Открыть меню" aria-expanded="false" aria-controls="menu"><svg><use href="#burger"/></svg></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" role="dialog" aria-label="Все разделы сайта" aria-hidden="true">
  <div class="wrap">
    <div class="menu-top"><span class="brand"><b>Мосритуалист</b></span><button class="round" data-menu-close aria-label="Закрыть меню"><svg><use href="#close"/></svg></button></div>
    <div class="menu-grid">{cols}</div>
    <div class="menu-foot"><div><a href="tel:{SITE['tel']}" class="big num">{SITE['phone']}</a><p>Круглосуточно, звонок бесплатный</p></div><p>Москва и Московская область</p></div>
  </div>
</div>'''


def lead_form(b, quick=False):
    agree = f'<label class="agree"><input type="checkbox" data-agree><span>Даю <a href="{b.url("soglasie")}">согласие на обработку персональных данных</a></span></label>'
    hp = '<input class="hp" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
    if quick:
        return f'''<form class="quick" data-lead novalidate>
            <label for="qPhone" class="sr">Ваш телефон для обратного звонка</label>
            <input id="qPhone" name="phone" type="tel" inputmode="tel" placeholder="Ваш телефон" autocomplete="tel" data-phone>{hp}
            <button class="pill pill-line" type="submit">Перезвоните мне</button>
            {agree}
            <p class="form-msg" data-msg aria-live="polite">Перезвоним за 5 минут. Консультация ни к чему не обязывает.</p>
          </form>'''
    return f'''<form class="form" data-lead novalidate>
          <h3>Перезвоним за 5 минут</h3>
          <div class="fld"><input id="fName" name="name" placeholder=" " autocomplete="name"><label for="fName">Как к вам обращаться</label></div>
          <div class="fld"><input id="fPhone" name="phone" type="tel" inputmode="tel" placeholder=" " autocomplete="tel" data-phone><label for="fPhone">Телефон</label></div>
          <div class="fld sel"><select id="fTopic" name="topic"><option>Организовать похороны</option><option>Узнать цены</option><option>Кремация</option><option>Перевозка умершего</option><option>Памятник</option><option>Другой вопрос</option></select><label for="fTopic">Чем помочь</label><svg class="chev"><use href="#chev"/></svg></div>{hp}
          {agree}
          <button class="pill pill-ink" type="submit" style="width:100%">Перезвоните мне</button>
          <p class="form-msg" data-msg aria-live="polite"></p>
        </form>'''


def contact(b):
    return f'''<section class="contact" id="contact">
    <div class="wrap contact-grid">
      <span class="ghost-orb" aria-hidden="true"></span>
      <div class="contact-text">
        <h2>Мы на связи круглосуточно</h2>
        <p>Позвоните или оставьте номер. Дежурный перезвонит в течение пяти минут и, если нужно, отправит агента.</p>
        <a href="tel:{SITE['tel']}" class="bigphone num">{SITE['phone']}</a>
        <p class="sub">Звонок бесплатный, консультация ни к чему не обязывает</p>
        <div class="office">
          <div><span>{'Офис' if SITE['address'] else 'Выезд агента'}</span><b>{H(SITE['address'] or 'Москва и Московская область')}</b><small>Работаем круглосуточно, без выходных</small></div>
          <div class="office-links"><a href="{b.ext('ymaps')}" class="chip-dark" data-goal="ymaps">Яндекс Карты</a><a href="{b.ext('gis')}" class="chip-dark" data-goal="2gis">2ГИС</a></div>
        </div>
        <div class="channels">
          <a href="{b.ext('telegram')}" class="chip-dark" data-goal="tg">Telegram</a><a href="{b.ext('max')}" class="chip-dark" data-goal="max">MAX</a>
          <p>Покажем гробы, урны и венки по видеосвязи, если не хотите ехать в офис.</p>
        </div>
      </div>
      <div class="form-wrap">{lead_form(b)}</div>
    </div>
  </section>'''


def footer(b):
    def col(t, sl):
        return f'<div class="f-col"><h4>{t}</h4><ul>' + "".join(f'<li><a href="{b.url(s)}">{H(PAGES[s]["crumb"])}</a></li>' for s in sl) + "</ul></div>"
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="f-grid">
      <div class="f-col"><span class="brand"><b>Мосритуалист</b><span>Ритуальная служба</span></span><p style="margin-top:18px">Организуем похороны в Москве и области круглосуточно.</p>
        <ul style="margin-top:18px"><li><a href="tel:{SITE['tel']}" class="num" style="color:var(--on-band);font-size:20px">{SITE['phone']}</a></li><li>{SITE['email']}</li><li><a href="{b.ext('telegram')}" data-goal="tg">Telegram</a> · <a href="{b.ext('max')}" data-goal="max">MAX</a></li></ul></div>
      {col("Услуги", ["organizaciya-pohoron", "kremaciya", "zahoronenie", "perevozka-umershego", "gruz-200", "socialnye-pohorony"])}
      {col("Справочник", ["posobie-na-pogrebenie", "poleznoe/chto-delat-esli-umer-chelovek", "kladbishcha-moskvy", "krematorii", "poleznoe", "voprosy"])}
      {col("Компания", ["o-nas", "ceny", "ritualnyj-agent", "otzyvy", "kontakty", "oferta"])}
    </div>
    <div class="f-bottom">
      <p>© {datetime.date.today().year} Мосритуалист.{(' ' + H(SITE['legal']) + '.') if SITE['legal'] else ''} Частная ритуальная служба, не является государственным учреждением. Цены на сайте не являются окончательными, стоимость фиксируется в договоре.</p>
      <div style="display:flex;gap:8px 24px;flex-wrap:wrap"><a href="{b.url('politika')}">Политика конфиденциальности</a><a href="{b.url('soglasie')}">Согласие на обработку данных</a><a href="{b.url('oferta')}">Публичная оферта</a><a href="{b.url('polzovatelskoe-soglashenie')}">Пользовательское соглашение</a></div>
    </div>
  </div>
</footer>
<div class="cookie" id="cookie" hidden><p>Сайт использует Яндекс Метрику, чтобы понимать, что работает, а что нет. <a href="{b.url('politika')}">Подробнее</a></p><button class="pill pill-ink" id="cookieOk">Понятно</button></div>
<div class="fab" id="fab"><a href="tel:{SITE['tel']}" class="pill pill-ink"><svg><use href="#tel"/></svg>Позвонить круглосуточно</a></div>'''


PACKS = {
    "crem": [
        {"name": "Простой", "desc": "Необходимое для кремации без зала прощания", "price": "34 900", "items": ["Оформление документов", "Гроб и принадлежности", "Катафалк до крематория", "Кремация и урна"]},
        {"tag": "Выбирают чаще", "name": "Достойный", "desc": "Прощание в ритуальном зале и полное сопровождение", "price": "59 900", "mid": True, "items": ["Всё из «Простого»", "Зал прощания, 30 минут", "Подготовка тела и одежда", "Автобус для родственников", "Агент на весь день"]},
        {"name": "Особый", "desc": "Церемония с ведущим, цветами и поминальным обедом", "price": "99 900", "items": ["Всё из «Достойного»", "Ведущий церемонии", "Живые цветы и венки", "Поминальный обед"]}],
    "bur": [
        {"name": "Простой", "desc": "Необходимое для захоронения на кладбище", "price": "44 900", "items": ["Оформление документов", "Гроб и принадлежности", "Катафалк до кладбища", "Копка и захоронение"]},
        {"tag": "Выбирают чаще", "name": "Достойный", "desc": "Прощание или отпевание и полное сопровождение", "price": "74 900", "mid": True, "items": ["Всё из «Простого»", "Зал прощания или отпевание", "Подготовка тела и одежда", "Автобус для родственников", "Крест и табличка"]},
        {"name": "Особый", "desc": "Всё под ключ, включая благоустройство места", "price": "129 900", "items": ["Всё из «Достойного»", "Ведущий церемонии", "Живые цветы и венки", "Поминальный обед", "Временное благоустройство"]}],
}
CALC = {"base": {"crem": 34900, "bur": 44900}, "hall": {"0": 0, "30": 9000, "60": 15000}, "body": 7000, "bus": 8000, "guest": 1200, "benefit": {"msk": 25988.63, "work": 9678.63, "reg": 9678.63}}


def scripts(b):
    cfg = {"phone": SITE["phone"], "lead": SITE["lead"], "ym": SITE["ym"] or None, "packs": PACKS, "calc": CALC}
    ym = ""
    if SITE["ym"]:
        ym = f'''<script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym({SITE['ym']},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});</script>'''
    return f'<script>window.SITE={json.dumps(cfg, ensure_ascii=False)}</script>\n<script src="{b.asset("site.js")}" defer></script>{ym}'


ORG = {"@type": "LocalBusiness", "@id": SITE["domain"] + "/#org", "name": SITE["name"], "url": SITE["domain"] + "/", "telephone": SITE["tel"], "email": SITE["email"],
       "image": SITE["domain"] + "/assets/og.jpg", "priceRange": f"от {P['org']} ₽",
       "areaServed": [{"@type": "City", "name": "Москва"}, {"@type": "AdministrativeArea", "name": "Московская область"}],
       "address": {"@type": "PostalAddress", "addressLocality": "Москва", "addressCountry": "RU"},
       "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}}


def head(b, title, desc, slug, noindex=False, ld=None, artifact_index=False):
    canon = SITE["domain"] + ("/" if not slug else f"/{slug}/")
    t = "Мосритуалист" if artifact_index else title
    meta = [f"<title>{H(t)}</title>",
            '<meta name="claude:viewport-fit-sides" content="cover">' if artifact_index else '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
            f'<meta name="description" content="{H(desc)}">',
            f'<meta name="robots" content="{"noindex,follow" if noindex else "index,follow"}">',
            f'<link rel="canonical" href="{canon}">',
            '<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Мосритуалист">',
            f'<meta property="og:title" content="{H(title)}"><meta property="og:description" content="{H(desc)}"><meta property="og:url" content="{canon}">',
            f'<meta property="og:image" content="{SITE["domain"]}/assets/og.jpg">',
            '<meta name="theme-color" content="#16171a"><meta name="format-detection" content="telephone=yes">',
            f'<link rel="icon" href="{b.asset("favicon.svg")}" type="image/svg+xml">',
            f'<link rel="preload" href="{b.asset("fonts/jost-cyrillic-300-normal.woff2")}" as="font" type="font/woff2" crossorigin>',
            f'<link rel="stylesheet" href="{b.asset("site.css")}">']
    if SITE["yandex_verification"]:
        meta.append(f'<meta name="yandex-verification" content="{SITE["yandex_verification"]}">')
    graph = [ORG] + (ld or [])
    meta.append('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>")
    return "\n".join(meta)


def doc(b, headh, body, artifact_index=False):
    if artifact_index:
        return headh + "\n" + body
    return f'<!doctype html>\n<html lang="ru">\n<head>\n{headh}\n</head>\n<body>\n{body}\n</body>\n</html>\n'


def crumbs(b, p):
    chain = [("", "Главная")]
    par = p.get("parent")
    if par:
        pp = PAGES[par]
        if pp.get("parent"):
            chain.append((pp["parent"], PAGES[pp["parent"]]["crumb"]))
        chain.append((par, pp["crumb"]))
    chain.append((p["slug"], p["crumb"]))
    lis = "".join(f'<li><a href="{b.url(s)}">{H(t)}</a></li>' if i < len(chain) - 1 else f'<li aria-current="page">{H(t)}</li>' for i, (s, t) in enumerate(chain))
    ld = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "item": SITE["domain"] + ("/" if not s else f"/{s}/")} for i, (s, t) in enumerate(chain)]}
    return f'<ol class="crumbs">{lis}</ol>', ld


def blocks(b, body):
    out = []
    for blk in body:
        k = blk[0]
        v = blk[1]() if callable(blk[1]) else blk[1]
        if k == "h2":
            idattr = f' id="{blk[2]}"' if len(blk) > 2 else ""
            out.append(f"<h2{idattr}>{H(v)}</h2>")
        elif k == "p":
            out.append(f"<p>{b.links(v)}</p>")
        elif k == "note":
            out.append(f'<p class="note">{b.links(v)}</p>')
        elif k in ("ul", "ol"):
            out.append(f"<{k}>" + "".join(f"<li>{b.links(x)}</li>" for x in v) + f"</{k}>")
        elif k == "table":
            cls = "ptable total" if len(blk) > 2 else "ptable"
            rows = "".join(f'<tr><td>{b.links(a)}</td><td class="num">{b.links(c)}</td></tr>' for a, c in v)
            out.append(f'<div class="tbl"><table class="{cls}">{rows}</table></div>')
            if SITE["demo_prices"] and any("₽" in c for _, c in v) and "25 988,63" not in rows and "70 884" not in rows and "9 678,63" not in rows:
                out.append('<p class="demo">Цены указаны для примера и будут заменены на актуальные.</p>')
        elif k == "cards":
            items = []
            for t, d, s, pr in v:
                inner = f"<h3>{H(t)}</h3><p>{H(d)}</p>" + (f'<b class="num">{pr}</b>' if pr else "")
                items.append(f'<a class="cards-l" href="{b.url(s)}">{inner}</a>' if s else f"<div>{inner}</div>")
            out.append('<div class="cards">' + "".join(items) + "</div>")
    return "\n".join(out)


def faq_html(items):
    return '<div class="qs">' + "".join(f'<div class="q"><button aria-expanded="false">{H(q)}<span class="pm" aria-hidden="true"></span></button><div class="ans"><div><p>{H(a)}</p></div></div></div>' for q, a in items) + "</div>"


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def related(b, slugs):
    if not slugs:
        return ""
    cards = "".join(f'<a href="{b.url(s)}" class="g"><span class="g-k">{"Статья" if PAGES[s].get("kind") == "article" else "Раздел"}</span><h3>{H(PAGES[s]["crumb"])}</h3><p>{H(PAGES[s]["desc"].split(".")[0])}.</p></a>' for s in slugs)
    return f'<section class="related"><div class="wrap"><h2>Смотрите также</h2><div class="g-grid">{cards}</div></div></section>'


def aside(b):
    return f'''<aside class="aside"><div class="aside-card">
      <h2>Нужна помощь сейчас?</h2><p>Дежурный ответит в любое время и подскажет, что делать.</p>
      <a href="tel:{SITE['tel']}" class="ph num">{SITE['phone']}</a>
      <a href="#contact" class="pill">Перезвоните мне</a>
      <div class="aside-links"><a href="{b.url('poleznoe/chto-delat-esli-umer-chelovek')}">Что делать, если умер человек</a><a href="{b.url('ceny')}">Калькулятор стоимости</a><a href="{b.url('posobie-na-pogrebenie')}">Пособие до 25 988 ₽</a></div>
    </div></aside>'''


def page(b, p):
    cr, crld = crumbs(b, p)
    facts = "".join(f'<div><b class="num">{H(x)}</b>{H(y)}</div>' for x, y in p.get("facts", []))
    special = ""
    faq_items = list(p.get("faq", []))
    if p.get("special") == "ceny":
        special = b.links((ROOT / "parts/ceny.html").read_text())
    if p.get("special") == "voprosy":
        faq_items = []
        for q in PAGES.values():
            faq_items += q.get("faq", [])
        seen = set()
        faq_items = [x for x in faq_items if not (x[0] in seen or seen.add(x[0]))]
    prose = blocks(b, p.get("body", []))
    if faq_items:
        prose += "\n<h2>Частые вопросы</h2>\n" + faq_html(faq_items)
    ld = [crld]
    if faq_items:
        ld.append(faq_ld(faq_items))
    if p.get("price"):
        ld.append({"@type": "Service", "name": p["h1"], "provider": {"@id": SITE["domain"] + "/#org"}, "areaServed": "Москва",
                   "offers": {"@type": "Offer", "priceCurrency": "RUB", "price": p["price"].replace(" ", ""), "priceSpecification": {"@type": "PriceSpecification", "minPrice": p["price"].replace(" ", ""), "priceCurrency": "RUB"}}})
    if p.get("kind") == "article":
        ld.append({"@type": "Article", "headline": p["h1"], "dateModified": TODAY, "author": {"@id": SITE["domain"] + "/#org"}, "publisher": {"@id": SITE["domain"] + "/#org"}, "mainEntityOfPage": SITE["domain"] + f"/{p['slug']}/"})
    lead_html = b.links(H(p["lead"]))
    main = f'''<main>
  <section class="p-hero"><div class="wrap">
    {cr}
    <h1>{H(p["h1"])}</h1>
    <p class="lead">{lead_html}</p>
    <div class="p-cta"><a href="tel:{SITE['tel']}" class="pill pill-ink"><svg><use href="#tel"/></svg><span class="num">{SITE['phone']}</span></a><a href="#contact" class="pill pill-line">Перезвоните мне</a></div>
    {f'<div class="facts">{facts}</div>' if facts else ''}
  </div></section>
  {special}
  <div class="wrap p-body"><div class="prose">{prose}</div>{aside(b)}</div>
  {related(b, p.get("related", []))}
  {contact(b)}
</main>'''
    body = header(b) + "\n" + main + "\n" + footer(b) + "\n" + scripts(b)
    return doc(b, head(b, p["title"], p["desc"], p["slug"], p.get("noindex"), ld), body)


HOME_MAP = [
    ("Что делать в первые сутки", "poleznoe/chto-delat-esli-umer-chelovek"), ("Какие документы нужны", "poleznoe/dokumenty-dlya-pohoron"),
    ("Как получить пособие", "posobie-na-pogrebenie"), ("Кремация или захоронение", "poleznoe/kremaciya-ili-zahoronenie"),
    ("Как выбрать памятник", "poleznoe/kak-vybrat-pamyatnik"), ("Когда можно ставить", "poleznoe/kogda-stavit-pamyatnik"),
    ("Все статьи", "poleznoe"), ("Организация похорон", "organizaciya-pohoron"), ("Кремация", "kremaciya"), ("Захоронение", "zahoronenie"),
    ("Перевозка умершего", "perevozka-umershego"), ("Поминальный обед", "pominalnyj-obed"), ("Благоустройство могилы", "blagoustrojstvo-mogil"),
    ("Уход за захоронением", "uhod-za-mogiloj"), ("Памятники", "pamyatniki"), ("Подробнее", "ritualnyj-agent#proverit"),
    ("обработку персональных данных", "soglasie"),
] + [(d[1], f"rajony/{d[0]}") for d in DISTRICTS]
HOME_EXT = [("Яндекс Карт", "ymaps"), ("2ГИС", "gis"), ("Telegram", "telegram"), ("MAX", "max")]


def home(b):
    src = (ROOT.parent / "mosritualist/index.html").read_text()
    main = re.search(r"<main id=\"top\">.*?</main>", src, re.S).group(0)
    main = re.sub(r"\s*<!-- СВЯЗЬ -->.*?</section>", lambda m: "\n  " + contact(b), main, flags=re.S)
    main = re.sub(r'<form class="quick" id="quick" novalidate>.*?</form>', lambda m: lead_form(b, True), main, flags=re.S)
    main = main.replace('<div class="hero-art">', '''<div class="hero-art">
          <figure class="hero-photo"><img src="%s" srcset="%s 640w, %s 960w, %s 1600w" sizes="(max-width:1000px) 100vw, 50vw" width="1600" height="900" alt="Вид на Кремль и Москву-реку на закате" fetchpriority="high"></figure>''' % (b.asset("hero-960.webp"), b.asset("hero-640.webp"), b.asset("hero-960.webp"), b.asset("hero-1600.webp")), 1)
    main = main.replace("<p class=\"q\">Что делать, если умер близкий</p>", "")
    main = main.replace('<a href="#steps" class="q-link">', f'<a href="{b.url("poleznoe/chto-delat-esli-umer-chelovek")}" class="q-link">')
    main = re.sub(r'\s*<div class="msg">.*?</div>', lambda m: f'\n          <div class="msg"><span>Удобнее написать?</span><a href="{b.ext("telegram")}" data-goal="tg">Telegram</a><a href="{b.ext("max")}" data-goal="max">MAX</a></div>', main, count=1, flags=re.S)
    main = main.replace('<a href="#" class="link-more">Все услуги и цены', f'<a href="{b.url("uslugi")}" class="link-more">Все услуги и цены')
    main = main.replace('<a href="#" class="link-all">', f'<a href="{b.url("poleznoe")}" class="link-all">')

    def fix(m):
        tail = re.sub(r"<[^>]+>", "", src_tail(m))[:160]
        for key, slug in HOME_MAP:
            if key in tail:
                return f'href="{b.url(slug)}"'
        for key, ek in HOME_EXT:
            if key in tail:
                return f'href="{b.ext(ek)}"'
        return 'href="' + b.url("kontakty") + '"'
    state = {"s": main}

    def src_tail(m):
        return state["s"][m.end():m.end() + 400]
    main = re.sub(r'href="#"', fix, main)
    main = main.replace("</section>\n\n  <!-- УТВЕРЖДЕНИЕ -->", "</section>\n" + (ROOT / "parts/pricegrid.html").read_text().replace("ceny-link", b.url("ceny")) + "\n  <!-- УТВЕРЖДЕНИЕ -->", 1)
    main = main.replace("tel:+74950000000", "tel:" + SITE["tel"]).replace("+7 (495) 000-00-00", SITE["phone"])
    main = b.links(main)
    faq = re.findall(r'<div class="q"><button aria-expanded="false">(.*?)<span class="pm".*?<p>(.*?)</p>', main, re.S)
    ld = [faq_ld([(html.unescape(q), html.unescape(a)) for q, a in faq])]
    title = "Ритуальные услуги и организация похорон в Москве 24/7 | Мосритуалист"
    desc = f"Ритуальные услуги в Москве: организация похорон под ключ от {P['org']} ₽, кремация, перевозка, груз 200. Агент за 60 минут, круглосуточно. Пособие до 25 988 ₽, цена в договоре."
    help_ = f'''<div class="help" id="help" role="dialog" aria-modal="true" aria-labelledby="helpTitle" aria-hidden="true">
  <div class="help-bg" data-help-close></div>
  <div class="help-card">
    <button class="round x" data-help-close aria-label="Закрыть"><svg><use href="#close"/></svg></button>
    <h3 id="helpTitle">Получить помощь</h3>
    <a class="ph num" href="tel:{SITE['tel']}" id="helpPhone">{SITE['phone']}</a>
    <p class="hint">Круглосуточно. Дежурный подскажет, что делать прямо сейчас.</p>
    <button class="copy" id="copyBtn">Скопировать номер</button>
    <div class="alt"><a href="tel:{SITE['tel']}" class="pill pill-ink">Позвонить</a><a href="#contact" class="pill pill-line" data-help-close>Перезвоните мне</a></div>
  </div>
</div>'''
    body = header(b) + "\n" + main + "\n" + footer(b) + "\n" + help_ + "\n" + scripts(b)
    ai = b.mode == "preview"
    return doc(b, head(b, title, desc, "", False, ld, artifact_index=ai), body, artifact_index=ai)


def build(mode):
    out = ROOT / ("dist" if mode == "prod" else "preview")
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    shutil.copytree(ROOT / "assets", out / "assets", dirs_exist_ok=True)
    b = B(mode)
    files = {"": home(b)}
    for s, p in PAGES.items():
        files[s] = page(b, p)
    for s, txt in files.items():
        f = out / ("index.html" if not s else (f"{s}/index.html" if mode == "prod" else s.replace("/", "--") + ".html"))
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt)
    if mode == "prod":
        (out / "api").mkdir(exist_ok=True)
        shutil.copy(ROOT / "api/lead.php", out / "api/lead.php")
        urls = [""] + [s for s, p in PAGES.items() if not p.get("noindex") and not p.get("legal")]
        sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
            f"  <url><loc>{SITE['domain']}{'/' if not s else f'/{s}/'}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if not s else ('0.8' if s.count('/') == 0 else '0.6')}</priority></url>\n" for s in urls) + "</urlset>\n"
        (out / "sitemap.xml").write_text(sm)
        (out / "robots.txt").write_text(f"User-agent: *\nDisallow: /api/\nClean-param: ysclid&utm_source&utm_medium&utm_campaign&utm_content&utm_term&yclid&gclid\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
        (out / "404.html").write_text(page(b, {"slug": "404", "crumb": "Страница не найдена", "title": "Страница не найдена | Мосритуалист", "h1": "Страница не найдена", "desc": "Страница не найдена.", "lead": "Возможно, ссылка устарела. Позвоните нам или вернитесь на главную.", "noindex": True, "body": [], "faq": [], "related": ["uslugi", "ceny", "kontakty"]}).replace('<link rel="canonical" href="https://mosritualist.ru/404/">', ""))
    print(mode, len(files), "pages ->", out)


if __name__ == "__main__":
    for m in sys.argv[1:] or ["prod", "preview"]:
        build(m)
