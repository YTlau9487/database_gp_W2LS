-- find all details of a book by ISBN 
SELECT b.book_id AS BookID, b.isbn AS ISBN, b.book_title AS BookTitle,
a.author_name AS AuthorName, 
c.category_name AS Catagory, 
p.publisher_name AS PublisherName
l.loc_district AS Location, l.book_shelf AS BookShelf, l.shelf_level AS ShelfLevel

FROM books b

JOIN publisher p ON b.publisher_id = p.publisher_id
JOIN catagory c ON c.catagory_id = b.catagory_id  
JOIN books_location bl ON b.book_id = bl.book_id
JOIN location l ON bl.loc_id = l.loc_id
JOIN book_author ba ON b.book_id = ba.book_id
JOIN author_info a ON b.author_id = a.author_id

WHERE b.isbn = :isbn 
AND bl.book_status = 'O';