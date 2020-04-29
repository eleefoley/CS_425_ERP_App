DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'engineer') THEN
		
		create role engineer;
		create view engineerView as 
		select firstName, lastName, department
		from employee;
		grant select on engineerView to engineer;
		grant update on model to engineer;
		grant update on inventory to engineer;
   END IF;
END
$do$;
