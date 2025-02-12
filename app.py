# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
import datetime

app = Flask(__name__)

#jwt
app.config['JWT_SECRET_KEY'] = 'a3f8b1c2d3e4f5g67890abcdef1234567890abcdef1234567890abcdef1234'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return 'Hello<>World'

import controller.routers as routers



# All URL is:
# http://127.0.0.1:5000/user/signup for new users
# http://127.0.0.1:5000/user/user/login for login
# http://127.0.0.1:5000/protected

# http://127.0.0.1:5000/user/user/update for update user details
# http://127.0.0.1:5000/user/user/delete for delete user details
# http://127.0.0.1:5000/user/user/details for get user details