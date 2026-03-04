from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    room_type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation: {self.customer_name} in Room {self.room.room_number}"

class WaitingList(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=50)
    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Waiting: {self.customer_name} for {self.room_type}"
