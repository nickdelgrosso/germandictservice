from flask import Flask
from flask_restful import Resource, Api
from germandictservice import query_pons_dictionary, extract_definitions, secret
import re
from os import path

app = Flask(__name__)
api = Api(app)


with open('wiki_grunwortschatz.txt') as f:
    common_words = {line.strip().lower(): None for line in f.readlines()}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


class Definitions(Resource):
    def get(self, query):
        response = query_pons_dictionary(query=query, secret=secret)
        result = {}
        result['definition'] = list(extract_definitions(response.json()))[0]['definition']
        result['definition_url'] = 'http://de.pons.com/%C3%BCbersetzung?' + response.url.split('?')[1]
        return result

api.add_resource(Definitions, '/defs/<string:query>')


class AnalyzeText(Resource):
    def get(self, text):
        words = re.sub("[^\w]", " ", text).split()
        words = map(str.lower, words)
        words_not_found = []
        for word in words:
            try:
                common_words[word]
            except KeyError:
                result = {
                    'word': word,
                    'suggestions': [],
                    'problem': 'NotFoundInCommonList',
                    'definition': 'definition string',
                    'definition_url': "http://de.pons.com/%C3%BCbersetzung?l=dedx&q=kind&in=de&language=de",
                }
                words_not_found.append(result)


        return words_not_found

api.add_resource(AnalyzeText, '/analyze/<string:text>')



if __name__ == '__main__':
    app.run(debug=True)