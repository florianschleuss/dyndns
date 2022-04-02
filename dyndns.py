import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

from flask import Flask, jsonify, request
from flask_restful import Api

load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")
ZONE_ID = os.environ.get("ZONE_ID")

# List of subdomains to update. '' for root domain
SUBDOMAINS = [i for i in os.environ.get("SUBDOMAINS").split(", ")]

# IP Adresses
IPv6=''
IP=''


# Gets all DNS records on your domain.
def _getCustomRecords():
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(ZONE_ID),
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
        })
    return resp.json()['result']


# changes the IP Address of a TYPE A record. Default TTL=3800
def _changeIP(records, SUBDOMAIN, IP, IPv6):
    for rec in records:
        if SUBDOMAIN not in rec['name']:
            continue
        type = rec['type']

        if type == 'AAAA':
            IP = IPv6

        resp = requests.put(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
                ZONE_ID, rec['id']),
            json={
                'type': type,
                'name': rec['name'],
                'content': IP,
                'proxied': False
            },
            headers={
                'Authorization': f'Bearer {API_TOKEN}',
            })
        if resp.status_code != 200:
            print(f'{type} update failed', flush=True)
            print(resp.text, flush=True)
        else:
            print(
                f'{type} change successful on subdomain "' + SUBDOMAIN +
                '" to new IP "' + IP + '"', flush=True)
    return


def _update_dns():
    # List of subdomains to update. '' for root domain
    SUBDOMAINS = [i for i in os.environ.get("SUBDOMAINS").split(", ")]
    try:
        IPv6 = requests.get('https://api64.ipify.org/').text
        IP = requests.get('https://api.ipify.org/').text
    except Exception:
        print('Error while IP detection', flush=True)
        return

    # get dns records
    records = _getCustomRecords()

    # loop through list of subdomains
    for subdomain in SUBDOMAINS:
        _changeIP(records, subdomain, IP, IPv6)


app = Flask(__name__)
api = Api(app)
@app.route('/update_dns', methods=['GET'])
def update_dns():
    _update_dns()
    return 'success', 200

if __name__ == '__main__':
    # _update_dns()

    print(datetime.now())
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

