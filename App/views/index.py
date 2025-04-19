from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import (create_user,
                             initialize,
                             get_all_campuses,
                             get_campus,
                             get_all_categories,
                             get_all_markers_for_campus_json,
                             get_all_markers_filtered_json)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
@index_views.route('/<campus_id>', methods=['GET'])
def index_page(campus_id=1):
    category_filters = request.args.getlist('category')
    markers = get_all_markers_filtered_json(campus_id, category_filters) if len(category_filters) > 0 else get_all_markers_for_campus_json(campus_id)
    return render_template('index.html', 
                           campuses=get_all_campuses(), 
                           selected_campus=get_campus(campus_id),
                           categories=get_all_categories(),
                           markers=markers)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})