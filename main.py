from model import *
from domain import *

def main():
    # Инициализируем сервис хранения данных
    storage_service = StorageService()
    
    # Создаем менеджер читателей и каталог библиотеки с общим хранилищем
    reader_manager = ReaderManager(storage_service)
    catalog = LibraryCatalog(storage_service)

    # Создаем книгу
    book = Book(
        title="Программирование на Python",
        authors=["Марк Лутц"],
        library_code="PY001",
        year=2019,
        publisher="O'Reilly",
        total_copies=5
    )
    catalog.add_book(book)

    # Создаем читателя
    reader = Reader(
        full_name="Иванов Иван Иванович",
        ticket_number="ST001",
        category="Студент"
    )

    reader_manager.register_reader(reader)
    # Выдаем книгу читателю
    loan = Loan(reader, book)

    # Пример поиска книги в каталоге
    found_book = catalog.find_by_title("Программирование на Python")
    if found_book:
        print(f"Найдена книга: {found_book}")
        print(f"Доступно экземпляров: {found_book.available_copies}")

if __name__ == "__main__":
    main()