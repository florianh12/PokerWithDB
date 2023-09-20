from typing import List

from .SqlDataBase import SqlDataBase
from models import *

from faker import Faker
from datetime import datetime, timedelta
import random
import csv


dev_player = "TestPlayer"
dev_pwd = "1234"
fake = Faker()   


def populate_sql(sqlDataBase: SqlDataBase):   
    sqlDataBase.clear()
    
    usernames: List[str] = []
    players: List[Player] = []

        
    for i in range(0,4):
           
        player = Player("","",None)
        user = fake.user_name()
        
        if i == 0:
            usernames.append(dev_player)
            player = Player(dev_player,dev_pwd,None)
        elif i == 1:
            usernames.append(dev_player+"2")
            player = Player(dev_player+"2",dev_pwd,None)
        else:
            usernames.append(user)
            player = Player(user,fake.password(),None) 
        
        sqlDataBase.create_player(player)
        players.append(player)
    
    sqlDataBase.create_game(players)
            
       
            
