"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")  # Create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return response_body, 200


@app.route('/members/<int:member_id>', methods=['GET'])
def member(member_id):
    response_body = {}
    if request.method == 'GET':
        response_body['message'] = 'Datos del integrante de la familia'
        response_body['results'] = jackson_family.get_member(member_id)
        print(response_body)
        if response_body['results']:
            return response_body, 200
        response_body['message'] = 'Error en la petición, id fuera de rango'
        return response_body, 400


@app.route('/students', methods=['POST', 'GET'])
def students():
    response_body = {}
    if request.method == 'POST':
        data = request.json
        name = data.get('name', 'Desconosido')
        age = data.get('age', 0)
        numbers = data.get('lucky_number', [0])
        new_data = {'name': name,
                    'age': age,
                    'lucky_numbers': numbers}
        response_body['results'] = new_data
        return response_body


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
