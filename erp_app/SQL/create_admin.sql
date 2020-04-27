DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'admin') THEN

	  create role admin;
      grant all privileges on database erp to admin;
   END IF;
END
$do$;
