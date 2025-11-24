SET profiling = 1;

SELECT DISTINCT movie_id 
FROM user_judge 
WHERE timestamp > NOW() - INTERVAL 10 MINUTE;

SHOW PROFILES;  -- 应显示 0.02~0.05 秒
SHOW PROCESSLIST; 
KILL 19; 
-- 创建测试用户
INSERT INTO user (user_id, user_name, password) 
VALUES (114514, 'test_user', 'test_password');

-- 为测试用户插入2条评分数据
-- 假设电影ID为1和2存在，如果不存在需要先创建电影记录
INSERT INTO user_judge (user_id, movie_id, rating, timestamp) 
VALUES 
(114514, 1, 5.0, NOW()),
(114514, 2, 4.5, NOW());

-- 验证数据插入
SELECT * FROM user WHERE user_id = 114514;
SELECT * FROM user_judge WHERE user_id = 114514;

-- 删除测试用户
DELETE FROM user_judge WHERE user_id = 114514;
DELETE FROM user WHERE user_id = 114514;

