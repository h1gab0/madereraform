CREATE DATABASE IF NOT EXISTS test;
CREATE USER 'gabo'@'%' IDENTIFIED WITH mysql_native_password BY 'gabo';
GRANT ALL PRIVILEGES ON test.* TO 'gabo'@'%';
FLUSH PRIVILEGES;