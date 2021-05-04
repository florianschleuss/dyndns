# Setup
Auf dem Gerät:
1. dyndns.py wie in der Anleitung per CRONJOB automatisch starten lassen:
   https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
2. Empfehlung: Logdatei mit anlegen. Vereinfacht Debugging.
3. Nach der Erstellung reboot. 

FritzBox:
Internet > Freigaben > DynDNS
- Update-URL:       http://\<IP\>/dyndns/update_dns
- Domainname:       \<Subdomain\>.\<Domain\>
- Benutzername:     -
- Kennwort:         -

