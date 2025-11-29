INSERT INTO loan_records     
VALUES (1+COUNT(*), :rid, :blid, CURDATE(), CURDATE() + INTERVAL 14 DAY, NULL);

