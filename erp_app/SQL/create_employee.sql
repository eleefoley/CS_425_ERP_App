CREATE TABLE IF NOT EXISTS employee (
	employeeID int PRIMARY key NOT NULL CHECK (employeeID >= 0), 
	FirstName varchar(25), 
	MiddleName varchar(25), 
	LastName varchar(25), 
	Salary numeric NOT NULL CHECK (Salary >= 0), 
	Salaried boolean, 
	Hourly boolean, 
	Department varchar(50));
	--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE IF NOT EXISTS employeeID START 10001;
create index IF NOT EXISTS employeeID_index on employee(employeeID);