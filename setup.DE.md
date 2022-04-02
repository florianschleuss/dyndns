# Setup
Auf dem Gerät:
1. dyndns.py wie in der Anleitung per CRONJOB automatisch starten lassen:
   https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
   1. chmod 755 dyndns.sh
   2. sh dyndns.sh
   3. sudo pip3 install flask flask_restful
   4. sudo crontab -e
   5. @reboot sh /home/pi/dyndns-script/dyndns.sh >/home/pi/dyndns-script/cronlog 2>&1
2. Empfehlung: Logdatei mit anlegen. Vereinfacht Debugging.
3. Nach der Erstellung reboot. 

FritzBox:
Internet > Freigaben > DynDNS
- Update-URL:       http://\<IP\>/dyndns/update_dns
- Domainname:       \<Subdomain\>.\<Domain\>
- Benutzername:     -
- Kennwort:         -

