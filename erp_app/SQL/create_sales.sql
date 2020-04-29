DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_roles
      WHERE  rolname = 'sales') THEN

      CREATE ROLE sales;
      create view salview as
      SELECT * FROM customer;
      GRANT select on salview TO sales;
      GRANT UPDATE ON customer to sales;
      grant insert on orders to sales;
   END IF;
END
$do$;