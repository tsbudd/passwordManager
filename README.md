# passwordManager
## Description
Secure Password manager using MySQL database

## Setting up database (MacOS X 12+)
#### 1. Install MariaDB with Homebrew
See [MariaDB Documentation](https://mariadb.com/resources/blog/installing-mariadb-10-1-16-on-mac-os-x-with-homebrew/) on how to install MariaDB database on Mac OS.


#### 2. Create a new user
```
sudo mysql -u root -p
```
enter root password (usually computer password but it could have changed when you set it up in step 1)
```
CREATE USER '<yourNameNoSpaces>'@'localhost' IDENTIFIED BY '<yourPassword>';
```

#### 3. create database
```
CREATE DATABASE passwords;
```

#### 4. give new user permissions to pennyPusherTest
```
GRANT ALL PRIVILEGES ON passwords.* TO '<yourNameNoSpaces>'@'localhost';
```

#### 5. flush privileges
```
FLUSH PRIVILEGES;
```

##### Now you have a database and a user

#### 6. log out of sudo and log in with your new username and password

```
exit;
mysql -u <yourNameNoSpaces> -p
enter password: <yourPassword>
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 336
Server version: 10.8.3-MariaDB Homebrew

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

USE passwords;
```

#### 7. run script to set up database
Use [this](passDatabaseCreation.sql) to create your database tables and procedures

## Required Python Libraries
#### pwinput
```
pip install pwinput
```
#### cryptocode
```
pip install cryptocode
```
#### tabulate
```
pip install tabulate
```
#### mysql.connector
```
pip install mysql-connector-python
```
