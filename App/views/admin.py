from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash, request, jsonify
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_admin import Admin
from App.models import db, User

class AdminView(ModelView):

    @jwt_required()
    def is_accessible(self):
        return current_user is not None

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))
    
    # Add debug route
    @app.route('/debug-db')
    def debug_db():
        try:
            # Get basic database info
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
            tables = []
            
            # Only try to get tables if database is connected
            if db.engine:
                tables = db.engine.table_names()
                
                # Test simple query if you have a User model
                user_count = User.query.count() if 'user' in tables else 0
            else:
                user_count = 0
            
            return jsonify({
                'status': 'success',
                'database_uri': db_uri,
                'database_driver': str(db.engine.driver) if db.engine else None,
                'tables': tables,
                'user_count': user_count,
                'is_postgresql': 'postgresql' in db_uri.lower() if db_uri else False
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e),
                'database_uri': app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
            }), 500