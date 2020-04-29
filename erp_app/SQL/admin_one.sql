select sum(orders.salevalue) as total_revenue,
employee.FirstName as emp_fname, 
employee.LastName as emp_lname, 
customer.FirstName as cust_fname, 
customer.LastName as cust_lname 
from orders 
left join employee
	on orders.employeeId = employee.employeeId 
left join customer 
	on orders.customerId = customer.customerId
group by
employee.FirstName, 
employee.LastName, 
customer.FirstName, 
customer.LastName;