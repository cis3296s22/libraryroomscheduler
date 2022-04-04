


# from findRoom import Scheduler
# from datetime import date
# from datetime import datetime
import datetime as dt
from threading import currentThread


# As soon as it turns the next day - two days ahead are available for schelding
currentDate = dt.date.today()

day1 = currentDate + dt.timedelta(days=1)
day2 = currentDate + dt.timedelta(days=2)

canBook = [day1, day2]

print(canBook[0])

print(canBook[1])

# print("Date1 =", d1)

# d2 = dt.datetime.strptime("2022-5-8", "%Y-%m-%d").date()

# print("Date2 =", d2)

# delta = d2-d1
# print(delta.days)

