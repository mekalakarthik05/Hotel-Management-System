from hotel_management.oop.room import Room

class RoomManager:
    def __init__(self):
        # Using a Dictionary for fast room lookup
        self.rooms = {}
        self._initialize_rooms()

    def _initialize_rooms(self):
        """Initialize some default rooms"""
        self.rooms["101"] = Room("101", 1, "Single")
        self.rooms["102"] = Room("102", 1, "Double")
        self.rooms["201"] = Room("201", 2, "Suite")
        self.rooms["202"] = Room("202", 2, "Double")
        self.rooms["301"] = Room("301", 3, "Penthouse")

    def get_room(self, room_number):
        """Lookup room in dictionary O(1)"""
        return self.rooms.get(str(room_number))

    def get_all_rooms(self):
        return self.rooms.values()

    def get_available_rooms(self):
        return [room for room in self.rooms.values() if room.is_available]

# Global room manager instance
room_manager = RoomManager()
