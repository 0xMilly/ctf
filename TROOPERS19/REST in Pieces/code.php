<?php
 
/**
 * rest.php
 *
 * Remote Execution Service Tomato™
 *
 * @category   REST
 * @package    Fishbowl 0day DB
 * @author     @hnzlmnn <hnzlmnn@fishbowl.tech>
 * @endpoint   /api/vegan/rest
 * @license    MIT
 * @version    1.0
 */
 
require_once("../../libs/tomato.php");
 
$secret = getenv('secret');
$command = array(
    'algo' => "sha256",
    'nonce' => $_POST['nonce'],
    'hash' => $_POST['hash'],
    'action' => base64_decode($_POST['action'])
);
 
if (empty($command['action'])) {
    error(400);
}
 
if (!in_array($command['algo'], hash_hmac_algos()) || empty($command['hash'])) {
    error(400);
}
 
if (!empty($command['nonce'])) {
    $secret = hash_hmac($command['algo'], $command['nonce'], $secret);
}
 
if (hash_hmac($command['algo'], $command['action'], $secret) !== $command['hash']) {
    error(401);
    exit;
}
 
passthru($command['action']);
