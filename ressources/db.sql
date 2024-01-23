DROP DATABASE IF EXISTS pro_league_player,
CREATE DATABASE IF NOT EXISTS pro_league_player,

use pro_league_player,

CREATE TABLE IF NOT EXISTS players(
    ID INT PRIMARY KEY AUTOINCREMENT,
    name varchar(150) not null,
    fullname vachar(300) not null,
    age int,
    value float,
    wage float,
    position varchar(5),
    origin varchar(25),
    club varchar(100),
    contract_start int,
    contract_end int
)