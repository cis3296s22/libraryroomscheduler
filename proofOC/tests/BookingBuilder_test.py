import pytest
import shutil
import os

from unittest import TestCase
from proofOC.BookingBuilder import BookingBuilder, BookingCreationException

class Test_BookingBuilder(TestCase):

  LOCAL_PATH_NAME = "local"
  USERNAME = "user"
  PASSWORD = "p@ssw0rd"

  @classmethod
  def setUp(self):
    os.mkdir(self.LOCAL_PATH_NAME)

  @classmethod
  def tearDown(self):
    shutil.rmtree(self.LOCAL_PATH_NAME)

  def test_create_new_booking_builder(self):
    booking = BookingBuilder(self.USERNAME, self.PASSWORD, self.LOCAL_PATH_NAME)
    assert booking is not None

  def test_create_new_booking_builder_throws_on_nonexistent_path(self):
    with pytest.raises(BookingCreationException) as test_exception:
      booking = BookingBuilder(self.USERNAME, self.PASSWORD, "bad_path")

    assert "Unable to create file" in str(test_exception.value)

  def test_add_booking_to_file(self):
    booking = BookingBuilder(self.USERNAME, self.PASSWORD, self.LOCAL_PATH_NAME)
    booking.addBooking("2022-04-17", "8:00am", "small")

    f = open (booking.fullPath, "r")
    lines = f.readlines()
    f.close()
    assert "2022-04-17,8:00am,small" in lines[1]
