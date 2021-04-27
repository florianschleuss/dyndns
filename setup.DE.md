# Setup
Auf dem Gerät:
dyndns.py wie in der Anleitung per CRONJOB automatisch starten lassen:
https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
Empfehlung: Logdatei mit anlegen. Vereinfacht Debugging.
Nach der Erstellung reboot. 

FritzBox:
Internet > Freigaben > DynDNS
- Update-URL:       http://<IP>/dyndns/update_dns
- Domainname:       <Subdomain>.<Domain>
- Benutzername:     -
- Kennwort:         -

