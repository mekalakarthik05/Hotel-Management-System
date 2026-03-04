class ReservationHistoryStack:
    def __init__(self):
        self.reservation_history = []

    def push(self, reservation):
        """Add a completed/cancelled reservation to the history"""
        self.reservation_history.append(reservation)

    def pop(self):
        """Remove and return the most recently completed reservation"""
        if self.reservation_history:
            return self.reservation_history.pop()
        return None

    def get_all(self):
        # Return reversed so latest is first
        return list(reversed(self.reservation_history))

# Global stack instance
history_stack = ReservationHistoryStack()
