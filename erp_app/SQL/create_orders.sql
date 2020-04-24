CREATE TABLE IF NOT EXISTS orders (	
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
