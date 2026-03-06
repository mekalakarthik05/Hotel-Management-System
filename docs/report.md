# Project Report

This report contains the architecture and workflow diagrams for the Hotel Reservation System.

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    Room ||--o{ Reservation : "has"
    Room {
        string room_number
        int floor
        string room_type
        boolean is_available
    }
    Reservation {
        int id
        string customer_name
        string contact_number
        datetime check_in
        datetime check_out
    }
    WaitingList {
        int id
        string customer_name
        string contact_number
        string room_type
    }
```

## Class Diagram

```mermaid
classDiagram
    class Person {
        - _name: String
        - _contact: String
        + display_details(): String
    }
    
    class Customer {
        - _customer_id: String
        + display_details(): String
    }
    
    class Admin {
        - _employee_id: String
        + display_details(): String
    }
    
    Person <|-- Customer : Inherits
    Person <|-- Admin : Inherits
    
    class Room {
        - _room_number: String
        - _floor: Integer
        - _room_type: String
        - _is_available: Boolean
        + reserve_room(): Boolean
        + release_room(): void
        + display_room(): String
    }
    
    class Reservation {
        - _customer: Customer
        - _room: Room
        - _check_in: Date
        - _check_out: Date
        - _is_active: Boolean
        + create_reservation(): Boolean
        + cancel_reservation(): Boolean
        + display_reservation(): String
    }
    
    Reservation --> Customer : "has a"
    Reservation --> Room : "has a"
```

## Workflow Diagram

```mermaid
flowchart TD
    Start[Start Booking Process] --> CreateCustomer(Create Customer Object)
    CreateCustomer --> LookupRoom{Lookup Room in Dictionary}
    
    LookupRoom -->|Found & Available| CreateRes(Create Reservation Object)
    LookupRoom -->|Found & Unavailable| AddQueue(Add Customer to Queue)
    
    CreateRes --> ActiveRes[Store in Active Reservations]
    
    AddQueue --> Wait[Customer in Waiting List]
    
    Checkout[Start Checkout Process] --> ReleaseRoom(Release Room)
    ReleaseRoom --> PushHistory(Push to History Stack)
    PushHistory --> CheckQueue{Check Waiting Queue}
    
    CheckQueue -->|Queue Not Empty| Dequeue(Dequeue Next Customer)
    Dequeue --> BookNext(Book Released Room for Customer)
    CheckQueue -->|Queue Empty| End[End Checkout]
    
    BookNext --> End
```
