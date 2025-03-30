from model import *

def main():
    # Создаем каталог библиотеки
    catalog = LibraryCatalog()

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

    # Выдаем книгу читателю
    loan = Loan(reader, book)

    # Пример поиска книги в каталоге
    found_book = catalog.find_by_title("Программирование на Python")
    if found_book:
        print(f"Найдена книга: {found_book}")
        print(f"Доступно экземпляров: {found_book.available_copies}")

if __name__ == "__main__":
    main()