-- Write a SQL script that ranks country origins of bands,
-- ordered by the number of (non-unique) fans
-- Import this table dump: https://github.com/lahincapie/holbertonschool-backend-storage/blob/master/0x00-MySQL_Advanced/metal_bands.sql
-- Column names must be: origin and nb_fans
-- Your script can be executed on any database
-- Context: Calculate/compute something is always
-- power intensive… better to distribute the load!

SELECT origin, sum(fans) as nb_fans
    FROM metal_bands
    group by origin
    ORDER BY nb_fans DESC;
