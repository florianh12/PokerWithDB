SET GLOBAL sql_mode = '';

CREATE TABLE PokerGame (
    gameID INTEGER AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL DEFAULT '',
    table1 INTEGER NOT NULL,
    table2 INTEGER NOT NULL,
    table3 INTEGER NOT NULL,
    table4 INTEGER NOT NULL,
    table5 INTEGER NOT NULL,
    stake DOUBLE NOT NULL DEFAULT 1.0,
    pot DOUBLE NOT NULL DEFAULT 0.0,
    round INTEGER NOT NULL DEFAULT -1,
    PRIMARY KEY (gameID)
);

CREATE TABLE player (
    username VARCHAR(40) NOT NULL,
    password VARCHAR(100) NOT NULL,
    stash DOUBLE NOT NULL DEFAULT 10.0,
    PRIMARY KEY (username)
);


CREATE TABLE plays (
    gameID INTEGER,
    player_username VARCHAR(40),
    hand1 INTEGER NOT NULL,
    hand2 INTEGER NOT NULL,
    status ENUM('RAISE','BET','FOLD','UNKNOWN') NOT NULL DEFAULT 'UNKNOWN',
    paid_this_round DOUBLE NOT NULL DEFAULT 0.0,
    PRIMARY KEY (gameID, player_username),
    FOREIGN KEY (gameID) REFERENCES PokerGame(gameID) ON DELETE CASCADE,
    FOREIGN KEY (player_username) REFERENCES player(username) ON DELETE CASCADE
);

CREATE TABLE won_by (
    gameID INTEGER,
    username VARCHAR(40),
    PRIMARY KEY (gameID, username),
    FOREIGN KEY (gameID) REFERENCES PokerGame(gameID) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES player(username) ON DELETE CASCADE
);

DELIMITER $$
CREATE TRIGGER block_card_update_game
BEFORE UPDATE ON game
FOR EACH ROW
BEGIN
    IF NEW.table1 <> OLD.table1 OR NEW.table2 <> OLD.table2 OR
       NEW.table3 <> OLD.table3 OR NEW.table4 <> OLD.table4 OR 
       NEW.table5 <> OLD.table5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Update of protected columns not allowed';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER block_card_update_player
BEFORE UPDATE ON plays
FOR EACH ROW
BEGIN
    IF NEW.Hand_0 <> OLD.hand1 OR NEW.hand2 <> OLD.hand2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Update of protected columns not allowed';
    END IF;
END;
$$
DELIMITER ;