import datetime as dt
import calendar
from TraverseSite import TraverseSite


def convertDate(date, time):
    """
    Converts a date and time into a string

    . . .

    Parameters
    ----------
    date: datetime.date
      The date of the booking
    time: datetime.time
      The time of the booking

    Returns
    ----------
    A string of the date and time along with the day of the week
    """
    select = dt.datetime.strptime(date, "%Y-%m-%d").date()
    fullDate = select.strftime("%B %-d, %Y")
    weekday = calendar.day_name[select.weekday()]
    selectTime = (f"{time} {weekday}, {fullDate}")
    return selectTime


# Grab the date and the new day that just opened up
currentDate = dt.date.today()
newDate = str(currentDate + dt.timedelta(days=2))

passW = userN = ""
booking = []

# Check if there are any dates in the csv that can be booked (compare to newDate)
with open('bookings.csv', 'r') as f:
    count = 0
    results = []
    for line in f:
        words = line.strip().split(',')
        lineObj = words[0]

        # If the first line is being read, save the username and password
        if(count==0):
            userN = lineObj
            passW = words[1]
            count = count+1
            continue
            
        if(words[0] == newDate):
            print("Booking for date: " + lineObj + " @ " + words[1])
            booking = words
            break
        else:
            print("Cant book for date: " + lineObj)
        count = count+1


# Make the booking 
if booking:
    link = f"https://charlesstudy.temple.edu/reserve/charles-{booking[2]}"
    scrapeSite = TraverseSite(link)

    # Convert csv date and time in the correct format ('8:30am Wednesday, April 6, 2022...')
    dateTime = convertDate(booking[0], booking[1])

    # 'Random' room number is returned in correct format ('8:30am Wednesday, April 6, 2022 - ### - Available)
    bookingString = scrapeSite.findRoom(dateTime)

    if bookingString is not None:
       
        scrapeSite.bookRoom(bookingString, userN, passW)
    else:
        print("No rooms available")
else:
    print("No bookings to be made")
    
