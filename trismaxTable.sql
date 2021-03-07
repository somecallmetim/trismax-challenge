create table trismaxChallenge(
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	employeeName VARCHAR(255),
	company ENUM('Apple', 'Microsoft', 'Google'),
	gender ENUM('Male', 'Female', 'Other'),
	dateEmployed DATE,
	status ENUM('Active', 'Inactive'),
	vacation INT,
	PRIMARY KEY ( id )
);