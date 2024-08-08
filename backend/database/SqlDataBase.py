from flask_sqlalchemy import SQLAlchemy
from typing import List

from .DataBase import DataBase
from models import Card, Player, PokerGame, Plays,db, State
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
        to_insert_game = PokerGame(name=name,table1=cards.pop(),table2=cards.pop(),table3=cards.pop(),table4=cards.pop(),table5=cards.pop())
        
        self.mysqldb.session.add(to_insert_game)
        self.mysqldb.session.commit()
        for player in players:
            self.mysqldb.session.add(Plays(gameID=to_insert_game.gameID,player_username=player,hand1=cards.pop(),hand2=cards.pop()))
        
        self.mysqldb.session.commit()
        
    def start_game(self, player:str, id = None) -> None:
        if id is None:
            raise Exception("Id not given")
        elif PokerGame.query.filter_by(gameID=int(id)).all() is None:
            raise Exception("Game with given ID: {id} does not exist")
        else:
            id = int(id)
            game = PokerGame.query.filter_by(gameID=id).first()
            
            # return without doing anything if game has already started or ended
            

            participants = Plays.query.filter_by(gameID=id).all()
            usernames = [participant.player_username for participant in participants]
            if player in usernames:
                if not game.round == -1:
                    return
                game.round = 0
            else:
                raise Exception("Player didn't join the game")

        self.mysqldb.session.commit()


    def join_game(self, player:str, id = None, name = None) -> None:
        cards = list(Card)
        join = None
        if id is None and name is None:
            raise Exception("Neither id nor name given")
        elif id is None:
            name = str(name)
            if len(PokerGame.query.filter(Plays.participation.has(name=name)).all()) is None:
                raise Exception("PokerGame does not exist")
            game = PokerGame.query.filter_by(name=name).first()
            if game.round != -1:
                raise Exception("Game started already")
            cards.remove(game.table1)
            cards.remove(game.table2)
            cards.remove(game.table3)
            cards.remove(game.table4)
            cards.remove(game.table5)
            participants = Plays.query.filter(Plays.participation.has(name=name)).all()
            for participant in participants:
                cards.remove(participant.hand1)
                cards.remove(participant.hand2)
                if participant.player_username == player:
                    raise Exception("Player already joined")
            join = Plays(gameID=game.gameID,player_username=player,hand1=cards.pop(),hand2=cards.pop())
        else:
            id = int(id)
            if PokerGame.query.filter_by(gameID=id).all() is None:
                raise Exception("PokerGame does not exist")
            game = PokerGame.query.filter_by(gameID=id).first()
            if game.round != -1:
                raise Exception("Game started already")
            cards.remove(game.table1)
            cards.remove(game.table2)
            cards.remove(game.table3)
            cards.remove(game.table4)
            cards.remove(game.table5)
            participants = Plays.query.filter_by(gameID=id).all()
            for participant in participants:
                cards.remove(participant.hand1)
                cards.remove(participant.hand2)
                if participant.player_username == player:
                    raise Exception("Player already joined")
            join = Plays(gameID=id,player_username=player,hand1=cards.pop(),hand2=cards.pop())
        self.mysqldb.session.add(join)
        self.mysqldb.session.commit()                                
                


    def get_games(self, username:str) -> List[PokerGame]:
        return self.mysqldb.session.query(PokerGame).join(Plays, PokerGame.gameID == Plays.gameID).filter_by(player_username=username).all()
    
    def get_game(self, gameID:int) -> PokerGame | None:
        return PokerGame.query.filter_by(gameID=gameID).first()

    def get_players(self,game:PokerGame) -> List[Plays]:
        return Plays.query.filter_by(gameID=game.gameID).all()

    def get_player(self, player:str, gameID:int) -> Plays:
        return Plays.query.filter_by(player_username=player, gameID=gameID).first()

    def check_action_allowed(self, player:str, gameID:int) -> bool:
        player_state = Plays.query.filter_by(gameID=gameID,player_username=player).first()

        if player_state is None:
            raise Exception("Player not part of the game")

        if player_state.status == State.unkown:
            return True
        
        return False

    # returns false if player is force folded
    def bet(self, player:str, gameID:int) -> bool:
        game = self.get_game(gameID=gameID)
        player_game = Plays.query.filter_by(player_username=player, gameID=gameID).first()
        player_account = Player.query.filter_by(username=player).first()

        if game.stake > player_account.stash:
            player_game.status = State.fold

            #commit changes
            self.mysqldb.session.commit()
            return False
        paid_amount = (game.stake - player_game.paid_this_round)
        player_account.stash -= paid_amount
        player_game.paid_this_round += paid_amount
        player_game.status = State.bet
        
        #commit changes
        self.mysqldb.session.commit()
        return True


    def do_raise_update(self, player_raise:str, gameID:int) -> None:
        players = Plays.query.filter_by(gameID=gameID).all()

        for player in players:
            
            if player.player_username == player_raise or player.status == State.fold:
                continue

            player.status = State.unkown

        #commit changes
        self.mysqldb.session.commit()

    def do_round_update(self, gameID:int) -> None:
        game = PokerGame.query.filter_by(gameID=gameID).first()
        players = Plays.query.filter_by(gameID=gameID).all()
        next_round = True
        not_folded = 0

        if game.round < 0:
            raise Exception("Game either hasn't started yet or is already over")

        for player in players:
            
            if player.status == State.unkown:
                next_round = False
            elif player.status != State.fold:
                    not_folded += 1
       

        if next_round:
            if game.round < 3 and not_folded > 1:
                
                for player in players:
                    
                    if player.status == State.fold:
                        continue

                    player.status = State.unkown
                
                game.round += 1

            else:
                #TODO: Implement winning mechanics


                # Declare game to be over
                game.round = -2
        
        #commit changes
        self.mysqldb.session.commit()


    def get_player_account(self, player:str) -> Player:
        return Player.query.filter_by(username=player).first()

    def login(self, username:str, pwd:str) -> bool:
        hash :str = Player.query.filter_by(username=username).with_entities(Player.password).first()

        if hash is None: 
            return False
        
        hash = hash[0]
        
        return bcrypt.checkpw(password=pwd.encode('utf-8'),hashed_password=hash.encode('utf-8'))
    
    def clear(self) -> None:
        Player.query.delete()
        PokerGame.query.delete()
        Plays.query.delete()
        