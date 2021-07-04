 USE pokemon;
 
CREATE TABLE pokemon(
    id int auto_increment primary key,
    name VARCHAR(20),
    weight int,
    height int
);

CREATE TABLE types(
	id int,
    type varchar(20),
    primary key(id,type)
);

CREATE TABLE trainer(
    name VARCHAR(20) primary key,
    town varchar(20)
);

CREATE TABLE ownership (
    owner_name varchar(20),
    pokemon_id INT,
    PRIMARY KEY (owner_name , pokemon_id),
    FOREIGN KEY (owner_name)
        REFERENCES trainer (name),
    FOREIGN KEY (pokemon_id)
        REFERENCES pokemon (id)
); 
