import gunicorn
from flask import Flask, request, jsonify, redirect, url_for
import bcrypt
from oauthlib.common import generate_token
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = str(os.getenv('MONGO_URI'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))


client = MongoClient(MONGO_URI)
db = client['mydatabase']
collection = db["mycollection"]

def generate_custom_user_id():
    last_custom_user_id = db.users.find_one(sort=[('_id', -1)])
    if last_custom_user_id:
        last_id = int(last_custom_user_id['_id'].split('-')[1])
    else:
        last_id = 0
    new_id = f'USER-{str(last_id + 1).zfill(4)}'  # e.g., "USER-0001"
    return new_id

def generate_template_id():
    last_template = db.templates.find_one(sort=[('template_id', -1)])
    if last_template:
        last_id = int(last_template['template_id'])
    else:
        last_id = 0
    new_id = last_id + 1
    return new_id

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        # print(data)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        # Check if the email is already registered
        existing_user = db.users.find_one({'email': email})

        if existing_user:
            # If the user already exists, redirect to the login page
            return redirect(url_for('login'))

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        custom_user_id = generate_custom_user_id()
        # Create a new user document
        user_data = {
            '_id': custom_user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': hashed_password.decode('utf-8'),  # Store the hashed password as a string
        }

        # Insert the user document into the database
        db.users.insert_one(user_data)
        return jsonify({'message': 'User registered and logged in successfully'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred'}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        # print(data)
        email = data.get('email')
        password = data.get('password')

        # Find the user with the provided email
        user = db.users.find_one({'email': email})

        if not user:
            return jsonify({'message': 'User not found!'}), 401

        # Check the password using bcrypt.checkpw
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token=generate_token()
            return jsonify({'message': 'Login successful'}), 200
            # return redirect('/template'+token), 200
            return redirect(url_for('insert_template',token=token)), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred'}), 500

@app.route('/template', methods=['POST', 'GET'])
def insert_template():
    if request.method == 'POST':
        try:
            data = request.get_json()
            template_name = data.get('template_name')
            subject = data.get('subject')
            body = data.get('body')

            custom_user_id = generate_template_id()

            template_data = {
                'template_id': custom_user_id,
                'template_name': template_name,
                'subject': subject,
                'body': body,
                # 'user_email': user_email  # Associate the template with the user who created it
            }

            # Insert the template document into the database
            # db.templates.insert_one(template_data)
            db.templates.insert_one(template_data)

            return jsonify({'message': 'Template inserted successfully'}), 201
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'An error occurred'}), 500

    elif request.method == 'GET':
        try:
            templates = list(db.templates.find({}, {"_id": 0}))

            return jsonify({'templates': templates}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'An error occurred'}), 500


@app.route('/template/<int:template_id>', methods=['GET', 'PUT', 'DELETE'])
def single_template(template_id):
    if request.method == 'GET':
        try:
            # Convert the template_id string to ObjectId
            templates = list(db.templates.find({"template_id": template_id}, {"_id": 0}))

            # template = db.templates.find_one({'_id': template_id_object})

            return jsonify({'templates': templates}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'An error occurred'}), 500
    elif request.method == 'PUT':
        try:
            if not db.templates.find_one({"template_id": template_id}, {"_id": 0}):
                return jsonify({'message': 'Template not found'}), 404

            # Get the updated data from the request body
            data = request.get_json()
            updated_template_name = data.get('template_name')
            updated_subject = data.get('subject')
            updated_body = data.get('body')

            # Update the template in the database
            db.templates.update_one(
                {"template_id": template_id},
                {
                    '$set': {
                        'template_name': updated_template_name,
                        'subject': updated_subject,
                        'body': updated_body
                    }
                }
            )

            return jsonify({'message': 'Template updated successfully'}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'An error occurred'}), 500

    elif request.method == 'DELETE':
        try:
            # Delete the template from the database
            db.templates.delete_one({"template_id": template_id})

            return jsonify({'message': 'Template deleted successfully'}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'message': 'An error occurred'}), 500
if __name__ == '__main__':
    app.run(debug=True)

