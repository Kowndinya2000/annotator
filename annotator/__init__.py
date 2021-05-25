# ----------------------------------------------------------------------
# This script initialize the flask app
#
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#
#-----------------------------------------------------------------------

#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#connection with flask_sqlalchemy
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    
 #app.config['UPLOAD FOLDER']=r"D:\Academic\BTP\Annotation Tool\project\static\img"   
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

# blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
