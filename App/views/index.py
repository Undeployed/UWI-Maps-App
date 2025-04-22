import os
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (
        initialize,
        get_all_campuses,
        get_campus,
        get_all_categories,
        get_all_markers_for_campus_json,
        get_all_markers_filtered_json,
        get_all_faculties
        )

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return redirect(url_for('index_views.index_page'))

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


# Home Page
@index_views.route('/', methods=['GET'])
@index_views.route('/<int:campus_id>', methods=['GET'])
def index_page(campus_id=1):
    category_filters = request.args.getlist('category')
    faculty_filters = request.args.getlist('faculty')
    search_query = request.args.get('query', '').strip().lower()
    
    # Filter by Categories
    if category_filters:
        markers = get_all_markers_filtered_json(campus_id, category_filters)
    else:
        markers = get_all_markers_for_campus_json(campus_id)

    # Filter by Faculty
    if faculty_filters:
        markers = [
            marker for marker in markers
            if marker['faculty'] and str(marker['faculty']['id']) in faculty_filters
        ]

    # Filter by Search Query    
    if search_query:
        markers = [
            marker for marker in markers
            if search_query in marker['name'].lower() or search_query in marker['description'].lower()
        ]
        
    return render_template('index.html',
                           user=current_user,
                           campuses=get_all_campuses(), 
                           selected_campus=get_campus(campus_id),
                           categories=get_all_categories(),
                           faculties=get_all_faculties(),
                           markers=markers,
                           search_query=search_query)
