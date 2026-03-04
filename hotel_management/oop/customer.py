from .person import Person

# INHERITANCE: Customer inherits from the abstract base class Person
class Customer(Person):
    def __init__(self, name, contact, customer_id):
        # Constructor Usage & Inheritance: Call parent constructor
        super().__init__(name, contact)
        self._customer_id = customer_id

    # POLYMORPHISM: Method Overriding - Providing a specific implementation for Customer
    def display_details(self):
        return f"[Customer] ID: {self._customer_id}, Name: {self._name}, Contact: {self._contact}"

    @property
    def customer_id(self):
        return self._customer_id
