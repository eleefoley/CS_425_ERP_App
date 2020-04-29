/*
Privileges
1- Users with admin privileges can do the following:
a. Create a new employee
b. Set up tables: order table, employee, model table for product, inventory
c. Grant access  
d. Access and create the business reporting ….

2- The sale person should be able to view:
a. View and update customer 
b. Create an Order
c. Access sales reports

3- Users with engineer privileges can do the following:
a. Access and update model
b. Access and update inventory
c. Limited view to employee information, first and last name, title ….

4- Users with HR privileges can do the following:
a. Access and update of employee information
b. View of employee and associated sales number
*/

CREATE ROLE sales;
CREATE VIEW salview AS
SELECT * FROM customer;
GRANT select on salview TO sales;
GRANT UPDATE ON customer to sales;
grant insert on orders to sales;

create role admin;
grant all privileges on database erp to admin;
grant all privileges on all tables in schema public to admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;
create view customerModel as 
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
create view expenseReport as (
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


create role engineer;
create view engineerView as 
select firstName, lastName, department
from employee;
grant select on engineerView to engineer;
grant update on model to engineer;
grant update on inventory to engineer;

create role hr;
grant update on employee to hr;
create view hrView as select
firstName, lastName, orderNumber from
employee join orders on 
employee.employeeId = orders.employeeId;
grant select on hrView to hr;

