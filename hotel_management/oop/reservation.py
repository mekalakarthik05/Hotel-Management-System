class Reservation:
    def __init__(self, customer, room, check_in, check_out):
        self._customer = customer
        self._room = room
        self._check_in = check_in
        self._check_out = check_out
        self._is_active = False

    def create_reservation(self):
        if self._room.reserve_room():
            self._is_active = True
            return True
        return False

    def cancel_reservation(self):
        if self._is_active:
            self._room.release_room()
            self._is_active = False
            return True
        return False

    def display_reservation(self):
        status = "Active" if self._is_active else "Cancelled/Completed"
        return f"Reservation: {self._customer.name} in Room {self._room.room_number} ({self._check_in} to {self._check_out}) - {status}"

    @property
    def customer(self):
        return self._customer

    @property
    def room(self):
        return self._room

    @property
    def is_active(self):
        return self._is_active
