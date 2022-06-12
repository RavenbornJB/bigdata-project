CREATE KEYSPACE project_keyspace WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };
USE project_keyspace;


DROP TABLE IF EXISTS domains;
DROP TABLE IF EXISTS page_user;
DROP TABLE IF EXISTS 4;
DROP TABLE IF EXISTS pages_info;
DROP TABLE IF EXISTS page_users_info;


// task 1 -> return the list of existing domains for which pages were created
CREATE TABLE IF NOT EXISTS domains 
(
    domain text,
    PRIMARY KEY (domain)
);


// task 2 -> return all the pages which were created by the user with a specified user_id
CREATE TABLE IF NOT EXISTS page_user 
(
    domain text,
    page_name text,
    user_id int,
    PRIMARY KEY (domain, user_id)
);


// task 3 -> return the number of articles created for a specified domain
CREATE TABLE IF NOT EXISTS page_domains 
(
    domain text,
    page_id int,
    PRIMARY KEY (page_id, domain)
);


// task 4 -> return the page with the specified page_id
CREATE TABLE IF NOT EXISTS pages_info
(
    page_id int,
    page_name text,
    domain text,
    created_at date,
    PRIMARY KEY (page_id, domain)
);


// task 5 -> return the id, name, and the number of created pages of all the users
CREATE TABLE IF NOT EXISTS page_users_info
(
    user_id int,
    username text,
    page_id int,
    created_at date,
    PRIMARY KEY (domain)
);
