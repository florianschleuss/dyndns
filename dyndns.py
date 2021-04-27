import requests
import json
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request
# from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

load_dotenv()
USERNAME=os.environ.get("USERNAME")
PASSWORD=os.environ.get("PASSWORD")
DOMAIN=os.environ.get("DOMAIN")

# List of subdomains to update. '' for root domain
SUBDOMAINS = [i for i in os.environ.get("SUBDOMAINS").split(", ")]

# IP Adresses
IPv6=''
IP=''



# Will create a requests session and log you into your one.com account in that session
def _loginSession(USERNAME, PASSWORD, DOMAIN):

    print('Logging in', flush=True)

    loginurl = 'https://www.one.com/admin/login.do'

    session = requests.session()
    logindata = {'loginDomain': True,'displayUsername': USERNAME, 'password1': PASSWORD, 'username': USERNAME, 'targetDomain': '', 'loginTarget': ''}
    session.post(loginurl, data=logindata)
    if session.get('https://www.one.com/admin/api/domains/' + DOMAIN + '/dns/custom_records').status_code != 200:
        raise Exception('Login failed')

    return session


# Gets all DNS records on your domain.
def _getCustomRecords(session, DOMAIN):
    print('Getting Records', flush=True)
    return json.loads(session.get('https://www.one.com/admin/api/domains/' + DOMAIN + '/dns/custom_records').text)['result']['data']


# Finds the record id of a record from it's subdomain
def _findIdBySubdomain(records, subdomain, rc_type='A'):
    for obj in records:
        if obj['attributes']['prefix'] == subdomain and obj['attributes']['type'] == rc_type:
            print('Found', rc_type, 'domain "' + subdomain + '": ' + obj['id'], flush=True)
            return obj['id']
    print('No ID found for "' + subdomain + '"', rc_type, flush=True)
    return ''


# changes the IP Address of a TYPE A record. Default TTL=3800
def _changeIP(session, records, DOMAIN, SUBDOMAIN, IP, IPv6, TTL=3800):

    
    basednsurl='https://www.one.com/admin/api/domains/' + DOMAIN + '/dns/custom_records/'
    sendheaders={'Content-Type': 'application/json'}

    v4 = {'type':'dns_service_records','id':_findIdBySubdomain(records, SUBDOMAIN),'attributes':{'type':'A','prefix':SUBDOMAIN,'content':IP,'priority': 1, 'ttl':TTL}}
    ret = session.patch(basednsurl + v4['id'], data=json.dumps(v4), headers=sendheaders)
    if ret.status_code != 200:
        print('IPv4 update failed', flush=True)
        print(ret.text, flush=True)
    else:
        print('IPv4 change successful on subdomain "' + SUBDOMAIN + '" to new IP "' + v4['attributes']['content'] + '"', flush=True)
    
    v6 = {'type':'dns_service_records','id':_findIdBySubdomain(records, SUBDOMAIN, 'AAAA'),'attributes':{'type':'AAAA','prefix':SUBDOMAIN,'content':IPv6,'ttl':TTL}}
    ret = session.patch(basednsurl + v6['id'], data=json.dumps(v6), headers=sendheaders)
    if ret.status_code != 200:
        print('IPv6 change failed\n', flush=True)
        print(ret.text, flush=True)
    else:
        print('IPv6 change successful on subdomain "' + SUBDOMAIN + '" to new IP "' + v6['attributes']['content'] + '"\n', flush=True)
    return

def _update_dns():
    try:
        IPv6=requests.get('https://api64.ipify.org/').text
        IP=requests.get('https://api.ipify.org/').text
    except Exception:
        print('Error while IP detection', flush=True)
    # Create login session
    s = _loginSession(USERNAME, PASSWORD, DOMAIN)

    # get dns records
    records = _getCustomRecords(s, DOMAIN)

    # loop through list of subdomains
    for subdomain in SUBDOMAINS:
        _changeIP(s, records, DOMAIN, subdomain, IP, IPv6)

app = Flask(__name__)
api = Api(app)
@app.route('/dyndns/update_dns', methods=['GET'])
def update_dns():
    _update_dns()
    return 'success', 200
 
if __name__ == '__main__':
    # _update_dns()

    app.run(host='0.0.0.0', port=80, debug=True)

