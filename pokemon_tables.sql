 USE pokemon;


-- CREATE TABLE pokemon(
--     id int auto_increment primary key,
--     name VARCHAR(20),
--     type VARCHAR(20),
--     weight int,
--     height int
-- );


-- CREATE TABLE trainer(
--     name VARCHAR(20) primary key,
--     town varchar(20)
-- );

-- CREATE TABLE ownership (
--     owner_name varchar(20),
--     pokemon_id INT,
--     PRIMARY KEY (owner_name , pokemon_id),
--     FOREIGN KEY (owner_name)
--         REFERENCES owner (name),
--     FOREIGN KEY (pokemon_id)
--         REFERENCES pokemon (id)
-- );

-- insert into types (name) values("grass")
-- SELECT * FROM types where name= "grass"
-- Delete From types
-- SELECT * FROM types where name= "grass"


-- select own_name 
-- from own_by ,pokemon
--  where pokemon_id= id and name="gengar"

--  select name 
--  from own_by ob,pokemon p
--   where pokemon_id= id and own_name="Loga"

 select name from
 (select pokemon_id, count(*) as count
 from own_by
 group by pokemon_id) as ob1, pokemon
 where count in (select max(count) from
 (select pokemon_id, count(*) as count
 from own_by
 group by pokemon_id) as ob2) and id=pokemon_id

