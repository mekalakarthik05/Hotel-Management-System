class Room:
    def __init__(self, room_number, floor, room_type, is_available=True):
        self._room_number = room_number
        self._floor = floor
        self._room_type = room_type
        self._is_available = is_available

    def reserve_room(self):
        if self._is_available:
            self._is_available = False
            return True
        return False

    def release_room(self):
        self._is_available = True

    def display_room(self):
        status = "Available" if self._is_available else "Booked"
        return f"Room {self._room_number} (Floor {self._floor}, {self._room_type}) - {status}"

    @property
    def room_number(self):
        return self._room_number

    @property
    def is_available(self):
        return self._is_available
