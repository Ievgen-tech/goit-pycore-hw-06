"""Address book management system.

This module implements a contact management system with classes for
storing and managing contacts with their phone numbers.
"""
from collections import UserDict


class Field:
    """Base class for contact record fields."""

    def __init__(self, value: str) -> None:
        self._value: str = ""
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)

class Name(Field):
    """Class for storing contact name. Required field."""

class Phone(Field):
    """Class for storing phone number with validation (10 digits)."""

    @staticmethod
    def validate_phone(number: str) -> None:
        if not number.isdigit() or len(number) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")

    @Field.value.setter
    def value(self, new_value: str) -> None:
        # Validation via dedicated method
        self.validate_phone(new_value)
        self._value = new_value


class Record:
    """Class for storing contact information."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        # Find the phone number and update it (Phone.value validation will apply)
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict[str, Record]):
    """Class for storing records and managing them."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

# --- Test block with sample data ---
if __name__ == "__main__":
    # Create a new address book
    book = AddressBook()

    # Create a record for Andriy
    andriy_record = Record("Andriy")
    andriy_record.add_phone("0981234567")
    andriy_record.add_phone("0509876543")

    # Add Andriy record to the address book
    book.add_record(andriy_record)

    # Create and add a new record for Maria
    maria_record = Record("Maria")
    maria_record.add_phone("0675554433")
    book.add_record(maria_record)

    # Print all records in the book
    print("--- All contacts in the address book ---")
    for contact_name, contact_record in book.data.items():
        print(contact_record)

    # Find and edit Andriy's phone number
    # Change 0981234567 to 0631112233
    andriy = book.find("Andriy")
    if andriy:
        andriy.edit_phone("0981234567", "0631112233")
        print("\n--- Andriy after phone edit ---")
        print(andriy)

        # Search for a specific phone number in Andriy's record
        found_phone = andriy.find_phone("0509876543")
        print(f"\nFound phone in {andriy.name}: {found_phone}")

    # Delete Maria's record
    book.delete("Maria")

    print("\n--- Address book after deleting Maria ---")
    for contact_name, contact_record in book.data.items():
        print(contact_record)