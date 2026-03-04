from django.core.management.base import BaseCommand
from hotel_management.models import Room

class Command(BaseCommand):
    help = 'Seeds the database with 25 rooms across 5 floors'

    def handle(self, *args, **kwargs):
        # 5 floors, 5 rooms per floor
        room_types = ['Single', 'Double', 'Suite', 'Deluxe', 'Penthouse']
        
        rooms_created = 0
        for floor in range(1, 6):
            for i in range(1, 6):
                room_number = f"{floor}0{i}"
                # Assign a room type based on index
                room_type = room_types[i - 1]
                
                # Use get_or_create to prevent duplicates if run multiple times
                room, created = Room.objects.get_or_create(
                    room_number=room_number,
                    defaults={
                        'floor': floor,
                        'room_type': room_type,
                        'is_available': True
                    }
                )
                if created:
                    rooms_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {rooms_created} new rooms.'))
