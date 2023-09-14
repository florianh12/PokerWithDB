from flask_mysqldb import MySQL
from typing import List, Tuple

from .DataBase import DataBase
from dataclasses import replace
from models import *
import random
import bcrypt
import time


class SqlDataBase(DataBase):

    def __init__(self, app) -> None:
        again = True
        while again:
            try:
                self.mysql = MySQL(app)
                self.mysqlDateFormat = "%Y-%m-%d"
                if self.mysql is not None:
                    again = False
            except Exception as e:
                pass

    def create_player(self, player: Player) -> None:
        
        cur = self.mysql.connection.cursor()
        
        cur.execute(
            """
            INSERT INTO player(username, password) 
            VALUES (%s, %s)
            """,
            (player.user_name, bcrypt.hashpw(player.password.encode('utf-8'),bcrypt.gensalt()))
        )
        
        self.mysql.connection.commit()
        
    def create_game(self, players: List[Player]) -> None:
        cards = list(Card)
        random.shuffle(cards)
        
        cur = self.mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO game(table_0, table_1, table_2, table_3, table_4)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (cards.pop().value, cards.pop().value, cards.pop().value, cards.pop().value, cards.pop().value) 
        )
        gameid = cur.lastrowid
        for player in players:
            cur.execute(
            """
            INSERT INTO participates(game_id, player_username, hand_0, hand_1)
            VALUES (%s, %s, %s, %s)
            """,
            (gameid, player.user_name, cards.pop().value, cards.pop().value) 
        )
        
        self.mysql.connection.commit()

    def get_games(self, player:Player) -> List[Game]:
        game_list = list()
        cur = self.mysql.connection.cursor()
        
        cur.execute(''' SELECT game_id, table_0, table_1, table_2, table_3, table_4 FROM game NATURAL JOIN participates WHERE player_username = %s ''',(player.user_name,))
        results = cur.fetchall()
        for entry in results:
            game = Game(*entry)
            game_list.append(game)
        return game_list

    def get_players(self,game:Game) -> List[Player]:
        player_list = list()
        cur = self.mysql.connection.cursor()
        
        cur.execute(''' SELECT username, password, hand_0, hand_1 FROM player NATURAL JOIN participates WHERE game_id = %s ''',(game._id,))
        results = cur.fetchall()
        for entry in results:
            player = Player(entry[0],entry[1],entry[2:])
            player_list.append(player)
        return player_list



  

    def login(self, username:str, pwd:str) -> bool:
        cur = self.mysql.connection.cursor()
        cur.execute(
            """
            SELECT password
            FROM player
            WHERE username = %s 
            """,
            (username,)
        )
        hash = cur.fetchone()

        if hash is None: 
            return False
        
        return bcrypt.checkpw(password=pwd.encode('utf-8'),hashed_password=hash[0].encode('utf-8'))


    def validate_login_developer(self, username: str, password: str) -> object:
        return self.validate_login_person(username, password)


    def validate_login_interviewer(self, username: str, password: str) -> object:
        return self.validate_login_person(username, password)


    def validate_login_company(self, name: str, password: str) -> object:
        cur = self.mysql.connection.cursor()
        cur.execute(
            """
            SELECT company_id
            FROM company
            WHERE company_name=%s AND password=%s 
            """,
            (name, password)
        )
        results = cur.fetchone()

        if results is None: 
            return { "successLogin": False }
        return { "successLogin": True, "id": results[0] }


    


    def get_job_offers(self, searchQuery: str = "", developerId: Key = 1) -> List[JobOffer]:
        developerId = int(developerId)
        cur = self.mysql.connection.cursor()
        searchQuery = "%" + searchQuery + "%"
        cur.execute(
            """
            SELECT job_offer.company_id, offer_id, job_title, description, pay, 
            begin, end, job_offer.interviewer_id, company.company_name, person.username,
            EXISTS(SELECT * FROM is_interested_in AS is_intr WHERE is_intr.offer_id=job_offer.offer_id AND is_intr.company_id = job_offer.company_id AND is_intr.developer_id = %s) 
            FROM job_offer
            INNER JOIN company ON company.company_id=job_offer.company_id
            INNER JOIN person ON person.person_id=job_offer.interviewer_id
            WHERE LOWER(job_title) LIKE LOWER(%s) OR LOWER(company_name) LIKE LOWER(%s)
            """,
            (developerId, searchQuery, searchQuery)
        )
        result = cur.fetchall()

        jobOffers = [ JobOffer(
            *row[:-4], 
            interviewer=row[-4], 
            company_name=row[-3], 
            interviewer_name=row[-2], 
            developer_interested=row[-1]
        ) for row in result ]      

        return jobOffers
        

    def mark_job_offer_as_interested(self, companyId: Key, jobOfferId: Key, developerId: Key) -> None:
        companyId = int(companyId)
        jobOfferId = int(jobOfferId)
        developerId = int(developerId)

        cur = self.mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO is_interested_in(company_id, offer_id, developer_id)
            VALUES (%s, %s, %s)
            """,
            (companyId, jobOfferId, developerId)
        )
        self.mysql.connection.commit()


    def get_marked_job_offers(self, developerId: Key) -> List[JobOffer]:
        developerId = int(developerId)

        cur = self.mysql.connection.cursor()
        cur.execute(
            """
            SELECT job_offer.company_id, job_offer.offer_id, job_title, description, 
            pay, begin, end, interviewer_id, company.company_name, person.username
            FROM is_interested_in
            INNER JOIN job_offer ON job_offer.offer_id=is_interested_in.offer_id
            INNER JOIN company ON company.company_id=job_offer.company_id
            INNER JOIN person ON person.person_id=job_offer.interviewer_id
            WHERE is_interested_in.developer_id=%s
            """,
            (developerId,) # comma is needed, else python thinks it is an expression and not a tuple
        )
        result = cur.fetchall()
        jobOffers = [ JobOffer(
            *row[:-3], 
            interviewer=row[-3], 
            company_name=row[-2], 
            interviewer_name=row[-1], 
            developer_interested=True
        ) for row in result ]        
        return jobOffers
    

    def get_tuples_is_interested_in(self) -> List[tuple[int, int, int]]:
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM is_interested_in")
        result = cur.fetchall()
        return result




    

    def generate_token(self, companyId: Key) -> str:
        companyId = int(companyId)

        cur = self.mysql.connection.cursor()
        cur.callproc('generate_verification_token',args=(companyId,))
        self.mysql.connection.commit()
        cur.execute("""SELECT verification_token FROM company WHERE company_id = %s """,(companyId,))
        token = cur.fetchone()[0]
        return token


    def block_person(self, blocker: Key, blockee: Key) -> None:
        blocker = int(blocker)
        blockee = int(blockee)

        cur = self.mysql.connection.cursor()
        cur.execute(""" INSERT INTO blocks(blocker, blocked) VALUES(%s, %s)""", (blocker, blockee))
        self.mysql.connection.commit()
    
    
    def get_tuples_blocks(self) -> List[Tuple[int, int]]:
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM blocks")
        result = cur.fetchall()
        return result


    def clear(self) -> None:
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM game")
        cur.execute("DELETE FROM participates")
        cur.execute("DELETE FROM player")
        cur.execute("ALTER TABLE game AUTO_INCREMENT=1")
        self.mysql.connection.commit()
    
    def report_hejze(self, companyID: Key) -> List[object]:
        if not companyID.isdigit():
            raise AttributeError("Invalid CompanyID!")
        cur = self.mysql.connection.cursor()
        cur.execute("""
                    SELECT p.first_name, p.last_name, i.strictness,i.kindness,i.exp,i.blockeddevs
                    FROM person p INNER JOIN (SELECT i.person_id,i.strictness,i.kindness,i.exp,COUNT(*) AS blockeddevs 
                    FROM interviewer i INNER JOIN blocks b 
                    ON b.blocker = i.person_id 
                    INNER JOIN developer d 
                    ON b.blocked = d.person_id 
                    WHERE i.company_id = %s
                    GROUP BY i.person_id 
                    ORDER BY COUNT(*) DESC
                    LIMIT 5) i ON p.person_id=i.person_id
                    """, (int(companyID),))
        result = cur.fetchall()
        return result


    def report_wild(self, searchQuery: str = "") -> List[object]:
        cur = self.mysql.connection.cursor()
        searchQuery = "%" + searchQuery + "%"
        cur.execute(
            """
            SELECT company.company_id, company.company_name, COUNT(developer_id) as count_interested_developers FROM company
            JOIN is_interested_in ON is_interested_in.company_id = company.company_id
            WHERE is_interested_in.offer_id IN (
                SELECT job_offer.offer_id FROM job_offer
                WHERE job_title LIKE %s
            )
            GROUP BY company.company_id
            ORDER BY count_interested_developers DESC
            LIMIT 5
            """,
            (searchQuery,) # comma is needed, else python parses it as an expression, instead of a tuple
        )
        result = cur.fetchall()
        return [ { "id": row[0], "name": row[1], "count_interested_developers": row[2]} for row in result ]
