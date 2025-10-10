create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop TABLE if EXISTS user_judge;
drop table if EXISTS user;
drop Table if EXISTS movie_genre;
drop table if EXISTS movie_pro_company;
drop table if EXISTS movie_pro_country;
drop table if EXISTS country;
drop table if EXISTS company;
drop table if exists movie_cast;
drop Table if EXISTS movie;

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
    check (average_rating >= 0 and average_rating <= 10)
); # check

CREATE TABLE if NOT exists user_judge(
    user_id int,
    movie_id int,
    comment int,# 这里限制一下比如说1-10
    Foreign Key (user_id) REFERENCES user(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    PRIMARY KEY(user_id, movie_id),
    check (comment>=1 and comment<=10)
); # check
#至此用户部分完成


create Table if not exists movie_genre(# 影片的类别
    movie_id int,
    genre_id int,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    PRIMARY key(movie_id, genre_id)
);

CREATE table if not exists country(# 建立这个表主要是为了节省空间
    country_full_name VARCHAR(50),
    country_short_name VARCHAR(10) PRIMARY key
);

CREATE Table if not exists movie_pro_country(
    movie_id int,
    country_short_name VARCHAR(10) ,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (country_short_name) REFERENCES country(country_short_name),
    PRIMARY key(movie_id, country_short_name)
);

CREATE table if not exists company(
    company_name VARCHAR(100),
    company_id int PRIMARY KEY
);

create table if not exists movie_pro_company(
    movie_id int,
    company_id int,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (company_id) REFERENCES company(company_id),
    PRIMARY key(movie_id, company_id)
);

create table if not exists person(
    person_id int PRIMARY KEY,
    person_name VARCHAR(50)
);

create table if not exists movie_cast(
    movie_id int,
    cast_id int,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (cast_id) REFERENCES person(person_id),
    PRIMARY key(movie_id, cast_id)
);