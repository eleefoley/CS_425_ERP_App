DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'hr') THEN
		
		create role hr;
		grant update on employee to hr;
		create view hrView as select
		firstName, lastName, orderNumber from
		employee join orders on 
		employee.employeeId = orders.employeeId;
		grant select on hrView to hr;
   END IF;
END
$do$;
