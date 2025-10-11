create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop TABLE if EXISTS user_judge;
drop table if EXISTS user;
drop Table if EXISTS movie_genre;
drop table if exists movie;

drop table if exists person;
CREATE table if NOT EXISTS user(
    user_name VARCHAR(50),
    user_id int primary key,
    pass_word VARCHAR(50) NOT NULL
); # check

CREATE TABLE if NOT EXISTS movie(
    movie_id VARCHAR(20) PRIMARY KEY,
    movie_name VARCHAR(100),
    isAdult int,
    release_year SMALLINT,
    runtime_minutes SMALLINT,
    average_rating DECIMAL(3,1),
    numVotes int,
    check (isAdult in (0,1)),
    check (release_year >= 1895 and release_year <= 2030)
    check (average_rating >= 1 and average_rating <= 10) # 按照所给的数据集，这里的限制是1-10
); # check

CREATE TABLE if NOT exists user_judge(
    user_id int,
    movie_id VARCHAR(20),
    comment int,# 这里限制一下比如说1-10
    Foreign Key (user_id) REFERENCES user(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    PRIMARY KEY(user_id, movie_id),
    check (comment>=1 and comment<=10)
); # check
#至此用户部分完成

create Table if not exists genre_table(
    genre_id SMALLINT PRIMARY key,
    genre_name VARCHAR(20)
);

create Table if not exists movie_genre(# 影片的类别
    movie_id VARCHAR(20),
    genre_id SMALLINT,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (genre_id) REFERENCES genre_table(genre_id),
    PRIMARY key(movie_id, genre_id)
);

CREATE table if NOT exists person(
    person_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    birth_year SMALLINT,
    death_year SMALLINT
);

create table if NOT exists movie_person(
    movie_id VARCHAR(20),
    person_id VARCHAR(20),
    job VARCHAR(20),
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (person_id) REFERENCES person(person_id),
    PRIMARY key(movie_id, person_id)
);