DROP TABLE IF EXISTS userinfo;
DROP TABLE IF EXISTS userdata;

CREATE TABLE userinfo (
	id INT PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(50) UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE inventory (
	ind INT(50) PRIMARY KEY AUTO_INCREMENT NOT NULL,
	itemcode VARCHAR(10) UNIQUE NOT NULL,
	name VARCHAR(50),
	price FLOAT(5,2),
	rating FLOAT(3,1),
	descrip VARCHAR(200),
	img VARCHAR(30),
	FULLTEXT (name)
);
