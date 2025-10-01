create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop TABLE if EXISTS user_judge;
drop table if EXISTS user;
drop Table if EXISTS movie_genre;
drop table if EXISTS movie_pro_company;
drop table if EXISTS movie_pro_country;
drop Table if EXISTS movie;
drop table if EXISTS genre_table;
CREATE table if NOT EXISTS user(
    user_name VARCHAR(50),
    user_id int,
    pass_word VARCHAR(50) NOT NULL,
    PRIMARY KEY(user_name, user_id)
);

CREATE TABLE if NOT EXISTS movie(
    movie_id int PRIMARY KEY,
    movie_name VARCHAR(50),
    budget int,
    original_language varchar(5),
    popularity int,# 这里为了存储空间，考虑使用int
    release_date date,
    revenue int,# 此处用万元做单位
    vote_count int,# 评分人数
    vote_average int,# 评分的均分
    overview VARCHAR(2000)
);

CREATE TABLE if NOT exists user_judge(
    user_name VARCHAR(50),
    user_id int,
    movie_id int,
    comment int,# 这里限制一下比如说1-10
    Foreign Key (user_name, user_id) REFERENCES user(user_name, user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    PRIMARY KEY(user_name, user_id, movie_id),
    check (comment>=1 and comment<=10)
);
#至此用户部分完成


CREATE TABLE if NOT EXISTS genre_table(
    genre_id int PRIMARY KEY,
    genre_name VARCHAR(50)
);


create Table if not exists movie_genre(# 影片的类别
    movie_id int,
    genre int,
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    Foreign Key (genre) REFERENCES genre_table(genre_id),
    PRIMARY key(movie_id, genre)
);

CREATE Table if not exists movie_pro_country(
    movie_id int,
    pro_country VARCHAR(50),
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    PRIMARY key(movie_id, pro_country)
);


create table if not exists movie_pro_company(
    movie_id int,
    company_name VARCHAR(50),
    Foreign Key (movie_id) REFERENCES movie(movie_id),
    PRIMARY key(movie_id, company_name)
);


