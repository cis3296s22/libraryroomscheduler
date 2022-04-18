from actions.TraverseSite import TraverseSite


ts = TraverseSite("https://charlesstudy.temple.edu/reserve/charles-small")

def test_bookRoom(user, passW):
    assert ts.bookRoom("//a[@aria-label='8:00am Thursday, April 14, 2022 - 386 - Available']", user,passW) == True

def test_bookRoomWrongCreds():
    assert ts.bookRoom("//a[@aria-label='8:30am Wednesday, April 13, 2022 - 311 - Available']", 't','reger') == False
    
def test_bookRoomWrongDate(user,passW):
    assert ts.bookRoom("//a[@aria-label='8:30am Wednesday, April 1, 2022 - 384 - Available']", user,passW) == False

def test_findRoomS():
    assert ts.findRoom("9:00am Wednesday, April 13, 2022") != None
    
def test_findRoomF():
    assert ts.findRoom("8:30am Tuesday, April 10, 2022") == None
