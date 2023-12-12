import json

import flask
import requests
from lxml.html.soupparser import fromstring
from lxml.etree import tostring

source_tmpl = "<p>Source: <a href='{url}'>{url}</a></p>"
config_file = "services.json"

config = {
    'hjp.znanje.hr-definicija': {
        'url': 'https://hjp.znanje.hr/index.php?show=search',
        'xpath': '//*[@id="definicija"]/div',
        'method': 'POST',
        'params': lambda word: {'word': word}
    },
    'hjp.znanje.hr': {
        'url': 'https://hjp.znanje.hr/index.php?show=search',
        'xpath': '/html/body/div[7]/div[1]/div/p[2]',
        'method': 'POST',
        'params': lambda word: {'word': word}
    }
}


def read_config():
    with open(config_file) as inp_file:
        config = json.load(inp_file)
        for service in config:
            if 'params' in config[service]:
                names = config[service]['params']
                config[service]['params'] = lambda params: {name: params[i] for i, name in enumerate(names)}
                config[service]['n_params'] = len(names)

    return config


app = flask.Flask(__name__)


@app.route('/reload')
def reload():
    global config
    config = read_config()


@app.route('/<service>/<path:params>')
def linker(service, params):
    read_config()
    if service not in config:
        return ''

    method = config[service].get('method', 'GET')
    params = params.split('/')
    if len(params) < config[service].get('n_params', 0):
        return ''
    kwargs = {('params' if method == 'GET' else 'data'): config[service]['params'](params)}

    r = requests.request(config[service].get('method', 'GET'), config[service]['url'], verify=False, **kwargs)
    if r.status_code != 200:
        return ''

    if 'xpath' in config[service]:
        page_tree = fromstring(r.text)
        elem = page_tree.xpath(config[service]['xpath'])

        if not elem:
            return ''

        return tostring(elem[0], encoding='utf-8').decode('utf-8') + source_tmpl.format(url=config[service]['url'])
    else:
        return r.text


if __name__ == "__main__":
    config = read_config()
    app.run(debug=False)
