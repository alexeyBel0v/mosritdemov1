Мосритуалист — сайт
===================

Как устроено
- content_a.py, content_b.py, content_c.py — тексты, цены (словарь P) и контакты (SITE).
- build.py — собирает сайт: python3 build.py prod
- Готовый сайт — папка dist/. Её целиком заливаем на хостинг.

Перед запуском поменять в content_a.py → SITE:
- phone / tel — реальный телефон
- address, legal, email — адрес и реквизиты
- telegram, max, ymaps, gis — ссылки на мессенджеры и карточки на картах
- ym — номер счётчика Яндекс Метрики (появится плашка про Метрику и цели)
- yandex_verification — код подтверждения из Яндекс Вебмастера
- demo_prices — False, когда цены в словаре P станут реальными
После правок: python3 build.py prod

Заявки в Telegram
- Vercel: функция api/lead.js, токен и chat_id — в Settings → Environment Variables (TG_BOT_TOKEN, TG_CHAT_ID).
- Хостинг с PHP (Beget, Timeweb и т.п.): скопировать php/lead.php в dist/api/lead.php и поставить в SITE lead = "/api/lead.php".
- Рядом с папкой сайта (на уровень выше public_html) положить lead-config.php
  по образцу lead-config.example.php: токен бота и chat_id.
- Токен НЕ хранить в файлах внутри сайта.

Страницы с noindex (не попадут в поиск, пока нет реального контента):
- /otzyvy/ — нужны реальные отзывы с Яндекс Карт и 2ГИС
- /pamyatniki/nashi-raboty/ — нужны фото работ
