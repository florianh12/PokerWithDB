#jsonify and json_util only used to visualize mongodb-data on the website for now
from flask import Flask, jsonify, make_response, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from bson import ObjectId
from models import *
import threading
import time
import os
import re


from database import *

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.secret_key = os.urandom(24)

lock = False
login_manager = LoginManager()
login_manager.init_app(app)
sqlDataBase = SqlDataBase(app)
dataBase: DataBase = sqlDataBase

class User(UserMixin):
    id = 1

@login_manager.user_loader
def load_user(user_id):
    return User()

@app.route("/api/login", methods=["GET"])
def login():
    if dataBase.login(request.args.get("username",""),request.args.get("password","")):
        user = User()
        login_user(user)
        return 'Logged in'
    else:
        return "Login unsuccessful"

@app.route("/api/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    return 'Logged out'

@app.route("/api/populate_db", methods=["GET"])
def populate_db():
    global dataBase
    global lock
    if lock:
        return make_response(jsonify({"message": "Database is already populating"}), 201)
    lock = True
    populate_sql(sqlDataBase)
    dataBase = sqlDataBase
    lock = False
    return make_response(jsonify({"message": "Successful populated database"}), 201)




@app.route("/api/translate_test", methods=["GET"])
@login_required
def translate_test():
    retstr = str()
    cards = list(Card)
    for pos,card in enumerate(cards):
        
        retstr += CardToClearGerman.translate(card)+" "
        
        if pos%13 == 0 and pos != 0:
            retstr += "<br>"
            
    return retstr

def safe_populating():
    again = True
    while again:
        time.sleep(.1)
        try:
            populate_db()
            again = False
        except Exception as e:
            pass

if __name__ == "__main__":
    # connection Problems when starting db, hence the daemon thread, doesn't work, TODO: fix autopopulate
    populator = threading.Thread(target=safe_populating)
    populator.daemon = True
    populator.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True, use_reloader=False)