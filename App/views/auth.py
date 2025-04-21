from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers import login

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    response = redirect(request.referrer)
    if not token:
        flash('Bad username or password given')
    else:
        flash('Login Successful')
        set_access_cookies(response, token)
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.index_page'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return jsonify({'message': f"Logged in as {current_user.username}"})