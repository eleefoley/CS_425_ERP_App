CREATE TABLE IF NOT EXISTS customer (
	customerID int PRIMARY KEY, 
    FirstName varchar(25), 
    LastName varchar(25));
    --create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE customerID START 1;
create index customerID_index on customer(customerID);