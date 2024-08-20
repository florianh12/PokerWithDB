#jsonify and json_util only used to visualize mongodb-data on the website for now
from flask import Flask, jsonify, make_response, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import *
import threading
import time
import os
import re
import subprocess

from database import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.urandom(24)

lock = False
login_manager = LoginManager()
login_manager.init_app(app)
    

dataBase = SqlDataBase(app)

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
    populate_sql(dataBase)
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




@app.route("/api/new_game",methods=["GET"])
@login_required
def new_game():
    dataBase.create_game(players=[str(current_user.id)], name=request.args.get('name',''))
    return "PokerGame successfully created"

@app.route("/api/join_game",methods=["GET"])
@login_required
def join_game():
    dataBase.join_game(player=str(current_user.id), id=request.args.get('gameID'),name=request.args.get('name'))
    return "Joined successfully"

@app.route("/api/games/<int:gameID>/start",methods=["GET"])
@login_required
def start_game(gameID):
    dataBase.start_game(player=str(current_user.id), id=gameID)
    return "The game started successfully"

@app.route("/api/games/<int:gameID>/<action>",methods=["GET"])
@login_required
def act_game(gameID,action):
    #TODO: Fix the fact that nothing changes after executing the function
    #convert to enum
    action = State(action.upper())
    game = dataBase.get_game(gameID=gameID)

    if game is None:
        return "Game doesn't exist"

    if game.round < 0:
        return "Game either hasn't started yet or is already over"

    retstr = "Player acted successfully"

    if dataBase.check_action_allowed(player=current_user.id,gameID=gameID):
        
        if action == State.bet:
            if dataBase.bet(player=current_user.id,gameID=gameID):
                retstr = "Bet successfully"
            else:
                retstr = "Player folded because of low balance"
            

        elif action == State.raise_:
            amount = float(request.args.get("amount",0.0))

            dataBase.do_raise(current_user.id,gameID=gameID,amount=amount)
            retstr = "raised successfully"
        
        elif action == State.fold:
            dataBase.fold(player=current_user.id,gameID=gameID)
            retstr = "Player folded successfully"


        dataBase.do_round_update(gameID=gameID)

        return retstr
    #dataBase.start_game(player=str(current_user.id), id=gameID)
    return "Player cannot act right now!"

@app.route("/api/games/<int:gameID>/status",methods=["GET"])
@login_required
def game_status(gameID):
    game = dataBase.get_game(gameID=gameID)
    if game is None:
        return "Game does not exist"
    else:
        retstr:str = f"""Name: {game.name} Status: 
        {"NOT STARTED" if game.round == -1 else 
        "OVER" if game.round < 0 else "ONGOING"}<br>"""
        
        players = dataBase.get_players(game)
        usernames = [player.player_username for player in players]
        
        if current_user.id in usernames:
            if game.round > 0:
                retstr += "<br>Table:<br>&nbsp&nbsp" + CardToClearGerman.translate(game.table1)
                retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table2)
                retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table3)
            if game.round > 1:
                retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table4)
            if game.round > 2:
                retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table5)
            retstr += "<br><br> Round: " + str(game.round)

            if not game.round < 0:
                retstr += "<br><br> My Hand: "
                for player in dataBase.get_players(game):
                    if player.player_username == str(current_user.id):
                            retstr += " " + CardToClearGerman.translate(player.hand1)
                            retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(player.hand2)
                            retstr += "<br><br> Player-Status: " + player.status.value + "<br>"
                            retstr += "Paid this round: " + str(player.paid_this_round) + "<br>"
                    else:
                        continue

        return retstr

@app.route("/api/profile",methods=["GET"])
@login_required
def show_profile():
    account = dataBase.get_player_account(current_user.id)
    retstr:str = current_user.id + "<br> Stash: " + str(account.stash)

    for game in dataBase.get_games(current_user.id):
        
        retstr += "<br>" + str(game.gameID) + " " + str(game.name)
        
        if game.round < 0:
            if game.round == -1:  
                retstr += " Status: NOT STARTED <br>"
            else:
                retstr += " Status: OVER <br>"
        else:
            retstr += " Status: ONGOING <br>"

        if game.round > 0:
            retstr += " " + CardToClearGerman.translate(game.table1)
            retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table2)
            retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table3)
        if game.round > 1:
            retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table4)
        if game.round > 2:
            retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(game.table5)
        retstr += "<br> Round: " + str(game.round)

        if not game.round < 0:
            retstr += "<br> My Hand: "
            for player in dataBase.get_players(game):
                if player.player_username == str(current_user.id):
                        retstr += " " + CardToClearGerman.translate(player.hand1)
                        retstr += "&nbsp&nbsp&nbsp&nbsp" + CardToClearGerman.translate(player.hand2)
                        retstr += "<br> Player-Status: " + player.status.value + "<br>"
                else:
                    continue

    return retstr

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True, use_reloader=False)