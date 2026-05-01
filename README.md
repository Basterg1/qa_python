
Реализованные тесты
№	Тест	Что проверяет
1	test_add_new_book_add_two_books	Добавление двух книг (исправленный пример из шаблона)
2	test_add_new_book_empty_name_not_added	Пустое название не добавляется
3	test_add_new_book_max_length_name_added	Название длиной 40 символов добавляется
4	test_add_new_book_over_max_length_not_added	Название длиной 41 символ не добавляется
5	test_add_new_book_no_duplicates	Повторное добавление той же книги игнорируется
6	test_set_book_genre_valid	Книге присваивается жанр из разрешённого списка
7	test_get_book_genre_not_set_and_nonexistent	Для книги без жанра возвращается '', для неизвестной — None
8	test_get_books_with_specific_genre	Параметризованный тест: поиск книг по жанру (найдены/не найдены/пустой словарь)
9	test_get_books_genre_returns_dict	Метод возвращает актуальный словарь книг с жанрами
10	test_get_books_for_children_excludes_age_rating	Детские книги не содержат жанры с возрастным рейтингом и книги без жанра
11	test_add_book_in_favorites_no_duplicates	Книгу можно добавить в избранное только один раз
12	test_add_favorite_not_in_books	Книга, отсутствующая в books_genre, не добавляется в избранное
13	test_delete_book_from_favorites	Удаление книги из избранного, повторное удаление не вызывает ошибок
14	test_get_list_of_favorites_books	Список избранных книг содержит все добавленные позиции