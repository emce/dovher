import json
import locale

import ovh
from flask import Flask, render_template
from requests import get

app = Flask(__name__)
with open('config.json', 'r') as f:
    app.config.update(json.load(f))
with open('lang/' + app.config['LANGUAGE'] + '.json', 'r') as f:
    app.config.update(json.load(f))

@app.template_filter('translate')
def reverse_filter(s):
    return translate(s)

@app.route('/')
def index():
    ip = get('https://checkip.amazonaws.com').text.strip()
    hosts = []
    for host in app.config['HOSTS']:
        current_ip = get_current_record(host['domain'], host['subdomain'], host['type'])
        host['current_ip'] = current_ip
        if current_ip == ip:
            host['new_ip'] = current_ip
        else:
            host['new_ip'] = update_record(host['domain'], host['subdomain'], host['type'], ip)
        hosts.append(host)
    return render_template("base.html",
                           lang=app.config['LANGUAGE'],
                           title=translate('title'),
                           ip=ip,
                           hosts=hosts,
                           dev=app.config['DEVELOPMENT'])


def get_ovh_client():
    global app
    return ovh.Client(
        endpoint=app.config['OVH_ENDPOINT'],
        application_key=app.config['OVH_APPLICATION_KEY'],
        application_secret=app.config['OVH_APPLICATION_SECRET'],
        consumer_key=app.config['OVH_CONSUMER_KEY']
    )


def get_ip():
    return get('https://checkip.amazonaws.com').text.strip()


def get_current_record(domain, subdomain, record_type):
    client = get_ovh_client()
    path = '/domain/zone/{}/record'.format(domain)
    result = client.get(path, fieldType=record_type, subDomain=subdomain)
    if len(result) != 1:
        return None
    else:
        record_id = result[0]
        path = '/domain/zone/{}/record/{}'.format(domain, record_id)
        result = client.get(path)
        return result['target']


def update_record(domain, subdomain, record_type, new_ip, _ttl = 600):
    client = get_ovh_client()
    path = '/domain/zone/{}/record'.format(domain)
    result = client.get(path, fieldType=record_type, subDomain=subdomain)
    if len(result) != 1:
        return None
    else:
        record_id = result[0]
        path = '/domain/zone/{}/record/{}'.format(domain, record_id)
        if not app.config['DEVELOPMENT']:
            client.put(path, subDomain=subdomain, target=new_ip, ttl=_ttl)
            client.post('/domain/zone/{}/refresh'.format(domain))
        return get_current_record(domain, subdomain, record_type)

def translate(key):
    if key in app.config['TRANSLATION'].keys():
        return app.config['TRANSLATION'][key]
    else:
        return key


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)