import os

from app import app

from fileupload import file_upload
from auth import auth_flask_login

app.register_blueprint(file_upload)
app.register_blueprint(auth_flask_login)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000)) 
	app.run()
