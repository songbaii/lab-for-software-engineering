use soft_ware_engineering;
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