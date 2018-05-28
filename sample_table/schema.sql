-- Drop the table if it exists
DROP TABLE IF EXISTS batch_test;

-- Create sample table
CREATE TABLE batch_test (id int AUTO_INCREMENT PRIMARY key, number float default null, date datetime default null);

-- Add 100 rows
INSERT INTO batch_test (number, date)
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
