DROP TABLE IF EXISTS userinfo;
DROP TABLE IF EXISTS userdata;

CREATE TABLE userinfo (
	id INT PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(50) UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE userdata (
	id INT,
	username VARCHAR(50) UNIQUE NOT NULL
);