from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    # --- add_new_book: границы и дубли ---
    def test_add_new_book_empty_name_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('')
        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_max_length_name_added(self):
        collector = BooksCollector()
        collector.add_new_book('А' * 40)
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_over_max_length_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('А' * 41)
        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_no_duplicates(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.get_books_genre()) == 1

    # --- set_book_genre / get_book_genre ---
    def test_set_book_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book('Гиперион')
        collector.set_book_genre('Гиперион', 'Фантастика')
        assert collector.get_book_genre('Гиперион') == 'Фантастика'

    def test_get_book_genre_not_set_and_nonexistent(self):
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        assert collector.get_book_genre('Шерлок Холмс') == ''
        assert collector.get_book_genre('Неизвестная книга') is None

    # --- get_books_with_specific_genre (параметризация) ---
    @pytest.mark.parametrize("books_data, genre, expected", [
        ([("Книга1", "Ужасы"), ("Книга2", "Ужасы")], "Ужасы", ["Книга1", "Книга2"]),
        ([("Одинокая", "Комедии")], "Ужасы", []),
        ([], "Детективы", []),
    ])
    def test_get_books_with_specific_genre(self, books_data, genre, expected):
        collector = BooksCollector()
        for name, book_genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, book_genre)
        result = collector.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(expected)

    # --- get_books_genre ---
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Война и мир')
        collector.set_book_genre('Война и мир', 'Комедии')
        expected = {'Война и мир': 'Комедии'}
        assert collector.get_books_genre() == expected

    # --- get_books_for_children ---
    def test_get_books_for_children_excludes_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book('Детская энциклопедия')
        collector.set_book_genre('Детская энциклопедия', 'Фантастика')
        collector.add_new_book('Ужастик')
        collector.set_book_genre('Ужастик', 'Ужасы')
        collector.add_new_book('Без жанра')
        children = collector.get_books_for_children()
        assert 'Детская энциклопедия' in children
        assert 'Ужастик' not in children
        assert 'Без жанра' not in children

    # --- избранное ---
    def test_add_book_in_favorites_no_duplicates(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')
        collector.add_book_in_favorites('Мастер и Маргарита')
        collector.add_book_in_favorites('Мастер и Маргарита')
        assert collector.get_list_of_favorites_books() == ['Мастер и Маргарита']

    def test_add_favorite_not_in_books(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Призрак')
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Три товарища')
        collector.add_book_in_favorites('Три товарища')
        collector.delete_book_from_favorites('Три товарища')
        assert collector.get_list_of_favorites_books() == []
        collector.delete_book_from_favorites('Три товарища')  # не ломается

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book('А')
        collector.add_new_book('Б')
        collector.add_book_in_favorites('А')
        collector.add_book_in_favorites('Б')
        assert sorted(collector.get_list_of_favorites_books()) == ['А', 'Б']