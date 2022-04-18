import os.path
import sys
import logging

class BookingCreationException(Exception):
  pass

class BookingBuilder:
  def __init__(self, username: str, password: str, bookingP: str):
    """
    Creates a bookings history file only if it doesn't exist.
    The username and password are stored on the first line and used to 
    automate the scheduling.
    """
    self.fileName = "bookings.csv"
    self.fullPath = f"{bookingP}/{self.fileName}"
    self.logger = logging.getLogger("appLog")

    if not os.path.isfile(self.fullPath):
    # create the first line with user/pass if it doesn't exist
      try:
        with open(self.fullPath, "w+") as f:
          f.write(f"{username},{password}\n")
      except:
        self.logger.error("Unable to create file:")
        raise BookingCreationException("Unable to create file to store booking data!")

  def addBooking(self, date:str, time:str, size:str):
    """
    Adds a booking to the csv with each value wrapped in double quotes.
    """
    # TODO do we want to validate date/time here?
    try:
      with open(self.fullPath, "a+") as f:
        f.write(f'{date},{time},{size}\n')
      self.logger.debug("Added datetime to booking csv")
    except:
      self.logger.error("Unable to add to file:")
      raise BookingCreationException("Unable to add booking information to file!")
