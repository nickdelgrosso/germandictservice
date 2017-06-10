import requests
from bs4 import BeautifulSoup


def query_pons_dictionary(query, secret):
    """Makes a requst to Pons using their online API. Returns a response.
    Builds it following Pons' reccomendations: http://en.pons.com/assets/docs/api_dict.pdf"""
    url = "https://api.pons.com/v1/dictionary"
    header = {'X-Secret': secret}
    msg = {'l': 'dedx', 'q': query, 'in': 'de','language': 'de'}
    response = requests.get(url, headers=header, params=msg)  # , verify=False)
    return response


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


