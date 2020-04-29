CREATE TABLE IF NOT EXISTS model (
	modelNumber int PRIMARY KEY, 
	salePrice NUMERIC, 
	inventoryID int references inventory 
	on delete cascade on update cascade);
	--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
CREATE SEQUENCE IF NOT EXISTS modelNumber START 1001;
create index IF NOT EXISTS modelNumber_index on model(modelNumber);