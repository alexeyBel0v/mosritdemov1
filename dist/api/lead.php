<?php
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit('{"ok":false}'); }
$cfg = @include __DIR__ . '/../../lead-config.php';
$token = getenv('TG_BOT_TOKEN') ?: ($cfg['token'] ?? '');
$chat = getenv('TG_CHAT_ID') ?: ($cfg['chat'] ?? '');
$d = json_decode(file_get_contents('php://input'), true) ?: [];
if (!empty($d['hp'])) exit('{"ok":true}');
$digits = preg_replace('/\D/', '', $d['phone'] ?? '');
if (strlen($digits) !== 11 || !$token || !$chat) { http_response_code(400); exit('{"ok":false}'); }
$clip = fn($s) => mb_substr(trim(strip_tags((string)$s)), 0, 200);
$text = "Заявка с сайта\nТелефон: +$digits\nИмя: " . $clip($d['name'] ?? '') . "\nТема: " . $clip($d['topic'] ?? '') . "\nСтраница: " . $clip($d['page'] ?? '');
$ch = curl_init("https://api.telegram.org/bot$token/sendMessage");
curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10, CURLOPT_POSTFIELDS => ['chat_id' => $chat, 'text' => $text]]);
curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);
http_response_code($code === 200 ? 200 : 502);
echo json_encode(['ok' => $code === 200]);
