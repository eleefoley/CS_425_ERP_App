--Expense report, employee showing salary, bonus expense and part cost
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
) 