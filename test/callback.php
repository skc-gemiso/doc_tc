<?php
/**
 * 변환 결과 Callback 수신 테스트 엔드포인트
 * 수신 내용을 JSON 파일로 저장
 */
define('LOG_DIR', __DIR__ . '/callback_logs');
@mkdir(LOG_DIR, 0755, true);

$body = file_get_contents('php://input');
$data = json_decode($body, true);

$logFile = LOG_DIR . '/' . date('Ymd_His') . '_task' . ($data['data']['taskId'] ?? 'unknown') . '.json';
file_put_contents($logFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

http_response_code(200);
header('Content-Type: application/json');
echo json_encode(['result' => true, 'message' => 'received']);
