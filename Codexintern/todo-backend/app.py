from flask import Flask, render_template
from config import Config
from models import db
from routes import routes
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(routes)

jwt = JWTManager(app)

with app.app_context():
    os.makedirs("instance", exist_ok=True)
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
