from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, number):
        self.value = self.validate_number(number)

    def validate_number(self, number):
        if len(number) != 10:
            raise ValueError("Phone number must contain 10 digits")
        if not number.isdigit():
            raise ValueError("Phone number must contain only numbers")
        return number

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, number: str):
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        self.phones = list(filter(lambda phone: phone == number, self.phones))

    def edit_phone(self, old_phone: str, new_phone: str):
         for i, phone in enumerate(self.phones):
             if phone.value == old_phone:
                 self.phones[i] = Phone(new_phone)
                 return
             raise ValueError(f"Phone '{old_phone}' not found for contact '{self.name.value}'.")

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name):
        record = self.data.get(name, None)
        if record is None:
            raise KeyError(f"Record with name '{name}' not found.")
        return record

    def delete(self, name):
        if name not in self.data:
            raise KeyError(f"Record with name '{name}' not found.")
        del self.data[name]


# Приклад використання

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведе: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведе: 5555555555

# Видалення запису Jane
book.delete("Jane")