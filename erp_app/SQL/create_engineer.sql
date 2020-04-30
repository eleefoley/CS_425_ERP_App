DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'engineer') THEN
		
		create role engineer;
    END IF;
        create or replace view engineerView as 
        select firstName, lastName, department
        from employee;
        grant select on engineerView to engineer;
        grant update,select on model to engineer;
        grant update,select on inventory to engineer;
   
END
$do$;
