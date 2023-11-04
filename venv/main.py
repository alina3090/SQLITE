import sqlite3
import pandas as pd


con = sqlite3.connect("library.db")
print('задание 1')
df1 = pd.read_sql('''
    SELECT book.title AS "Название",
        reader.reader_name AS "Читатель",
        (julianday(book_reader.return_date) - julianday(book_reader.borrow_date)) AS "Количество дней"
    FROM book_reader, reader, book
    WHERE (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) + 1 > 14 
        AND reader.reader_id = book_reader.reader_id
        AND book.book_id = book_reader.book_id)
    ORDER BY book.title ASC, 3, reader.reader_name ASC;                  
''', con)
print(df1)
print('\n')

print('задание 2')
df2 = pd.read_sql('''
    SELECT book.title AS "Книга",
       author.author_name AS "Авторы",
       genre.genre_name AS "Жанр",
       publisher.publisher_name AS "Издательство",
       book.available_numbers + (SELECT COUNT(book_reader.book_id)
                                     FROM book_reader
                                     GROUP BY book_reader.book_id) AS "Количество"
FROM book
JOIN genre 
ON book.genre_id = genre.genre_id
JOIN publisher
ON publisher.publisher_id = book.publisher_id
JOIN book_author
ON book.book_id = book_author.book_id
JOIN author
On book_author.author_id = author.author_id
ORDER BY book.title, author.author_name;                  
''', con)
print(df2)
print('\n')

print('задание 3')
df3 = pd.read_sql('''
   SELECT genre.genre_name AS "Жанр",
       book.title AS "Название",
       MAX(book.available_numbers) AS "Доступное количество"
    FROM genre, book
    WHERE genre.genre_id = book.genre_id
    GROUP BY genre.genre_name;                 
''', con)
print(df3)
print('\n')

print('задание 4')

df4 = pd.read_sql_query('''
DROP TABLE if EXISTS rating;
CREATE TABLE if NOT EXISTS rating (
  reader_name VARCHAR(30),
  rating_reader INT
);

INSERT INTO rating 
SELECT reader.reader_name, 
       SUM(
           CASE 
              WHEN book_reader.return_date IS NULL THEN 1	
              WHEN book_reader.return_date - book_reader.borrow_date < 14 THEN 5
              WHEN book_reader.return_date - book_reader.borrow_date BETWEEN 14 AND 30 THEN 2
              ELSE -2
          END) AS rating_reader
 FROM reader, book_reader
 WHERE reader.reader_id = book_reader.reader_id
 GROUP BY reader.reader_name;

SELECT * FROM rating;
''', con)
print(df4)
print('\n')

print('задание 5')
df5 = pd.read_sql('''
   SELECT book.title AS 'Название',
       COUNT(book_reader.book_id) AS 'Количество',
       MIN( julianday(book_reader.return_date) - julianday(book_reader.borrow_date)) AS 'Минимальный_период'
FROM book
LEFT JOIN book_reader ON book.book_id = book_reader.book_id
WHERE book_reader.book_id IS NOT NULL and return_date IS NOT NULL
GROUP BY book.book_id, book.title
HAVING COUNT(book_reader.book_id) > 1
ORDER BY 3, 1;                 
''', con)
print(df5)
print('\n')












