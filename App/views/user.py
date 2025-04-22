from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    # Map functions
    get_all_campuses,
    get_campus,
    get_all_categories,
    get_all_faculties,
    get_all_markers_for_campus_json,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users, user=current_user)


@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    if create_user(data['username'], data['password'], data['role']):
        flash(f"User '{data['username']}' created!")
    else:
        flash(f"Failed to create user!")
        
    return redirect(url_for('user_views.get_user_page'))


# User(Admin) edit page
@user_views.route('/admin/edit', methods=['GET'])
@user_views.route('/admin/edit/<int:campus_id>', methods=['GET'])
@jwt_required()
def edit_page(campus_id=1):
    return render_template('edit.html',
                           user=current_user,
                           editing=True,
                           categories=get_all_categories(),
                           faculties=get_all_faculties(),
                           markers=get_all_markers_for_campus_json(campus_id),
                           campuses=get_all_campuses(),
                           selected_campus=get_campus(campus_id))