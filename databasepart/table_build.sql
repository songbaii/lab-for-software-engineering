create DATABASE if NOT EXISTS soft_ware_engineering;
use soft_ware_engineering;
drop table if EXISTS user;
CREATE table if NOT EXISTS user(
    user_name VARCHAR(50) PRIMARY KEY,
    pass_word VARCHAR(50) NOT NULL
)