from flask import Blueprint, redirect, request, flash
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (
        create_marker,
        delete_marker,
        update_marker
        )

marker_views = Blueprint('marker_views', __name__, template_folder='../templates')

# Add Marker to Campus
@marker_views.route('/marker/add/<int:campus_id>', methods=['POST'])
@jwt_required()
def add_marker(campus_id):
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    name = request.form.get('name')
    description = request.form.get('description')
    category = request.form.get('category')
    faculty = request.form.get('faculty')
    image = request.form.get('image')
    
    open_time = request.form.get('open_time', None)
    close_time = request.form.get('open_time', None)
    
    if create_marker(user_id=current_user.id, 
                     name=name, campus_id=campus_id, 
                     category_id=category,
                     faculty_id=faculty,
                     description=description, 
                     latitude=lat, 
                     longitude=lng, 
                     image=image,
                     open_time=open_time,
                     close_time=close_time):
        flash("Added marker")
    else:
        flash("Unable to add marker")
    
    return redirect(request.referrer)


# Update Marker
@marker_views.route('/marker/update/<int:marker_id>', methods=['POST'])
@jwt_required()
def update_maker_route(marker_id):
    if update_marker(user_id=current_user.id ,marker_id=marker_id, data=request.form) :
        flash("Updated marker")
    else:
        flash("Unable to update marker")
    
    return redirect(request.referrer)
    

# Delete Marker
@marker_views.route('/marker/delete/<int:marker_id>', methods=['POST'])
@jwt_required()
def delete_marker_route(marker_id):
    if delete_marker(marker_id) :
        flash("Deleted marker")
    else:
        flash("Unable to delete marker")
    
    return redirect(request.referrer)