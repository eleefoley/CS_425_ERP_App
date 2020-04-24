CREATE TABLE IF NOT EXISTS employeeLogin (
	employeeID int,
	userID int,
	PRIMARY KEY (employeeID, userID),
	FOREIGN KEY (employeeID) REFERENCES employee (employeeID)
	on delete cascade on update cascade,
	FOREIGN KEY (userID) REFERENCES login (userID)
	on delete cascade on update cascade
	);

