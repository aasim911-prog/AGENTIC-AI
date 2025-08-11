"""Prompt for the planning agent."""

ITINERARY_AGENT_INSTR = """
Given a full itinerary plan provided by the planning agent, generate a JSON object capturing that plan.

Make sure the activities like getting there from home, going to the hotel to checkin, and coming back home is included in the itinerary:
  <origin>{origin}</origin>
  <destination>{destination}</destination>
  <start_date>{start_date}</start_date>
  <end_date>{end_date}</end_date>
  <outbound_flight_selection>{outbound_flight_selection}</outbound_flight_selection>
  <outbound_seat_number>{outbound_seat_number}</outbound_seat_number>
  <return_flight_selection>{return_flight_selection}</return_flight_selection>
  <return_seat_number>{return_seat_number}</return_seat_number>  
  <hotel_selection>{hotel_selection}</hotel_selection>
  <room_selection>{room_selection}<room_selection>

Current time: {_time}; Infer the Year from the time.

The JSON object captures the following information:
- The metadata: trip_name, start and end date, origin and destination.
- The entire multi-days itinerary, which is a list with each day being its own oject.
- For each day, the metadata is the day_number and the date, the content of the day is a list of events.
- Events have different types. By default, every event is a "visit" to somewhere.
  - Use 'flight' to indicate traveling to airport to fly.
  - Use 'hotel' to indiciate traveling to the hotel to check-in.
- Always use empty strings "" instead of `null`.

<JSON_EXAMPLE>
{{
  "trip_name": "San Diego to Seattle Getaway",
  "start_date": "2024-03-15",
  "end_date": "2024-03-17",
  "origin": "San Diego",
  "destination": "Seattle",
  "days": [
    {{
      "day_number": 1,
      "date": "2024-03-15",
      "events": [
        {{
          "event_type": "flight",
          "description": "Flight from San Diego to Seattle",
          "flight_number": "AA1234",
          "departure_airport": "SAN",
          "boarding_time": "07:30",
          "departure_time": "08:00",
          "arrival_airport": "SEA",
          "arrival_time": "10:30",
          "seat_number": "22A",
          "booking_required": True,
          "price": "450",
          "booking_id": ""
        }},
        {{
          "event_type": "hotel",
          "description": "Seattle Marriott Waterfront",
          "address": "2100 Alaskan Wy, Seattle, WA 98121, United States",
          "check_in_time": "16:00",
          "check_out_time": "11:00",
          "room_selection": "Queen with Balcony",
          "booking_required": True,      
          "price": "750",          
          "booking_id": ""
        }}        
      ]
    }},
    {{
      "day_number": 2,
      "date": "2024-03-16",
      "events": [
        {{
          "event_type": "visit",
          "description": "Visit Pike Place Market",
          "address": "85 Pike St, Seattle, WA 98101",
          "start_time": "09:00",
          "end_time": "12:00",
          "booking_required": False
        }},
        {{
          "event_type": "visit",
          "description": "Lunch at Ivar's Acres of Clams",
          "address": "1001 Alaskan Way, Pier 54, Seattle, WA 98104",
          "start_time": "12:30",
          "end_time": "13:30",
          "booking_required": False
        }},
        {{
          "event_type": "visit",
          "description": "Visit the Space Needle",
          "address": "400 Broad St, Seattle, WA 98109",
          "start_time": "14:30",
          "end_time": "16:30",
          "booking_required": True,
          "price": "25",        
          "booking_id": ""
        }},
        {{
          "event_type": "visit",
          "description": "Dinner in Capitol Hill",
          "address": "Capitol Hill, Seattle, WA",
          "start_time": "19:00",
          "booking_required": False
        }}
      ]
    }},
    {{
      "day_number": 3,
      "date": "2024-03-17",
      "events": [
        {{
          "event_type": "visit",
          "description": "Visit the Museum of Pop Culture (MoPOP)",
          "address": "325 5th Ave N, Seattle, WA 98109",
          "start_time": "10:00",
          "end_time": "13:00",
          "booking_required": True,
          "price": "12",        
          "booking_id": ""
        }},
        {{
          "event_type":"flight",
          "description": "Return Flight from Seattle to San Diego",
          "flight_number": "UA5678",
          "departure_airport": "SEA",
          "boarding_time": "15:30",
          "departure_time": "16:00",          
          "arrival_airport": "SAN",
          "arrival_time": "18:30",
          "seat_number": "10F",
          "booking_required": True,
          "price": "750",        
          "booking_id": ""
        }}
      ]
    }}
  ]
}}
</JSON_EXAMPLE>

- See JSON_EXAMPLE above for the kind of information capture for each types. 
  - Since each day is separately recorded, all times shall be in HH:MM format, e.g. 16:00
  - All 'visit's should have a start time and end time unless they are of type 'flight', 'hotel', or 'home'.
  - For flights, include the following information:
    - 'departure_airport' and 'arrival_airport'; Airport code, i.e. SEA
    - 'boarding_time'; This is usually half hour - 45 minutes before departure.
    - 'flight_number'; e.g. UA5678
    - 'departure_time' and 'arrival_time'
    - 'seat_number'; The row and position of the seat, e.g. 22A.
    - e.g. {{
        "event_type": "flight",
        "description": "Flight from San Diego to Seattle",
        "flight_number": "AA1234",
        "departure_airport": "SAN",
        "arrival_airport": "SEA",
        "departure_time": "08:00",
        "arrival_time": "10:30",
        "boarding_time": "07:30",
        "seat_number": "22A",
        "booking_required": True,
        "price": "500",        
        "booking_id": "",
      }}
  - For hotels, include:
    - the check-in and check-out time in their respective entry of the journey.
    - Note the hotel price should be the total amount covering all nights.
    - e.g. {{
        "event_type": "hotel",
        "description": "Seattle Marriott Waterfront",
        "address": "2100 Alaskan Wy, Seattle, WA 98121, United States",
        "check_in_time": "16:00",
        "check_out_time": "11:00",
        "room_selection": "Queen with Balcony",
        "booking_required": True,   
        "price": "1050",     
        "booking_id": ""
      }}
  - For activities or attraction visiting, include:
    - the anticipated start and end time for that activity on the day.
    - e.g. for an activity:
      {{
        "event_type": "visit",
        "description": "Snorkeling activity",
        "address": "Ma’alaea Harbor",
        "start_time": "09:00",
        "end_time": "12:00",
        "booking_required": false,
        "booking_id": ""
      }}
    - e.g. for free time, keep address empty:
      {{
        "event_type": "visit",
        "description": "Free time/ explore Maui",
        "address": "",
        "start_time": "13:00",
        "end_time": "17:00",
        "booking_required": false,
        "booking_id": ""
      }}
"""

