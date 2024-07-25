# Завдання 1
# По перше додамо додатковий функціонал до класів з попередньої домашньої роботи

from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """
        Adds a new phone number to the list of phones.

        Parameters:
        - phone (str): The phone number to be added.

        Returns:
        None
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Removes a phone number from the list of phones.

        Parameters:
        - phone (str): The phone number to be removed.

        Returns:
        None
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
            """
            Edit the phone number in the contact list.

            Args:
                old_phone (str): The old phone number to be replaced.
                new_phone (str): The new phone number to replace the old one.

            Returns:
                None
            """
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

    def add_birthday(self, birthday):
        """
        Adds a birthday to the object.

        Parameters:
        - birthday: A string representing the birthday in the format 'YYYY-MM-DD'.

        Returns:
        None
        """
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
            """
            Finds a phone object with the given phone number.

            Parameters:
            phone (str): The phone number to search for.

            Returns:
            Phone or None: The phone object if found, None otherwise.
            """
            for p in self.phones:
                if p.value == phone:
                    return p
            return None

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        """
        Adds a record to the data dictionary.

        Parameters:
        - record: The record object to be added.

        Returns:
        None
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Find and return the value associated with the given name in the data dictionary.

        Parameters:
        - name (str): The name to search for in the data dictionary.

        Returns:
        - The value associated with the given name, or None if the name is not found.
        """
        return self.data.get(name, None)

    def delete(self, name):
            """
            Deletes the specified name from the data dictionary.

            Args:
                name (str): The name to be deleted.

            Returns:
                None
            """
            if name in self.data:
                del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        """
        Retrieves a list of upcoming birthdays within a specified number of days.

        Args:
            days (int): Number of days to consider for upcoming birthdays. Default is 7.

        Returns:
            list: A list of dictionaries containing the name and congratulation date of the upcoming birthdays.
                  Each dictionary has the following keys:
                  - 'name': The name of the person with an upcoming birthday.
                  - 'congratulation_date': The date of the upcoming birthday in the format "%Y.%m.%d".
        """
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        result = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_date:
                    if birthday_this_year.weekday() in (5, 6):
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                    result.append({
                        'name': record.name.value,
                        'congratulation_date': birthday_this_year.strftime("%Y.%m.%d")
                    })

        return result

if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("25.07.1990")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name.value}: {found_phone}")

    book.delete("Jane")
    for name, record in book.items():
        print(record)

    upcoming = book.get_upcoming_birthdays()
    print("Upcoming birthdays:")
    for entry in upcoming:
        print(f"{entry['name']}: {entry['congratulation_date']}")

