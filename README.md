# Library Room Auto-Scheduler
For Temple students who need to schedule rooms in Charles Library farther in advance, the Library Room Auto-Scheduler is a room booking app that allows you to automatically schedule rooms as soon as they’re available. Unlike Charles’s own scheduler, our product allows proactive students to book rooms more than 2-3 days in advance without needing to navigate through the library’s appointment interface.

![This is a screenshot.](images/login.png)
![This is a screenshot.](images/booking.png)

# How to run
- Download the latest binary from the Release section on the right on GitHub.  
- On the command line uncompress using
```
tar -xzf  
```
- On the command line run with
```
./hello
```
- You will see Hello World! on your terminal. 

# How to contribute
Follow this project board to know the latest status of the project: [http://...]([https://github.com/cis3296s22/libraryroomscheduler/projects/2])  

### How to build
- Use this github repository
- Use Visual Studio Code
- Install:

```
pip3 install selenium
pip3 install kivy
pip3 install webdriver_manager
pip3 install pyinstaller

```
- Run main.py to login and book a room through the command line
- Run bookRoom.py to login and book a room with a GUI 
- In both programs, the user will be prompted for their TU credentials to login and they'll be asked to specify the details of their booking.
- main.py opens the browser to show the automation of the login/booking process, but it won't make the reservation. 
- bookRoom.py will not open the browser for the login process but after the booking details are entered and submitted, the browser opens and the user can see the room being booked. An actual reservation will be made (Check TUmail).


