--Customer model bought and quantity to make prediction and understand trending
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
