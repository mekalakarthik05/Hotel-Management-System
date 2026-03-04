from .person import Person

# INHERITANCE: Admin inherits from the abstract base class Person
class Admin(Person):
    def __init__(self, name, contact, employee_id):
        # Constructor Usage & Inheritance: Call parent constructor
        super().__init__(name, contact)
        self._employee_id = employee_id

    # POLYMORPHISM: Method Overriding - Providing a specific implementation for Admin
    def display_details(self):
        return f"[Admin] Emp ID: {self._employee_id}, Name: {self._name}, Contact: {self._contact}"

    @property
    def employee_id(self):
        return self._employee_id
