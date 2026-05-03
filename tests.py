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

    # =============================================
    # Ниже — мои тесты с улучшенным дизайном
    # =============================================

    @pytest.fixture
    def collector(self):
        """Фикстура возвращает новый экземпляр BooksCollector для каждого теста."""
        return BooksCollector()

    # -- add_new_book --
    @pytest.mark.parametrize("name, expected_len", [
        ('', 0),
        ('А' * 40, 1),
        ('А' * 41, 0),
    ])
    def test_add_new_book_length_constraints(self, collector, name, expected_len):
        """Граничные значения длины названия книги."""
        collector.add_new_book(name)
        assert len(collector.get_books_genre()) == expected_len

    def test_add_new_book_no_duplicates(self, collector):
        """Повторное добавление той же книги игнорируется."""
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.get_books_genre()) == 1

    # -- set_book_genre --
    def test_set_book_genre_valid(self, collector):
        """Книге можно задать жанр из разрешённого списка."""
        # Подготавливаем книгу напрямую, не через add_new_book
        collector.books_genre['Гиперион'] = ''
        collector.set_book_genre('Гиперион', 'Фантастика')
        # Проверяем, что жанр установлен, используя прямой доступ
        assert collector.books_genre['Гиперион'] == 'Фантастика'

    # -- get_book_genre --
    def test_get_book_genre_positive(self, collector):
        """Позитивный тест: возвращается установленный жанр."""
        # Подготавливаем книгу с жанром напрямую
        collector.books_genre['Детская книга'] = 'Фантастика'
        assert collector.get_book_genre('Детская книга') == 'Фантастика'

    def test_get_book_genre_empty_for_book_without_genre(self, collector):
        """Для книги без жанра возвращается пустая строка."""
        collector.books_genre['Неизвестный жанр'] = ''
        assert collector.get_book_genre('Неизвестный жанр') == ''

    def test_get_book_genre_none_for_nonexistent_book(self, collector):
        """Для несуществующей книги возвращается None."""
        assert collector.get_book_genre('Вымышленная книга') is None

    # -- get_books_with_specific_genre --
    @pytest.mark.parametrize("initial_books, genre, expected", [
        ({'Книга1': 'Ужасы', 'Книга2': 'Ужасы'}, 'Ужасы', ['Книга1', 'Книга2']),
        ({'Одинокая': 'Комедии'}, 'Ужасы', []),
        ({}, 'Детективы', []),
    ])
    def test_get_books_with_specific_genre(self, collector, initial_books, genre, expected):
        """Поиск книг по жанру: найдены / не найдены / библиотека пуста."""
        # Подготавливаем словарь напрямую
        collector.books_genre = initial_books
        result = collector.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(expected)

    # -- get_books_genre --
    def test_get_books_genre_returns_dict(self, collector):
        """Метод возвращает актуальный словарь книг и жанров."""
        collector.books_genre = {'Война и мир': 'Комедии'}
        assert collector.get_books_genre() == {'Война и мир': 'Комедии'}

    # -- get_books_for_children --
    def test_get_books_for_children_excludes_age_rating(self, collector):
        """Детские книги не содержат жанры с возрастным рейтингом и книги без жанра."""
        collector.books_genre = {
            'Детская энциклопедия': 'Фантастика',
            'Ужастик': 'Ужасы',
            'Без жанра': ''
        }
        children = collector.get_books_for_children()
        assert 'Детская энциклопедия' in children
        assert 'Ужастик' not in children
        assert 'Без жанра' not in children

    # -- add_book_in_favorites --
    def test_add_book_in_favorites_positive(self, collector):
        """Позитивный тест: книга добавляется в избранное (однократный вызов)."""
        collector.books_genre['Мастер и Маргарита'] = ''
        collector.add_book_in_favorites('Мастер и Маргарита')
        assert collector.favorites == ['Мастер и Маргарита']

    def test_add_book_in_favorites_duplicate_ignored(self, collector):
        """Повторное добавление той же книги в избранное игнорируется."""
        collector.books_genre['Мастер и Маргарита'] = ''
        collector.add_book_in_favorites('Мастер и Маргарита')
        collector.add_book_in_favorites('Мастер и Маргарита')
        assert collector.favorites == ['Мастер и Маргарита']

    def test_add_favorite_not_in_books(self, collector):
        """Если книги нет в books_genre, она не добавляется в избранное."""
        collector.add_book_in_favorites('Призрак')
        assert collector.favorites == []

    # -- delete_book_from_favorites --
    def test_delete_book_from_favorites_positive(self, collector):
        """Удаление существующей книги из избранного делает список пустым."""
        collector.favorites = ['Три товарища']
        collector.delete_book_from_favorites('Три товарища')
        assert collector.favorites == []

    def test_delete_book_from_favorites_twice_does_not_raise(self, collector):
        """Повторное удаление уже удалённой книги не вызывает ошибок."""
        collector.favorites = ['Три товарища']
        collector.delete_book_from_favorites('Три товарища')
        collector.delete_book_from_favorites('Три товарища')
        assert collector.favorites == []

    # -- get_list_of_favorites_books --
    def test_get_list_of_favorites_books_after_additions(self, collector):
        """Список избранного корректно возвращает все добавленные книги."""
        collector.favorites = ['А', 'Б']
        assert collector.get_list_of_favorites_books() == ['А', 'Б']