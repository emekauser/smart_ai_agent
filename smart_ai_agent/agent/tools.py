from langchain_core.tools import tool, BaseTool
from typing import Optional, List

from .flight_interface import book_flight_db, reschedule_flight_db, cancel_flight_db


def generate_flight_tools(user) -> List[BaseTool]:

    @tool
    def reschedule_flight( pnr: Optional[str], departure_city: Optional[str], arrival_city: Optional[str], departure_time: Optional[str]) -> str:
        """
        This tool should get customer pnr from the prompt when submitted by human,
        when user try to reschedule flight
        """
       
        if not pnr:
            return "Please provide your PNR to reschedule your flight."

        ticket = reschedule_flight_db(user, {"pnr": pnr, "departure": departure_city, "arrival": arrival_city, "departure_time": departure_time})
        return f"Flight rescheduled for customer with the following details: {ticket}."


    @tool
    def book_flight(departure_city: str, arrival_city: str, departure_time: str):
        """
        This tool book a flight for user with departure and arrival cities, departure date and time.
        """
        ticket = book_flight_db(user, {
            "departure": departure_city,
            "arrival": arrival_city,
            "departure_time": departure_time
        })
        if not ticket:
            return "Failed to book flight. Please check the provided details."

        return f"Flight booked from {departure_city} to {arrival_city} on {departure_time}."

    @tool
    def cancel_flight( pnr: str):
        """
        This tool should get customer pnr from the prompt when submitted by human,
        when user try to cancel flight
        """

        print(f"Customer pnr received: {pnr}")
        ticket = cancel_flight_db(user, pnr)
        if ticket:
            return f"Flight cancelled for PNR {pnr}."
        else:
            return "Please provide all required information: pnr to cancel your flight."

    @tool
    def ask_for_refund( pnr: str):
        """
        This tool should get customer pnr from the prompt when submitted by human,
        when user try to ask for refund
        """ 
        print(f"Customer pnr received: {pnr}")

        if pnr:
            return f"Refund requested for PNR {pnr}."
        return "Please provide all required information: email, pnk, and surname to request a refund."

   
    
    return [reschedule_flight, book_flight, cancel_flight, ask_for_refund]
