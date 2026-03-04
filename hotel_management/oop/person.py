class Person:
    # ABSTRACTION: This base class provides a template for all people in the system.
    def __init__(self, name, contact):
        # ENCAPSULATION: Using private variables (denoted by '_') to hide internal state
        self._name = name
        self._contact = contact

    def display_details(self):
        """Method to be overridden by subclasses"""
        return f"Name: {self._name}, Contact: {self._contact}"

    @property
    def name(self):
        return self._name

    @property
    def contact(self):
        return self._contact
