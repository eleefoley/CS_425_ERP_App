CREATE TABLE IF NOT EXISTS login (
	userID int PRIMARY KEY,
	privelege varchar (25),
	loginTime timestamp,
	logoutTime timestamp
	);

--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE userID START 1000001;
create index userID_index on login(userID);

