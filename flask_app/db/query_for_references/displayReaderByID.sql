SELECT
  reader_id,
  reader_name,
  reader_contact_phone,
  reader_addr
FROM
  reader_info
WHERE
  reader_id = :rId;