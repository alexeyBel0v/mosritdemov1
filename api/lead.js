export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  const d = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
  if (d.hp) return res.status(200).json({ ok: true });
  const digits = String(d.phone || '').replace(/\D/g, '');
  const token = process.env.TG_BOT_TOKEN, chat = process.env.TG_CHAT_ID;
  if (digits.length !== 11 || !token || !chat) return res.status(400).json({ ok: false });
  const clip = s => String(s || '').replace(/<[^>]*>/g, '').trim().slice(0, 200);
  const text = `Заявка с сайта\nТелефон: +${digits}\nИмя: ${clip(d.name)}\nТема: ${clip(d.topic)}\nСтраница: ${clip(d.page)}`;
  const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ chat_id: chat, text })
  });
  res.status(r.ok ? 200 : 502).json({ ok: r.ok });
}
