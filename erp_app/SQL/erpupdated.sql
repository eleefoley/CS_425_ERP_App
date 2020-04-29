
CREATE TABLE INVENTORY (
	inventoryID int PRIMARY KEY, 
	cost NUMERIC, 
	leadTime NUMERIC, 
	categoryType varchar(50), 
	amount int);

--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE inventoryID START 101;
create index inventoryID_index on Inventory(inventoryid);

CREATE TABLE model (
	modelNumber int PRIMARY KEY, 
	salePrice NUMERIC, 
	inventoryID int references inventory
	on delete cascade on update cascade
);
	
--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE modelNumber START 1001;
create index modelNumber_index on model(modelNumber);

CREATE TABLE employee (
	employeeID int PRIMARY KEY, 
	FirstName varchar(25), 
	MiddleName varchar(25), 
	LastName varchar(25), 
	Salary numeric, 
	Salaried boolean, 
	Hourly boolean, 
	Department varchar(50)
);
	
--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE employeeID START 10001;
create index employeeID_index on employee(employeeID);

CREATE TABLE customer (
	customerID int PRIMARY KEY, 
	FirstName varchar(25), 
	LastName varchar(25) 
	)
;
	
--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE customerID START 1;
create index customerID_index on customer(customerID);

CREATE TABLE orders (
	orderNumber int PRIMARY KEY,
	customerID int REFERENCES customer
	on delete cascade on update cascade,
	employeeID int REFERENCES employee
	on delete cascade on update cascade,
	modelNumber int REFERENCES model
	on delete cascade on update cascade,
	saleValue money
	);

--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE orderNumber START 100001;
create index orderNumber_index on orders(orderNumber);

CREATE TABLE employeeLogin (
	userId int primary key,
	employeeID int,
	userName varchar (25),
	userRole varchar(25),
	FOREIGN KEY (employeeID) REFERENCES employee (employeeID)
	on delete cascade on update cascade
	);
create sequence userId start 1000001;
create index userId_index on employeeLogin(userID);

CREATE TABLE login (
	userName varchar(25),
	privelege varchar (25),
	loginTime timestamp,
	logoutTime timestamp
);

