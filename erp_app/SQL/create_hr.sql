DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'hr') THEN
		
        create role hr;
    END IF;
        grant update,select on employee to hr;
        create or replace view hrView as select
        firstName, lastName, orderNumber from
        employee join orders on 
        employee.employeeId = orders.employeeId;
        grant select on hrView to hr;
        grant select on orders to hr;

   
END
$do$;
