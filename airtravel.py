""" Model for aircraft flights. """


class Flight:
    """ A flight with a particular passenger aircraft """

    def __init__(self, number, aircraft):
        # Verifies if the 1st two characters of the flight no. are alphabetic
        if not number[:2].isalpha():
            # raises error if not
            raise ValueError(f"No airline code in '{number}'")

        # checks if the slice is in upper case form or not
        if not number[:2].isupper():
            raise ValueError(f"Invalid airline code '{number}'")

        # through slicing and int, we verify the next numbers are digits between 0-9999
        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError(f"Invalid route number '{number}'")

        self._number = number
        self._aircraft = aircraft
        # retrival of aircraft's seating plan using tuple unpacking of seat identifiers into local variables
        rows, seats = self._aircraft.seating_plan()

        # list for seat allocations
        self._seating = [None] + \
            [{letter: None for letter in seats} for _ in rows]

    # This method delegates the aircraft on behalf of the client
    def aircraft_model(self):
        return self._aircraft.model()

    def number(self):
        return self._number

    # returns a slice of the flight number
    def airline(self):
        return self._number[:2]

    def allocate_seat(self, seat, passenger):
        """ Allocate a seat to a passenger
        Args:
            seat:A seat designator such as '12C' or '16D'
            passenger: the passenger name

        Raises:
            ValueError: If the seat is unavailable
        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} already occupied")

        self._seating[row][letter] = passenger

    def _parse_seat(self, seat):
        rows, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]  # obtaining the seat letter
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")

        row_text = seat[:-1]  # obtaining the row
        try:
            row = int(row_text)
        except:
            raise ValueError(f"Invalid seat row {row_text}")

        if row not in rows:
            raise ValueError(f"Invalid row number {row}")

        return row, letter

    def relocate_passenger(self, from_seat, to_seat):
        """ Relocate a passenger to a different seat.

        Args:
            from_seat: The existing seat designator for the
                        passenger to moved
            to_seat: The new seat designator
        """
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"No passenger to relocate in seat {from_seat}")

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is None:
            raise ValueError(f"Seat {to_seat} is already occupied")

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    # checking for the available seats
    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                   for row in self._seating
                   if row is not None)

    # this method accepts a card printer
    # concept of duck typing(polymorphism) was achieved here
    def making_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(),
                         self.aircraft_model())

    def _passenger_seats(self):
        """ An iterable series of passenger seating locations."""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield(passenger, f"{row}{letter}")

# Base class for the derived classes


class Aircraft:
    """ Inheritance in Python"""

    # returns the total number of seats
    def __init__(self, registration):  # initializer takes in fewer args
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)


# Acceptance of seat bookings made by passengers for different airplanes

# Aircraft type 1
class AirbusA345(Aircraft):  # Aircraft class is inherited

    def model(self):
        return "Airbus A345"

    # returns allowed rows and seats as a tuple in the plane
    def seating_plan(self):
        return range(1, 23), "ABCDEF"

# Aircraft type 2


class Boeing777(Aircraft):  # Aircraft class is inherited

    def model(self):
        return "Boeing 777"

    # returns allowed rows and seats as a tuple in the plane
    def seating_plan(self):
        # for simplicity sake, we ignore complex
        # seating arrangement for first class
        return range(1, 23), "ABCDEFGHIJK"


# Card printing function that prints boarding cards for passengers in the terminal
def console_card_printer(passenger, seat, flight_number, aircraft):
    output = f"| Name: {passenger}"         \
             f"  Flight: {flight_number}"  \
             f"  Seat: {seat}"             \
             f"  Aircraft: {aircraft}"     \
             " |"

    banner = "+" + "-" * (len(output) - 2) + "+"
    border = "|" + " " * (len(output) - 2) + "|"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()

# both aircraft models will work with Flight class as they quack like duck(duck typing)😄


def make_flights():
    f = Flight(
        "BA1654", AirbusA345("G-EUPT"))
    f.allocate_seat("12C", "Lionel Man")
    f.allocate_seat("10A", "Dude Perfect")
    f.allocate_seat("11D", "Pana Wana")
    f.allocate_seat("1A", "Flir Digg")
    f.allocate_seat("2B", "Zen Mod")

    b = Flight(
        "CD2341", Boeing777("A-AIRX"))
    b.allocate_seat("3D", "Larry Walden")
    b.allocate_seat("20E", "Yao Hamushi")
    b.allocate_seat("12A", "Micheal Mroto")
    b.allocate_seat("2C", "Claire Reecs")
    b.allocate_seat("4B", "Pragya Khan")

    return f, b
