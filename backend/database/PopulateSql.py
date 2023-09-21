from typing import List

from .SqlDataBase import SqlDataBase
from faker import Faker

dev_player = "TestPlayer"
dev_pwd = "1234"
fake = Faker()   


def populate_sql(sqlDataBase: SqlDataBase):   
    sqlDataBase.clear()
    
    usernames: List[str] = []

        
    for i in range(0,4):
           
        user = fake.user_name()
        pwd = fake.password()
        
        if i == 0:
            usernames.append(dev_player)
            user = dev_player
            pwd = dev_pwd
        elif i == 1:
            usernames.append(dev_player+"2")
            user = dev_player+"2"
            pwd = dev_pwd
        else:
            usernames.append(user) 
        
        sqlDataBase.create_player(user,pwd)
    
    sqlDataBase.create_game(usernames)
            
       
            
