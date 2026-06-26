<?php
/**
 * Cal.com v2 API Proxy
 * --------------------
 * Keeps your API key server-side so it never reaches the browser.
 * Place this file on your Krystal/cPanel server (e.g. in your site root or a subdirectory).
 *
 * Usage from front-end JS:
 *   GET  /cal-proxy.php?action=slots&eventTypeId=5614269&startTime=...&endTime=...
 *   POST /cal-proxy.php?action=book  (with JSON body)
 */

// =============================================
// YOUR CAL.COM API KEY (keep this file private)
// =============================================
$API_KEY = 'cal_live_f85a2c899fc87b39963913d47d38aab4';

// Cal.com v2 base URL
$BASE_URL = 'https://api.cal.com/v2';
$API_VERSION = '2024-08-13';

// CORS: allow your own domain only (update to your actual domain)
$allowed_origins = [
    'https://cornerstonedg.com',
    'https://www.cornerstonedg.com',
    'http://localhost',
    'http://127.0.0.1'
];

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
}
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$action = $_GET['action'] ?? '';

// --------------------------------------------------
// ACTION: slots - fetch available time slots
// --------------------------------------------------
if ($action === 'slots' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    $eventTypeId = $_GET['eventTypeId'] ?? '';
    $startTime   = $_GET['startTime'] ?? '';
    $endTime     = $_GET['endTime'] ?? '';

    if (!$eventTypeId || !$startTime || !$endTime) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing required parameters: eventTypeId, startTime, endTime']);
        exit;
    }

    $url = "$BASE_URL/slots/available?" . http_build_query([
        'eventTypeId' => $eventTypeId,
        'startTime'   => $startTime,
        'endTime'     => $endTime
    ]);

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            "Authorization: Bearer $API_KEY",
            "cal-api-version: $API_VERSION",
            "Content-Type: application/json"
        ],
        CURLOPT_TIMEOUT => 15
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error    = curl_error($ch);
    curl_close($ch);

    if ($error) {
        http_response_code(502);
        echo json_encode(['error' => 'Failed to reach Cal.com API', 'detail' => $error]);
        exit;
    }

    http_response_code($httpCode);
    echo $response;
    exit;
}

// --------------------------------------------------
// ACTION: book - create a booking
// --------------------------------------------------
if ($action === 'book' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);

    if (!$input) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON body']);
        exit;
    }

    // Build the v2 booking payload
    $payload = [
        'eventTypeId' => (int)($input['eventTypeId'] ?? 5614269),
        'start'       => $input['start'] ?? '',
        'attendee'    => [
            'name'     => $input['name'] ?? '',
            'email'    => $input['email'] ?? '',
            'timeZone' => $input['timeZone'] ?? 'Europe/London',
            'language' => 'en'
        ],
        'metadata' => $input['metadata'] ?? new \stdClass()
    ];

    if (!empty($input['bookingFieldsResponses'])) {
        $payload['bookingFieldsResponses'] = $input['bookingFieldsResponses'];
    }

    // Optional: pass location if provided
    if (!empty($input['location'])) {
        $payload['location'] = $input['location'];
    }

    $ch = curl_init("$BASE_URL/bookings");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($payload),
        CURLOPT_HTTPHEADER     => [
            "Authorization: Bearer $API_KEY",
            "cal-api-version: $API_VERSION",
            "Content-Type: application/json"
        ],
        CURLOPT_TIMEOUT => 15
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error    = curl_error($ch);
    curl_close($ch);

    if ($error) {
        http_response_code(502);
        echo json_encode(['error' => 'Failed to reach Cal.com API', 'detail' => $error]);
        exit;
    }

    http_response_code($httpCode);
    echo $response;
    exit;
}

// --------------------------------------------------
// Unknown action
// --------------------------------------------------
http_response_code(400);
echo json_encode(['error' => 'Unknown action. Use ?action=slots or ?action=book']);
