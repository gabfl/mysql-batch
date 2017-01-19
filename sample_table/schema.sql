-- Create sample table
CREATE TABLE test_update (id int AUTO_INCREMENT PRIMARY key, number float default null, date datetime default null);

-- Add 100 rows
INSERT INTO test_update (number, date)
VALUES (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null),
       (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null), (RAND(), null);
