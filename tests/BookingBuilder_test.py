from venv import create
from proofOC.BookingBuilder import BookingBuilder, BookingCreationException
from proofOC.RepoCommunicator import RepoCommunicator, RepositoryConfigurationException
import pytest
import shutil
import os
import time


mainPath="tests/local_test_repo"

def createRepo(url, localPath):
    return RepoCommunicator(url, localPath)

@pytest.fixture()
def setUp():
    print("testing")
    yield
    deletingD = [".github/", "scripts/", ".git/","bookings.csv", "remoteURL.txt", "scripts"]
    
    for i in deletingD:
        try:
            if(i[-1]=="/"):
                shutil.rmtree(f"{mainPath}/{i}")
            else:
                os.remove(f"{mainPath}/{i}")
        except:
            pass
    
    shutil.rmtree(mainPath)
    time.sleep(5)

def test_bookingCreateF():
    try : 
        booking = BookingBuilder("userName", "passWord", mainPath)
    except BookingCreationException as exc:
        assert True, f"'new BookingBuilder object' raised an exception {exc}"

        
def test_bookingCreateS(setUp):
    repo = createRepo("https://github.com/ccho-0508/testL.git", mainPath)
    try : 
        booking = BookingBuilder("userName", "passWord", mainPath)
        with open(f"{mainPath}/bookings.csv") as f:
            assert f.readline().strip() == "userName,passWord"
    except BookingCreationException as exc:
        assert False, f"'new BookingBuilder object' raised an exception {exc}"


def test_addBookingF(setUp):
    repo = createRepo("https://github.com/ccho-0508/testL.git", mainPath)
    try: 
        booking = BookingBuilder("userName", "passWord", mainPath)
        booking.fullPath = ""
        booking.addBooking("5-8-2022","5:00pm","large")
        assert False
    except BookingCreationException as exc:
        assert True, f"'new BookingBuilder object' raised an exception {exc}"

def test_addBookingS(setUp):
    repo = createRepo("https://github.com/ccho-0508/testL.git", mainPath)
    try: 
        booking = BookingBuilder("userName", "passWord", mainPath)
        booking.addBooking("5-8-2022","5:00pm","large")
        assert True
    except BookingCreationException as exc:
        assert False, f"'new BookingBuilder object' raised an exception {exc}"


def test_writeFirstLine(setUp):
    repo = createRepo("https://github.com/ccho-0508/testL.git", mainPath)
    os.remove(f"{mainPath}/bookings.csv")
    try: 
        booking = BookingBuilder("userName", "passWord", mainPath)
        
        booking.addBooking("5-8-2022","5:00pm","large")
        assert True
    except BookingCreationException as exc:
        assert False, f"'new BookingBuilder object' raised an exception {exc}"

