from flask_sqlalchemy import SQLAlchemy
from typing import List

from .DataBase import DataBase
from models import Card, Player, Game, Participates,db
import random
import bcrypt


class SqlDataBase(DataBase):

    def __init__(self, app) -> None:
        self.mysqldb = db
        self.mysqldb.init_app(app)
        self.mysqlDateFormat = "%Y-%m-%d"
    
            
    
    def create_player(self, username:str, password:str) -> None:
        
        self.mysqldb.session.add(Player(username=username,password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())))
        
        self.mysqldb.session.commit()
        
    def create_game(self, players: List[str], name: str = '') -> None:
        cards = list(Card)
        random.shuffle(cards)
        to_insert_game = Game(name=name,table_0=cards.pop(),table_1=cards.pop(),table_2=cards.pop(),table_3=cards.pop(),table_4=cards.pop())
        
        self.mysqldb.session.add(to_insert_game)
        self.mysqldb.session.commit()
        for player in players:
            self.mysqldb.session.add(Participates(game_id=to_insert_game.game_id,player_username=player,hand_0=cards.pop(),hand_1=cards.pop()))
        
        self.mysqldb.session.commit()
        
    def join_game(self, player:str, id = None, name = None) -> None:
        cards = list(Card)
        join = None
        if id is None and name is None:
            raise Exception("Neither id nor name given")
        elif id is None:
            name = str(name)
            if len(Game.query.filter(Participates.participation.has(name=name)).all()) is None:
                raise Exception("Game does not exist")
            game = Game.query.filter_by(name=name).first()
            cards.remove(game.table_0)
            cards.remove(game.table_1)
            cards.remove(game.table_2)
            cards.remove(game.table_3)
            cards.remove(game.table_4)
            participants = Participates.query.filter(Participates.participation.has(name=name)).all()
            for participant in participants:
                cards.remove(participant.hand_0)
                cards.remove(participant.hand_1)
                if participant.player_username == player:
                    raise Exception("Player already joined")
            join = Participates(game_id=game.game_id,player_username=player,hand_0=cards.pop(),hand_1=cards.pop())
        else:
            id = int(id)
            if Game.query.filter_by(game_id=id).all() is None:
                raise Exception("Game does not exist")
            game = Game.query.filter_by(game_id=id).first()
            cards.remove(game.table_0)
            cards.remove(game.table_1)
            cards.remove(game.table_2)
            cards.remove(game.table_3)
            cards.remove(game.table_4)
            participants = Participates.query.filter_by(game_id=id).all()
            for participant in participants:
                cards.remove(participant.hand_0)
                cards.remove(participant.hand_1)
                if participant.player_username == player:
                    raise Exception("Player already joined")
            join = Participates(game_id=id,player_username=player,hand_0=cards.pop(),hand_1=cards.pop())
        self.mysqldb.session.add(join)
        self.mysqldb.session.commit()                                
                


    def get_games(self, username:str) -> List[Game]:
        return self.mysqldb.session.query(Game).join(Participates, Game.game_id == Participates.game_id).filter_by(player_username=username).all()

    def get_players(self,game:Game) -> List[Participates]:
        return Participates.query.filter_by(game_id=game.game_id).all()

    def login(self, username:str, pwd:str) -> bool:
        hash :str = Player.query.filter_by(username=username).with_entities(Player.password).first()

        if hash is None: 
            return False
        
        hash = hash[0]
        
        return bcrypt.checkpw(password=pwd.encode('utf-8'),hashed_password=hash.encode('utf-8'))
    
    def clear(self) -> None:
        Player.query.delete()
        Game.query.delete()
        Participates.query.delete()
        