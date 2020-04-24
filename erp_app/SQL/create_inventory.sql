CREATE TABLE IF NOT EXISTS INVENTORY (
	inventoryID int PRIMARY KEY, 
	cost NUMERIC, 
	leadTime NUMERIC, 
	categoryType varchar(50), 
	amount int);