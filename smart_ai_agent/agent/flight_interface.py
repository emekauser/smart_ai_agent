import random
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from api.models import FlightTicket

def get_pnr():
    middle_part=random.randint(100, 999)
    return f"FL{middle_part}N"

def get_arrival_time(date_string):
    format_code = "%Y-%m-%d %H:%M"

    datetime_object = datetime.strptime(date_string, format_code)
    later_datetime = datetime_object + timedelta(minutes=60)
    return later_datetime

def book_flight_db(user: User, flight_data: dict)-> dict:
    flight_ticket = FlightTicket.objects.create(
         departure= flight_data.get("departure"),
         arrival= flight_data.get("arrival"),
         departure_time= flight_data.get("departure_time"),
         arrival_time= get_arrival_time(flight_data.get("departure_time")),
         ticket_number= random.randint(1000000, 9999999),
         seat_number=  random.randint(1, 180),
         is_used= False,
         is_cancelled= False,
         pnr= get_pnr(),
         user= user
    )
    return {
            "arrival": flight_ticket.arrival,
            "departure": flight_ticket.departure,
            "arrival_time": flight_ticket.arrival_time,
            "departure_time": flight_ticket.departure_time,
            "seat_number": flight_ticket.seat_number,
            "pnr": flight_ticket.pnr
        }

def reschedule_flight_db(user: User, flight_data:dict)-> dict| None:
    ticket = FlightTicket.objects.filter(user=user, pnr=flight_data.get("pnr")).first()
    if not ticket:
        return None
    
    previous_ticket_data = {
        "arrival": ticket.arrival,
        "departure": ticket.departure,
        "arrival_time": ticket.arrival_time,
        "departure_time": ticket.departure_time
    }
    
    if flight_data["arrival"]:
        ticket.arrival = flight_data["arrival"]
    
    if flight_data["departure"]:
        ticket.departure = flight_data["departure"]

    if flight_data["departure_time"]:
        ticket.departure_time = flight_data["departure_time"]
        ticket.arrival_time = get_arrival_time(flight_data.get("departure_time"))
    ticket.save()

    return {
        "update_ticket_data": {
            "arrival": ticket.arrival,
            "departure": ticket.departure,
            "arrival_time": ticket.arrival_time,
            "departure_time": ticket.departure_time
        },
        "previous_ticket_data": previous_ticket_data
    }

def cancel_flight_db(user:User, pnr: str) -> FlightTicket | None:
    ticket = FlightTicket.objects.filter(user=user, pnr=pnr).first()
    if not ticket:
        return None
    ticket.is_cancelled= True
    ticket.save()
    
    return ticket
    
    

