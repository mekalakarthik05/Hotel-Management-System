from collections import deque

class WaitingListQueue:
    def __init__(self):
        self.waiting_list = deque()

    def enqueue(self, customer):
        """Add a customer to the waiting list"""
        self.waiting_list.append(customer)

    def dequeue(self):
        """Remove and return the next customer from the waiting list"""
        if self.waiting_list:
            return self.waiting_list.popleft()
        return None

    def is_empty(self):
        return len(self.waiting_list) == 0

    def get_all(self):
        return list(self.waiting_list)

# Global queue instance
waiting_queue = WaitingListQueue()
