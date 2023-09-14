SET GLOBAL sql_mode = '';

CREATE TABLE game (
    game_id INTEGER AUTO_INCREMENT,
    table_0 Integer NOT NULL,
    table_1 Integer NOT NULL,
    table_2 Integer NOT NULL,
    table_3 Integer NOT NULL,
    table_4 Integer NOT NULL,
    PRIMARY KEY (game_id)
);

CREATE TABLE player (
    username VARCHAR(40) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (username)
);


CREATE TABLE participates (
    game_id INTEGER,
    player_username VARCHAR(40),
    hand_0 INTEGER NOT NULL,
    hand_1 INTEGER NOT NULL,
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