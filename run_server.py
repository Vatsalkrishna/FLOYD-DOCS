import os

from app import app                                #import the main flask app
 
from fileupload import file_upload                   #get your blueprints
from auth import auth_flask_login

app.register_blueprint(file_upload)                #register your blueprint
app.register_blueprint(auth_flask_login)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000)) 
	app.run()
