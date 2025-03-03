-- Replace 'your_mysql_root_password' with your actual root password when logging in

-- Login to MySQL as root (if using the command line):
-- mysql -u root -p

-- Create the database
CREATE DATABASE IF NOT EXISTS `help_dev_db`;

-- Create the user and set the password
CREATE USER IF NOT EXISTS 'help_dev'@'localhost' IDENTIFIED BY 'dev@ROOT_|25|';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON `help_dev_db`.* TO 'help_dev'@'localhost';

-- Apply changes immediately
FLUSH PRIVILEGES;

-- Exit MySQL (if using the command line):
-- EXIT;