CREATE TABLE IF NOT EXISTS employeeLogin (
	userID int primary key,
	employeeID int,
	userName varchar (25),
	userRole varchar(25),
	FOREIGN KEY (employeeID) REFERENCES employee (employeeID)
	on delete cascade on update cascade
	);

