
drop DATABASE soft_ware_engineering;
create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop TABLE if EXISTS user_judge;
drop table if EXISTS user;
drop Table if EXISTS movie_genre;
drop TABLE if exists genre_table;
drop table if exists movie;
DROP TABLE IF EXISTS item_similarities;
CREATE table if NOT EXISTS user(
    user_id int primary key auto_increment,
    user_name VARCHAR(50),
    password VARCHAR(50) NOT NULL
); # check

CREATE TABLE if NOT EXISTS movie(
    movie_id int PRIMARY KEY auto_increment,
    movie_name VARCHAR(1000),
    release_year SMALLINT
); # check and done

CREATE TABLE if NOT exists user_judge(
    user_id int,
    movie_id int,
    rating DECIMAL(2,1),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  # 添加时间戳字段
    Foreign Key (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    PRIMARY KEY(user_id, movie_id),
    check (rating > 0 AND rating <= 5.0 AND (rating * 2) = FLOOR(rating * 2)) # 小数部分只能是0或5, 0.5-5
); # check
#至此用户部分完成

create Table if not exists genre_table(
    genre_id SMALLINT PRIMARY key auto_increment,
    genre_name VARCHAR(20)
);# check and done

create Table if not exists movie_genre(# 影片的类别
    movie_id int,
    genre_id SMALLINT,
    Foreign Key (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    Foreign Key (genre_id) REFERENCES genre_table(genre_id) ON DELETE CASCADE,
    PRIMARY key(movie_id, genre_id)
); # check and done

create table if not exists user_comment(
    user_id int,
    movie_id int,
    comment VARCHAR(1000),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  # 添加时间戳字段
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    PRIMARY KEY(user_id, movie_id)
); # check and done

# 以下为推荐系统使用
-- 创建 item_similarities 表（用于存 Top-K 相似物品）
CREATE TABLE IF NOT EXISTS item_similarities (
    movie_id INT NOT NULL,
    similar_movie_id INT NOT NULL,
    similarity DECIMAL(5,4) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (similar_movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, similar_movie_id),
    INDEX idx_movie_id (movie_id),
    INDEX idx_similarity (similarity DESC)
);

DROP TABLE IF EXISTS movie_stats;
CREATE TABLE movie_stats (
    movie_id INT PRIMARY KEY,
    avg_rating DECIMAL(3,2) NOT NULL,
    vote_count INT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    INDEX idx_vote_avg (vote_count, avg_rating)  -- ✅ 关键索引
);

-- 添加覆盖索引（关键！）
ALTER TABLE user_judge 
ADD INDEX idx_movie_rating (movie_id, rating), 
ALGORITHM=INPLACE, LOCK=NONE;  -- 在线添加，不锁表
INSERT INTO movie_stats (movie_id, avg_rating, vote_count)
SELECT 
    movie_id,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS vote_count
FROM user_judge
GROUP BY movie_id;