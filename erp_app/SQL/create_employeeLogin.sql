CREATE TABLE IF NOT EXISTS employeeLogin (
	userId int primary key NOT NULL CHECK (userId >= 0),
	employeeID int NOT NULL CHECK (employeeID >= 0),
	userName varchar (25),
	userRole varchar(25),
	FOREIGN KEY (employeeID) REFERENCES employee (employeeID)
	on delete cascade on update cascade
	);

