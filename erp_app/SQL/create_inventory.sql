CREATE TABLE IF NOT EXISTS INVENTORY (
	inventoryID int PRIMARY KEY, 
	cost NUMERIC, 
	leadTime NUMERIC, 
	categoryType varchar(50), 
	amount int);
CREATE SEQUENCE IF NOT EXISTS inventoryID START 101;
create index IF NOT EXISTS inventoryID_index on Inventory(inventoryid);