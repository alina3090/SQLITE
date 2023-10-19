import sqlite3
import pandas as pd


connection = sqlite3.connect("library.db")
print('задание 1')
df = pd.read_sql('''
    SELECT book.title AS "Название",
        reader.reader_name AS "Читатель",
        (julianday(book_reader.return_date) - julianday(book_reader.borrow_date)) AS "Количество дней"
    FROM book_reader, reader, book
    WHERE (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) + 1 > 14 
        AND reader.reader_id = book_reader.reader_id
        AND book.book_id = book_reader.book_id)
    ORDER BY book.title ASC, 3, reader.reader_name ASC;                  
''', connection)
# print(df)
print('\n')

print('задание 2')                                      # перечисление авторов
cursor = connection.cursor()
cursor.execute('''    
    SELECT book.title AS "Книга",
           author.author_name AS "Авторы",
           genre.genre_name AS "Жанр",
           publisher.publisher_name AS "Издательство",
           book.available_numbers + (SELECT COUNT(book_reader.book_id)
                                     FROM book_reader
                                     GROUP BY book_reader.book_id) AS "Количество"
    FROM book, author, genre, publisher
    ORDER BY book.title, author.author_name;
''')
for e in cursor.fetchall():
    print(e, end="\n")
cursor.close()
print('\n')



