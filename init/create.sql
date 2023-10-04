SET GLOBAL sql_mode = '';

CREATE TABLE game (
    game_id INTEGER AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL DEFAULT '',
    table_0 INTEGER NOT NULL,
    table_1 INTEGER NOT NULL,
    table_2 INTEGER NOT NULL,
    table_3 INTEGER NOT NULL,
    table_4 INTEGER NOT NULL,
    current_bet DOUBLE NOT NULL DEFAULT 1.0,
    pot DOUBLE NOT NULL DEFAULT 0.0,
    turn INTEGER NOT NULL DEFAULT -1,
    active BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY (game_id)
);

CREATE TABLE player (
    username VARCHAR(40) NOT NULL,
    password VARCHAR(100) NOT NULL,
    stash DOUBLE NOT NULL DEFAULT 10.0,
    PRIMARY KEY (username)
);


CREATE TABLE participates (
    game_id INTEGER,
    player_username VARCHAR(40),
    hand_0 INTEGER NOT NULL,
    hand_1 INTEGER NOT NULL,
    turn_state ENUM('RAISE','BET','FOLD','FALSE') NOT NULL DEFAULT 'FALSE',
    PRIMARY KEY (game_id, player_username),
    FOREIGN KEY (game_id) REFERENCES game(game_id) ON DELETE CASCADE,
    FOREIGN KEY (player_username) REFERENCES player(username) ON DELETE CASCADE
);

DELIMITER $$
CREATE TRIGGER block_card_update_game
BEFORE UPDATE ON game
FOR EACH ROW
BEGIN
    IF NEW.table_0 <> OLD.table_0 OR NEW.table_1 <> OLD.table_1 OR
       NEW.table_2 <> OLD.table_2 OR NEW.table_3 <> OLD.table_3 OR 
       NEW.table_4 <> OLD.table_4 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Update of protected columns not allowed';
    END IF;
END;
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER block_card_update_player
BEFORE UPDATE ON participates
FOR EACH ROW
BEGIN
    IF NEW.Hand_0 <> OLD.hand_0 OR NEW.hand_1 <> OLD.hand_1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Update of protected columns not allowed';
    END IF;
END;
$$
DELIMITER ;