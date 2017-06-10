import requests
from bs4 import BeautifulSoup
from . import cfg

secret = cfg.secret

def query_pons_dictionary(query, secret=secret):
    """Makes a requst to Pons using their online API. Returns a response dictionary."""
    url = "https://api.pons.com/v1/dictionary"
    header = {
        'X-Secret': '230a9175235c293af92041202396161ba2cec6bd055a98f10c3af4ce95f7fb2d',
    }

    msg = {
        'l': 'dedx',
        'q': query,
        'in': 'de',
        'language': 'de',
    }
    r = requests.get(url, headers=header, params=msg)  # , verify=False)
    return r.json()


def extract_definitions(pons_response_dict):
    """yields dictionary entries a pons dictionary response."""
    for word_class in pons_response_dict[0]['hits']:
        for ddd in word_class['roms']:
            for dd in ddd['arabs']:
                def_html = dd['translations'][0]['source']
                soup = BeautifulSoup(def_html, 'html5lib')
                span = soup.span
                if 'definition' in span['class']:
                    definition = {
                        'wordclass': ddd['wordclass'],
                        'definition': soup.span.text
                    }
                    yield definition


