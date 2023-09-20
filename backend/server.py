#jsonify and json_util only used to visualize mongodb-data on the website for now
from flask import Flask, jsonify, make_response, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import *
import threading
import time
import os
import re
import subprocess

from database import *

def ping_container(container_name_or_id, count=4):
    try:
        # Run the ping command to ping the container
        result = subprocess.run(
            ["ping", "-c", str(count), container_name_or_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return result.returncode == 0

    except Exception as e:
        return f"Error while pinging container {container_name_or_id}: {str(e)}"
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

while ping_container(os.getenv('MYSQL_HOST')) == False:
    time.sleep(.05)
sqlDataBase = SqlDataBase(app)

dataBase: DataBase = sqlDataBase

class User(UserMixin):
    def __init__(self, id):
            self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/api/login", methods=["GET"])
def login():
    if dataBase.login(request.args.get("username",""),request.args.get("password","")):
        user = User(request.args.get("username",""))
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

@app.route("/api/profile",methods=["GET"])
@login_required
def show_profile():
    retstr:str = current_user.id + "<br>"
    for game in dataBase.get_games(current_user.id):
        retstr += str(game._id)
        for card in game.table:
            retstr += " " + CardToClearGerman.translate(card)
        retstr += "<br> My Hand: "
        for player in dataBase.get_players(game):
            if player.user_name == str(current_user.id):
                for card in player.hand:
                    retstr += " " + CardToClearGerman.translate(card)
            else:
                continue
    return retstr

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True, use_reloader=False)