create table winterOlympics(
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	year INT,
	city VARCHAR(255),
	sport VARCHAR(255),
	discipline VARCHAR(255),
	noc VARCHAR(255),
	event VARCHAR(255),
	gender ENUM('M', 'W', 'X'),
	medal ENUM('Gold', 'Silver', 'Bronze'),
	PRIMARY KEY ( id )
);