from flask import Flask
from flask_restful import Resource, Api
from germandictservice import query_pons_dictionary, extract_definitions, secret

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


class Definitions(Resource):
    def get(self, query):
        response = query_pons_dictionary(query=query, secret=secret)
        result = {}
        result['definitions'] = list(extract_definitions(response))
        return result

api.add_resource(Definitions, '/defs/<string:query>')


if __name__ == '__main__':
    app.run(debug=True)