from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Номер повинен містити 10 цифр")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Невірний формат. Правильно: день.місяць.рік")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Номер не знайдено!")
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Номер не знайдено!")
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Даних немає"
        return f"Імʼя контакту: {self.name.value}, номер: {phones}, день нарождення: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def find(self, name):
        return self.data.get(name)
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value.date()
                birthday_this_year = birthday_date.replace(year=today.year)
                
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                days_until = (birthday_this_year - today).days
                
                if 0 <= days_until <= 7:
                    weekday = birthday_this_year.weekday()

                    if weekday == 5:
                        birthday_this_year += timedelta(days=2)
                    elif weekday == 6:
                        birthday_this_year += timedelta(days=1)
                    upcoming.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y")
                    })
        return upcoming

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Контакт не знайдено!"
        except IndexError:
            return "Введіть значення"
    return inner

def parse_input(user_input):
    parts = user_input.split()
    command = parts[0].strip().lower()
    args = parts[1:]
    return command, *args

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Контакт оновлено!"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано!"
    
    if phone:
        record.add_phone(phone)
    
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Контакт оновлено!"
    else:
        raise KeyError

@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return f"{name}: {phones}"
    else:
        raise KeyError

def show_all(book):
    if not book.data:
        return "Контактів немає"
    result = ""
    for record in book.data.values():
        result += str(record) + "\n"
    return result.strip()

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)  
    if record:
        record.add_birthday(birthday)
        return "Дата нарождення додана"
    else:
        raise KeyError

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        if record.birthday:
            birthday_str = record.birthday.value.strftime("%d.%m.%Y")
            return f"{name} день народження: {birthday_str}"
        else:
            return f"{name} не встановив/ла дату нарождення"
    else:
        raise KeyError
    
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Наступного тижня немає днів нарождення"
    result = "Майбутні дні нарождення:\n"
    for item in upcoming:
        result += f"{item['name']}: {item['birthday']}\n"
    
    return result.strip()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            save_data(book)
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
            print(birthdays(book))
        
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()