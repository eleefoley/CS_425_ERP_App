select 
orders.ordernumber as order_no,
model.modelNumber as model_no,
inventory.amount as avail_inv
from orders
left join model
	on orders.modelnumber = model.modelnumber
left join inventory 
	on model.inventoryid = inventory.inventoryid;
	
drop table employeelogin;
drop table login;