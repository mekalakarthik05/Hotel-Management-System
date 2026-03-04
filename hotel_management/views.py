from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
import uuid

# Import Data Structures and OOP Classes
from .datastructures.room_manager import room_manager
from .datastructures.queue_manager import waiting_queue
from .datastructures.stack_manager import history_stack
from .oop.customer import Customer
from .oop.reservation import Reservation as OOPReservation

# Import Database Models
from .models import Room, Reservation, WaitingList

def home(request):
    # Load stats from DB
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    reserved_rooms = total_rooms - available_rooms
    waiting_count = WaitingList.objects.count()

    # Load active reservations from DB to display
    active_reservations = Reservation.objects.filter(check_out__isnull=True).order_by('-created_at')

    return render(request, 'hotel_management/home.html', {
        'active_reservations': active_reservations,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'reserved_rooms': reserved_rooms,
        'waiting_count': waiting_count
    })

def available_rooms(request):
    # Filter functionality
    floor_filter = request.GET.get('floor')
    type_filter = request.GET.get('type')

    db_rooms = Room.objects.all()
    if floor_filter:
        db_rooms = db_rooms.filter(floor=floor_filter)
    if type_filter:
        db_rooms = db_rooms.filter(room_type__icontains=type_filter)

    # Dictionary Usage: We load these rooms into our Dictionary for fast lookup simulation
    # Even though DB exists, requirement is to use the Dictionary
    for r in db_rooms:
        room_manager.rooms[str(r.room_number)] = r

    rooms = room_manager.get_all_rooms()

    return render(request, 'hotel_management/available_rooms.html', {
        'rooms': rooms
    })

def book_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        room_number = request.POST.get('room_number')
        
        # Load all DB rooms into Dict to find the specific one
        for r in Room.objects.all():
            room_manager.rooms[str(r.room_number)] = r

        # Find room in Dictionary O(1)
        room_obj = room_manager.get_room(room_number)
        
        if room_obj:
            if room_obj.is_available:
                # DB Update: Allocate room, update status
                room_obj.is_available = False
                room_obj.save()

                # Save reservation to DB
                Reservation.objects.create(
                    customer_name=name,
                    contact_number=contact,
                    room=room_obj,
                    check_in=timezone.now()
                )
                return redirect('home')
            else:
                # Room unavailable, add to waiting list Queue and DB
                customer_id = str(uuid.uuid4())[:8]
                customer = Customer(name, contact, customer_id)
                
                # Queue usage
                waiting_queue.enqueue(customer)

                # Save to DB
                WaitingList.objects.create(
                    customer_name=name,
                    contact_number=contact,
                    room_type=room_obj.room_type
                )
                return redirect('waiting_list')
    
    # Load available rooms for dropdown
    available = Room.objects.filter(is_available=True)
    return render(request, 'hotel_management/book_room.html', {'available_rooms': available})

def checkout_room(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        
        try:
            # Find the active reservation in DB
            res = Reservation.objects.get(id=reservation_id, check_out__isnull=True)
            
            # Checkout logic
            res.check_out = timezone.now()
            res.save()

            room_obj = res.room
            
            # Check waiting list in DB (Load into Queue first to fulfill requirement)
            waiting_db = list(WaitingList.objects.filter(room_type=room_obj.room_type).order_by('requested_date'))
            
            # Enqueue to our memory queue
            for w in waiting_db:
                waiting_queue.enqueue(w)

            # Dequeue the first waiting customer
            if not waiting_queue.is_empty():
                next_customer = waiting_queue.dequeue()
                
                # Allocate room to next customer
                Reservation.objects.create(
                    customer_name=next_customer.customer_name,
                    contact_number=next_customer.contact_number,
                    room=room_obj,
                    check_in=timezone.now()
                )
                # Remove from DB waiting list
                WaitingList.objects.filter(id=next_customer.id).delete()
            else:
                # Release room if no one is waiting
                room_obj.is_available = True
                room_obj.save()

        except Reservation.DoesNotExist:
            pass

    return redirect('home')

def view_waiting_list(request):
    # Load from DB to simulate persistent Queue state
    db_waiting = WaitingList.objects.all().order_by('requested_date')
    
    # Empty existing queue to prevent memory leak across requests during dev
    while not waiting_queue.is_empty():
         waiting_queue.dequeue()

    for w in db_waiting:
        waiting_queue.enqueue(w)

    return render(request, 'hotel_management/waiting_list.html', {
        'waiting_list': waiting_queue.get_all()
    })

def view_history(request):
    # Load history from DB (reservations with check_out)
    db_history = Reservation.objects.filter(check_out__isnull=False).order_by('check_out')
    
    # Clear existing memory stack
    history_stack.reservation_history = []
    
    # Stack Usage: Push all history items
    for h in db_history:
        history_stack.push(h)
        
    return render(request, 'hotel_management/history.html', {
        'history': history_stack.get_all()
    })

def search_reservation(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Search by customer name or contact number
        results = Reservation.objects.filter(
            Q(customer_name__icontains=query) | Q(contact_number__icontains=query)
        ).order_by('-created_at')

    return render(request, 'hotel_management/search.html', {
        'results': results,
        'query': query
    })
