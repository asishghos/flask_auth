# In routers.py
from app import app
from model.model import model
from flask import request
from flask_jwt_extended import jwt_required

@app.route('/user/login', methods=["POST"])
def login():
    return model().login_model(request.form)

@app.route('/protected', methods=["GET"])
@jwt_required()
def protected():
    return {"status": "success", "message": "Access granted to protected route"}

@app.route('/user/details')
def user_details():
    return model().get_all_users()

@app.route('/user/signup', methods=["POST"])
def user_add():
    return model().register_model(request.form)

@app.route('/user/update', methods=["POST"])
def user_update():
    return model().update_user_model(request.form)

@app.route('/user/delete', methods=["POST"])
def user_delete():
    return model().delete_user_model(request.form)