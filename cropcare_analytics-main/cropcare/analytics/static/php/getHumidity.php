<?php
header("Cache-Control: no-cache, must-revalidate");
header("Expires: 0");
header('Content-Type: text/plain');

// URL of the Django endpoint
$djangoUrl = 'http://127.0.0.1:8000/get-sensor-data/';

// Attempt to fetch data from the Django endpoint
$response = @file_get_contents($djangoUrl);

if ($response !== false) {
    // Decode the JSON response
    $data = json_decode($response, true);

    // Check if humidity data is available
    if (isset($data['humidity']['value'])) {
        echo $data['humidity']['value']; // Output the humidity value
        exit;
    }
}

// Fallback to local file-based logic
$dataFile = 'humidity.txt';
$timestampFile = 'humidity_time.txt';

$humidityValue = @file_get_contents($dataFile) ?: '-';
$lastTime = @file_get_contents($timestampFile);

if ($lastTime === false || time() - intval($lastTime) > 5) {
    echo "-"; // Consider system OFF
} else {
    echo $humidityValue;
}
?>