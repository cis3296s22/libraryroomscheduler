import os.path
import sys
import logging

class BookingCreationException(Exception):
  """
  A custom exception used with the BookingBuilder class. 
  Used to send more specific error messages back to the caller where things failed.
  """
  pass

class BookingBuilder:
  """
  A class to represent the CSV file used to kepe track of library bookings
  
  . . .

  Attributes
  ----------
  fileName: str
    Name of the .csv file. Always 'bookings.csv'
  fullPath: str
    The full system path needed to access the file
  logger: Logger
    A logging object to log events

  Methods
  ----------
  addBooking(date:str, time:str, size:str)
    Adds a booking to the csv with each value wrapped in double quotes.
  """
  def __init__(self, username: str, password: str, bookingP: str):
    """
    Creates a bookings history file only if it doesn't exist.
    The username and password are stored on the first line and used to 
    automate the scheduling.

    . . .

    Parameters
    ----------
      username: str
        The Temple username of whomever is booking the library room
      password: str
        The password associated with the Temple username
      bookingP: str
        The filepath where the .csv file is located
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

    . . .

    Parameters
    ----------
    date: str
      The date of the booking as a string
    time: str
      The time of the booking as a string
    size: str
      The size of the room to be booked. Typically either small or large.

    Returns
    ----------
    None
    """
    # TODO do we want to validate date/time here?
    try:
      with open(self.fullPath, "a+") as f:
        f.write(f'{date},{time},{size}\n')
      self.logger.debug("Added datetime to booking csv")
    except:
      self.logger.error("Unable to add to file:")
      raise BookingCreationException("Unable to add booking information to file!")

  def removeBooking(self, date:str, time:str, size:str):
      """
      Finds and removes a booking from the csv file.
      """
      string = (f'{date},{time},{size}\n')
      
      try:
          with open(self.fullPath, "r+") as f:
              lines = f.readlines()
              # delete the line with the booking 
          for line in lines:
                  print(line)
                  if (line == string):
                      index = lines.index(string)
                      lines.pop(index)
          f.truncate(0)
          f.writelines(lines)
      except:
          self.logger.error("Unable to modify the file.")
          raise BookingCreationException("Unable to change booking information in the file.")
