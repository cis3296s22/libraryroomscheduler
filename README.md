# Library Room Auto-Scheduler

For Temple students who need to schedule rooms in Charles Library farther in advance, the Library Room Auto-Scheduler is a room booking app that allows you to automatically schedule rooms as soon as they’re available. Unlike Charles’s own scheduler, our product allows proactive students to book rooms more than 2-3 days in advance without needing to navigate through the library’s appointment interface.

![This is a screenshot.](images/login.png)
![This is a screenshot.](images/booking.png)

# How to run

- For MacOS users :
- Download the latest zip from the Release section on the right on GitHub.
- Extract the bookRoom.dmg file from the zip and open it
- Right click on the bookRoom.app file inside and click 'Open'. A popup will be appear claiming the file is not safe.
- Repeat the previous step. This time, the popup should have the option 'Open'. Click it and the application should load.

# How to contribute

Follow this project board to know the latest status of the project: [http://...]([https://github.com/cis3296s22/libraryroomscheduler/projects/2])

## How to build

_Note: Visual Studio Code is the recommended editor for the Library Room Auto-Scheduler_

- Python 3.8 or higher is recommended to contribute
- Clone this repo
- (Recommended) Create a virtual environment
  - In the main folder of this project, execute `python3 -m venv venv` on the command line to create the virtual environment
  - Activate it!
    - Mac/Linux: `source ./venv/bin/activate`
    - Windows: `.\venv\Scripts\activate`
- Install the dependencies by executing `pip3 install -r requirements.txt` from the main directory

If you used a virtual environment, be sure to deactivate it by executing `deactivate` from the root of this project once you are finished.

---

`main.py` will login and book a room through the command line

`bookRoom.py` to login and book a room with a GUI

---

In both programs, the user will be prompted for their TU credentials to login and they'll be asked to specify the details of their booking.

- main.py opens the browser to show the automation of the login/booking process, but it won't make the reservation.
- bookRoom.py the user can interact with a GUI to login and input their booking details. A browser will pop up to show the automated process (for now). An actual reservation will be made if the booking details are listed correctly (Check TUmail).

---

### BUILD EXECUTABLE

- From exe folder:

```
pyinstaller --onefile -y --clean --windowed bookroom.spec

pushd dist
hdiutil create ./bookRoom.dmg -srcfolder bookRoom.app -ov
popd
```

<!-- CREATE THE EXE FOLDER CONTENTS -->
<!-- pyinstaller --onefile -y --clean --windowed --name bookRoom --exclude-module _tkinter --exclude-module Tkinter --exclude-module enchant --exclude-module twisted ../proofOC/bookRoom.py -->
<!-- Change line 23 of bookroom.spec so it looks like : exe = EXE(pyz, Tree('../proofOC/'), -->
