from ast import Str
import os.path

class BookingBuilder:
  def __init__(self, username: str, password: str):
    """
    Creates a bookings history file only if it doesn't exist.
    The username and password are stored on the first line and used to 
    automate the scheduling.
    """
    self.fileName = "bookings.csv"
    self.fullPath = f"local_repo/{self.fileName}"

    if not os.path.isfile(self.fullPath):
    # create the first line with user/pass if it doesn't exist
      with open(self.fullPath, "w+") as f:
        f.write(f"{username},{password}\n")

  def addBooking(self, date:str, time:str, size:str):
    """
    Adds a booking to the csv with each value wrapped in double quotes.
    """
    # TODO do we want to validate date/time here?
    with open(self.fullPath, "a+") as f:
      f.write(f'{date},{time},{size}\n')
