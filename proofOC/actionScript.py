



import datetime as dt
import calendar
from TraverseSite import TraverseSite


def convertDate(date, time, roomSize):
    select = dt.datetime.strptime(date, "%Y-%m-%d").date()
    fullDate = select.strftime("%B %-d, %Y")
    weekday = calendar.day_name[select.weekday()]
    selectTime = (f"{time} {weekday}, {fullDate}")
    return selectTime


# As soon as it turns the next day - check for new day that opened up
currentDate = dt.date.today()
newDate = str(currentDate + dt.timedelta(days=2))
passW = userN = ""
booking = []

# Check if there are any dates in the csv that can be booked
with open('local_repo/bookings.csv', 'r') as f:
    cnt = 0
    results = []
    for line in f:
            words = line.strip().split(',')
            lineObj = words[0]
            if(cnt==0):
                userN = lineObj
                passW = words[1]
                
            if(words[0] == newDate):
                print("Booking for date: " + lineObj)
                booking = words
                break

            else:
                print("Cant book for date: " + lineObj)
            cnt = cnt+1


if booking:
    link = f"https://charlesstudy.temple.edu/reserve/charles-{booking[2]}"
    scrapeSite = TraverseSite(link)

    dateTime = convertDate(*booking)
    bookingString = scrapeSite.findRoom(dateTime)

    if bookingString is not None:
        print(bookingString)
        scrapeSite.bookRoom(bookingString, userN, passW)
    else:
        print("No rooms available")
else:
    print("No bookings to be made")
    

# "https://charlesstudy.temple.edu/reserve/charles-small"
# print("Date1 =", d1)

# d2 = dt.datetime.strptime("2022-5-8", "%Y-%m-%d").date()

# print("Date2 =", d2)

# delta = d2-d1
# print(delta.days)

