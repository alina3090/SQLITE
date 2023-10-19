SELECT book.title AS "Книга",
           author.author_name AS "Авторы",
           genre.genre_name AS "Жанр"
           publisher.publisher_name AS "Издательство"
           COUNT() AS "Количество"
    FROM book, author, genre, publisher
    WHERE COUNT=(book.available_number) AND book.book_id = book_reader.book_id AND return_date = NULL);