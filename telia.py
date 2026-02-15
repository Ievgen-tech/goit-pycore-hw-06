"""Address book management system.

This module implements a contact management system with classes for
storing and managing contacts with their phone numbers.
"""

from collections import UserDict
from typing import Optional


class Field:
    """Base class for contact record fields."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""


class Phone(Field):
    """Class for storing phone number with validation (10 digits)."""

    def __init__(self, value: str) -> None:
        # Validation: check that the value contains exactly 10 digits
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Record:
    """Class for storing contact information."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Add a phone number to the record."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the record."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit a phone number in the record."""
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number {old_phone} not found in the record")

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find a phone number in the record."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Class for storing records and managing them."""

    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Find a record by name."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete a record by name."""
        if name in self.data:
            del self.data[name]


# Example usage and testing
if __name__ == "__main__":
    # Create a new address book
    address_book = AddressBook()

    # Create a record for Michael
    michael_record = Record("Michael")
    michael_record.add_phone("3805551234")
    michael_record.add_phone("3805559876")

    # Add Michael's record to the address book
    address_book.add_record(michael_record)

    # Create and add a new record for Sarah
    sarah_record = Record("Sarah")
    sarah_record.add_phone("3805553210")
    address_book.add_record(sarah_record)

    # Display all records in the book
    print("All contacts in the address book:")
    for contact_name, contact_record in address_book.data.items():
        print(contact_record)

    # Find and edit Michael's phone number
    michael = address_book.find("Michael")
    if michael:
        michael.edit_phone("3805551234", "3805552222")

        print("\nAfter editing Michael's phone:")
        print(michael)

        # Search for a specific phone number in Michael's record
        found_phone = michael.find_phone("3805559876")
        print(f"\nFound phone for {michael.name}: {found_phone}")

    # Delete Sarah's record
    address_book.delete("Sarah")

    print("\nAfter deleting Sarah:")
    for contact_name, contact_record in address_book.data.items():
        print(contact_record)
