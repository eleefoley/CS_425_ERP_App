CREATE TABLE IF NOT EXISTS login (
	userName varchar(25),
	privelege varchar (25),
	loginTime timestamp primary key,
	logoutTime timestamp
	);