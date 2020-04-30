DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'sales') THEN

        CREATE ROLE sales;
    END IF;

        CREATE or replace  VIEW salview AS(
        SELECT * FROM customer);
        GRANT select on salview TO sales;
        GRANT update,select ON customer to sales;
        grant insert, select on orders to sales;

 
END
$do$;