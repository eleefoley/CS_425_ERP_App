CREATE TABLE IF NOT EXISTS employee (
	employeeID int PRIMARY KEY, FirstName varchar(25), 
	MiddleName varchar(25), LastName varchar(25), Salary numeric, 
	Salaried boolean, Hourly boolean, Department varchar(50));
	--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE employeeID START 10001;
create index employeeID_index on employee(employeeID);