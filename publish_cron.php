<?php
/**
 * Cornerstone Digital — Scheduled Blog Publication Cron Endpoint
 *
 * Can be run via:
 *   1) cPanel Crontab (Recommended):
 *      0 9 * * 1 /usr/local/bin/php /home/corners6/public_html/publish_cron.php >> /home/corners6/publish_cron.log 2>&1
 *
 *   2) Secure HTTP Webhook:
 *      GET https://cornerstonedg.com/publish_cron.php?token=csd_publish_2026_weekly
 */

// Define secure token for web trigger
define('CRON_TOKEN', 'csd_publish_2026_weekly');

$is_cli = (php_sapi_name() === 'cli' || defined('STDIN'));

if (!$is_cli) {
    header('Content-Type: application/json; charset=utf-8');
    $token = isset($_GET['token']) ? $_GET['token'] : '';
    if ($token !== CRON_TOKEN) {
        http_response_code(403);
        echo json_encode(['status' => 'error', 'message' => 'Unauthorized']);
        exit;
    }
}

$dir = __DIR__;
$script = $dir . '/publish_scheduled_posts.py';

if (!file_exists($script)) {
    $err = "Publisher script not found at {$script}";
    if ($is_cli) {
        echo "[Error] {$err}\n";
    } else {
        http_response_code(500);
        echo json_encode(['status' => 'error', 'message' => $err]);
    }
    exit(1);
}

// Find Python binary
$python_bins = ['python3', '/usr/bin/python3', '/usr/local/bin/python3', 'python'];
$python_cmd = 'python3';
foreach ($python_bins as $bin) {
    exec("which {$bin} 2>/dev/null", $test_out, $ret);
    if ($ret === 0 && !empty($test_out[0])) {
        $python_cmd = $test_out[0];
        break;
    }
}

$cmd = escapeshellcmd("{$python_cmd} {$script}") . " 2>&1";
exec($cmd, $output_lines, $exit_code);

$output_str = implode("\n", $output_lines);

if ($is_cli) {
    echo "=== Cornerstone Publisher Cron Run: " . date('c') . " ===\n";
    echo $output_str . "\n";
    echo "Exit code: {$exit_code}\n";
    exit($exit_code);
} else {
    echo json_encode([
        'status' => ($exit_code === 0 ? 'success' : 'failed'),
        'timestamp' => date('c'),
        'exit_code' => $exit_code,
        'output' => $output_lines
    ], JSON_PRETTY_PRINT);
}
