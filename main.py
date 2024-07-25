# Завдання 2
# Для реалізації нового функціоналу також додайте функції обробники з наступними командами

from models import AddressBook, Record

def input_error(func):
    """
    A decorator function that handles common input errors.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The decorated function.

    Raises:
    KeyError: If a key error occurs.
    ValueError: If a value error occurs.
    IndexError: If an index error occurs.
    Exception: If any other exception occurs.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return str(e)
        except ValueError as e:
            return str(e)
        except IndexError as e:
            return str(e)
        except Exception as e:
            return "An error occurred. Please try again."
    return inner

@input_error
def parse_input(user_input):
    """
    Parses the user input and returns the command and arguments.

    Args:
        user_input (str): The user input to be parsed.

    Returns:
        tuple: A tuple containing the command (str) and arguments (list).

    Example:
        >>> parse_input("add 1 2 3")
        ('add', ['1', '2', '3'])
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, book):
    """
    Add a new contact to the address book.

    Args:
        args (list): A list of two elements - name and phone.
        book (AddressBook): An address book containing existing contacts.

    Returns:
        str: A message indicating the result of the operation.
    """
    if len(args) != 2:
        raise ValueError("Invalid arguments. Usage: add [name] [phone]")
    name, phone = args
    if book.find(name):
        raise KeyError("Contact already exists.")
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    """
    Change the phone number of a contact.

    Args:
        args (list): A list of three elements - [name, old phone, new phone].
        book (AddressBook): An address book containing contact names as keys and phone numbers as values.

    Returns:
        str: A message indicating whether the contact was successfully updated or not.
    """
    if len(args) != 3:
        raise ValueError("Invalid arguments. Usage: change [name] [old phone] [new phone]")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(args, book):
    """
    Display the phone number of a contact.

    Args:
        args (list): A list of arguments. Should contain only one element, which is the name of the contact.
        book (AddressBook): An address book containing contact names as keys and phone numbers as values.

    Returns:
        str: The phone number of the contact if found, or an error message if the contact is not found.
    """
    if len(args) != 1:
        raise ValueError("Invalid arguments. Usage: phone [name]")
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(phone.value for phone in record.phones)
    else:
        raise KeyError("Contact not found.")

@input_error
def show_all(book):
    """
    Returns a formatted string representation of all contacts.

    Args:
        book (AddressBook): An address book containing contact names as keys and phone numbers as values.

    Returns:
        str: A formatted string representation of all contacts, with each contact's name and phone number separated by a colon.

    Example:
        >>> contacts = {'John': '1234567890', 'Jane': '9876543210'}
        >>> show_all(contacts)
        'John: 1234567890\nJane: 9876543210'
    """
    if not book:
        return "No contacts found."
    return "\n".join(str(record) for record in book.values())

@input_error
def add_birthday(args, book):
    """
    Add a birthday to an existing contact.

    Args:
        args (list): A list of two elements - [name, birthday].
        book (AddressBook): An address book containing existing contacts.

    Returns:
        str: A message indicating the result of the operation.
    """
    if len(args) != 2:
        raise ValueError("Invalid arguments. Usage: add-birthday [name] [birthday]")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_birthday(args, book):
    """
    Show the birthday of a contact.

    Args:
        args (list): A list containing one element - [name].
        book (AddressBook): An address book containing existing contacts.

    Returns:
        str: The birthday of the contact if found, or an error message if the contact is not found.
    """
    if len(args) != 1:
        raise ValueError("Invalid arguments. Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    else:
        raise KeyError("Contact or birthday not found.")

@input_error
def birthdays(args, book):
    """
    Show the list of users who need to be congratulated on their birthdays within the next 7 days.

    Args:
        args (list): An empty list (no arguments required).
        book (AddressBook): An address book containing existing contacts.

    Returns:
        str: A formatted string representation of contacts with upcoming birthdays.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming)

@input_error
def main():
    """
    The main function of the assistant bot program.
    """
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Available commands:")
    print("add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.")
    print("change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.")
    print("phone [ім'я]: Показати телефонні номери для вказаного контакту.")
    print("all: Показати всі контакти в адресній книзі.")
    print("add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту. Дата народження має бути у форматі DD.MM.YYYY.")
    print("show-birthday [ім'я]: Показати дату народження для вказаного контакту.")
    print("birthdays: Показати дні народження, які відбудуться протягом наступного тижня.")
    print("hello: Отримати вітання від бота.")
    print("close або exit: Закрити програму.")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()