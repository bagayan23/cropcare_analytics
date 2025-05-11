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

    // Check if pH data is available
    if (isset($data['ph_level']['value'])) {
        echo $data['ph_level']['value']; // Output the pH value
        exit;
    }
}

// Fallback to local file-based logic
$dataFile = 'ph.txt';
$timestampFile = 'ph_time.txt';

$phValue = @file_get_contents($dataFile) ?: '-';
$lastTime = @file_get_contents($timestampFile);

if ($lastTime === false || time() - intval($lastTime) > 5) {
    echo "-"; // Consider system OFF
} else {
    echo $phValue;
}
?>