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

INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("cas1", "White Casual Shirt", "14", "4.1", "A nice, casual buttoned shirt", "cas1.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("cas2", "Black Casual Shirt", "14", "4.5", "A black casual buttoned shirt", "cas2.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("cas3", "Checkered Casual Shirt", "11", "3.5", "A checkered casual buttoned shirt", "cas3.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("cas4", "Grey Casual Shirt", " 13", " 4", "A grey casual buttoned shirt", " cas4.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("cas5", "Blue Casual Shirt", " 16", " 4.8", "A blue casual buttoned shirt", " cas5.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("dre1", "Blue Dress Shirt", "18", "4.6", "A blue dress shirt", "dre1.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("dre2", "White Dress Shirt", "18", "4.6", "A white dress shirt", "dre2.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("dre3", "Darkeer Blue Dress Shirt", "18", "4.6", "Another blue dress shirt", "dre3.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("dre4", "Another White Dress Shirt", "18", "4.6", "A white dress shirt", "dre4.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("dre5", "Blue Checkered Dress Shirt", "18", "4.6", "A blue checkered dress shirt", "dre5.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("dre6", "Darker White Dress Shirt", "18", "4.6", "A darker white dress shirt", "dre6.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("j1", "Faded Blue Jeans", "35", "3", "A pair of faded blue jeans", "j1.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("j2", "Another Pair of Faded Blue Jeans", "36", "3.3", "Another pair of faded blue jeans", "j2.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("j3", "Black Jeans", "37", "4", "A pair of black jeans", "j3.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("p1", "Light Blue Pants", "32", "4", "A pair of light blue pants", "p1.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("p2", "Black Pants", "32", "4", "A pair of black pants", "p2.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("p3", "Grey Pants", "32", "4", "A pair of grey pants", "p3.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("p4", "Sports Pants", "35", "4", "A pair of sports pants", "p4.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("p5", "Dark Blue Pants", "33", "4", "A pair of dark blue pants", "p5.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("ss1", "Cute Black Dress", "55", "4.8", "A cute black dress", "ss1.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("ss2", "Cute Black Romper", "55", "4.8", "A cute blue romper", "ss2.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("ss3", "Cute Flowery Dress", "55", "4.8", "A cute flowery dress", "ss3.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("ss4", "Cute Blue Dress", "55", "4.8", "A cute blue dress", "ss4.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("ss5", "Cute Black Cocktail Dress", "55", "4.8", "A cute black cocktail dress", "ss5.jpg");
INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES ("ss6", "Somber Black Dress", "55", "4.8", "A somber black dress", "ss6.jpg");
