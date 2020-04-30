CREATE TABLE IF NOT EXISTS INVENTORY (
	inventoryID int PRIMARY key NOT NULL CHECK (inventoryID >= 0), 
	cost numeric NOT NULL CHECK (cost >= 0), 
	leadTime numeric NOT NULL CHECK (leadTime >= 0), 
	categoryType varchar(50), 
	amount int NOT NULL CHECK (amount >= 0));
CREATE SEQUENCE IF NOT EXISTS inventoryID START 101;
create index IF NOT EXISTS inventoryID_index on Inventory(inventoryid);