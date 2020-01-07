"""
Model for flight details
"""


class Flight:
    """
    A flight with a particular passenger aircraft.
    """

    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError("No airline code in '{}'".format(number))

        if not number[:2].isupper():
            raise ValueError("Invalid airline code in '{}'".format(number))

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("No airline code in '{}'".format(number))

        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def _parse_seat(self, seat):
        """
        Parse a seat into a valid row and letter

        Args:
            seat: A seat designator such as 21F

        Returns:
            A tuple containing int and str for row and seat

        :param seat:
        :return:
        """
        row_numbers, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in row_numbers:
            raise ValueError("Invalid row number {}".format(row))

        return row, letter

    def allocate_seat(self, seat, passenger):
        """
        Allocate a seat to a passenger

        Args:
            seat: A seat designator such as '12C' or 21F'
            passenger: The passenger name

        Raises:
            ValueError: If the seat is unavailable

        :param seat:
        :param passenger:
        :return:
        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))

        self._seating[row][letter] = passenger

    def relocate_passenger(self, from_seat, to_seat):
        """
        Relocates a passenger from one seat to another

        Args:
            from_seat: The existing seat designator for the passenger to be moved
            to_seat: The new seat designator

        :param from_seat:
        :param to_seat:
        :return:
        """
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger to relocate in seat {}".format(from_seat))

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} is already occupied".format(to_seat))

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_of_seats_available(self):
        """
        Check how many seats on the flight are still available
        :return:
        """
        return sum(sum(1 for s in row.values() if s is None)
                   for row in self._seating
                   if row is not None)


class Aircraft:
    def __init__(self, registration, model, num_of_rows, num_of_seats_per_row):
        self._registration = registration
        self._model = model
        self._num_of_rows = num_of_rows
        self._num_of_seats_per_row = num_of_seats_per_row

    def registration(self):
        return self._registration

    def model(self):
        return self._model

    def seating_plan(self):
        return range(1, self._num_of_rows + 1), "ABCDEF"[:self._num_of_seats_per_row]

def make_flight():
    """
    Create a dummy flight with some passengers
    :return:
    """
    f = Flight("SN766", Aircraft("G-EUPT", "Airbus A319", num_of_rows=25, num_of_seats_per_row=6))
    f.allocate_seat("12A", "Oliver Martinez")
    f.allocate_seat("15F", "Emily Sophie Brown")
    f.allocate_seat("15E", "Sophie Chloe Davis")
    f.allocate_seat("1C", "Daniel Smith")
    f.allocate_seat("1E", "Charlotte Lucy Jones")
    return f
