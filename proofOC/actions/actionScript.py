



import datetime as dt
import calendar

from numpy import index_exp
from TraverseSite import TraverseSite
import pandas as pd


def convertDate(date, time):
    select = dt.datetime.strptime(date, "%Y-%m-%d").date()
    fullDate = select.strftime("%B %-d, %Y")
    weekday = calendar.day_name[select.weekday()]
    selectTime = (f"{time} {weekday}, {fullDate}")
    return selectTime

def readCSV(bookings):
    # Grab the date and the new day that just opened up
    currentDate = dt.date.today()
    smallNewDate = str(currentDate + dt.timedelta(days=2))
    largeNewDate = str(currentDate + dt.timedelta(days=3))

    userN = bookings.iloc[0]['date']
    passW = bookings.iloc[0]['time']

    bookings = bookings.drop([0]).reset_index(drop=True)
    bookings = bookings.loc[(bookings['date'] == smallNewDate) & (bookings['size'] =='small') | (bookings['date'] == largeNewDate) & (bookings['size'] =='large')]
    bookings = bookings.reset_index(drop=True)

    finalBookings=[]

    for size in ['small', 'large']:
        index = bookings.index[bookings['size'] == size].tolist()
        if(len(index)>0):
            index=index[0]
            dateTime = convertDate(bookings.iloc[index]['date'], bookings.iloc[index]['time'])
            sizeOption = bookings.iloc[index]['size']
            finalBookings.append(f"{dateTime}+{sizeOption}") 

    print("Making bookings for: \n{}".format(finalBookings))

    if(finalBookings):
        scrapeSite = TraverseSite("https://tuportal5.temple.edu/", "https://charlesstudy.temple.edu/reserve/charles-")
        return scrapeSite.bookRoom(finalBookings, userN, passW)
    else:
        print("No Rooms to Book for")

successfulBookings = []
try: 
    bookings = pd.read_csv('bookings.csv', names=["date", "time", "size"])
    if(not bookings.empty):
        successfulBookings = readCSV(bookings)
    else:
        print("Empty file")
except:
    print("No bookings")

print("\n\n\nROOMS BOOKED: ")
for i in successfulBookings:
    print(f"\n\t - Room size {i.split('+')[1]} : {i.split('+')[0]}")

print("\n\n\n")


