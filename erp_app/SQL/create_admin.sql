DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'admin') THEN

			create role admin;
		END IF;
			grant all privileges on database erp to admin;
			grant all privileges on all tables in schema public to admin;
			GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;
		

			create or replace view customerModel as 
			(select
				ord.customerID,
				cust.FirstName,
				cust.LastName,
				ord.modelNumber,
				count(ord.orderNumber) as total_number_ordered
			FROM orders ord
			inner join customer cust
				on ord.customerID = cust.customerID
			group by
				ord.customerID,
				cust.FirstName,
				cust.LastName,
				ord.modelNumber)
			;
			create or replace view expenseReport as (
				SELECT 
					cost,
					'parts' as cost_type
				FROM inventory
				union
				select
					salary as cost,
					'salary' as cost_type
				from employee
			); 
			grant select on expenseReport to admin;
			grant select on customerModel to admin;
	END
$do$;
