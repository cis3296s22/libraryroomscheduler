from actions.TraverseSite import TraverseSite


ts = TraverseSite("https://tuportal5.temple.edu/", "https://charlesstudy.temple.edu/reserve/charles-")

def test_bookRoom(user, passW):
    assert ts.bookRoom(['8:00am Thursday, April 21, 2022+small', '10:00am Friday, April 22, 2022+large'], user,passW) == ['8:00am Thursday, April 21, 2022+small', '10:00am Friday, April 22, 2022+large']

def test_bookRoomWrongCreds():
    assert ts.bookRoom(['8:00am Thursday, April 21, 2022+small', '10:00am Friday, April 22, 2022+large'], 't','reger') == []
    
def test_bookRoomWrongDate(user,passW):
    assert ts.bookRoom(['7:00am Thursday, April 10, 2022+small', '10:00am Friday, April 1, 2022+large'], user,passW) == []


    
