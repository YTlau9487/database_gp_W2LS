SELECT EXISTS (
  SELECT 1
  FROM
    reader_info
  WHERE
    reader_id = :rId
  ) AS is_recorded;