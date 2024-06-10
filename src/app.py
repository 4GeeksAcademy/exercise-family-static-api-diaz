import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS
@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members', methods=['POST']) 
def add_member():
    new_member = request.json
    jackson_family.add_member(new_member)
    return jsonify({"creando": "endpoint"})

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    try:
        print(f"Attempting to delete member with ID: {member_id}")
        delete_family = jackson_family.delete_member(member_id)
        if not delete_family:
            print(f"Member with ID: {member_id} not found.")
            return jsonify({"msg": "familiar no encontrado"}), 404
        print(f"Member with ID: {member_id} successfully deleted.")
        return jsonify({"done": "user eliminado"}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"msg": "Internal server error"}), 500

@app.route('/members/<int:member_id>', methods=['GET'])
def get_family_member(member_id):
    try:
        print(f"Attempting to get member with ID: {member_id}")
        member = jackson_family.get_member(member_id)
        if member is None:
            print(f"Member with ID: {member_id} not found.")
            return jsonify({"msg": "familiar no encontrado"}), 404
        print(f"Member with ID: {member_id} found: {member}")
        return jsonify(member), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"msg": "Internal server error"}), 500

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    try:
        updated_member = request.json
        print(f"Attempting to update member with ID: {member_id}")
        update_successful = jackson_family.update_member(member_id, updated_member)
        if not update_successful:
            print(f"Member with ID: {member_id} not found.")
            return jsonify({"msg": "familiar no encontrado"}), 404
        print(f"Member with ID: {member_id} successfully updated.")
        return jsonify({"done": "user actualizado"}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"msg": "Internal server error"}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
