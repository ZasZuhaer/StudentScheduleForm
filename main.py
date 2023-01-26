import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from collections import OrderedDict

login_url = 'https://portal.aiub.edu/'
portal_url = 'https://portal.aiub.edu/Student/Home/Index/5'
courses_url = 'https://portal.aiub.edu'
course_and_time = []

# username = input("Enter your ID including hy-phen: ")
# password = input("Enter your password: ")
payload = {
    'UserName': input("Enter your ID including hy-phen: "),
    'Password': input("Enter your password: ")
}
thesoup = open('thesoup.txt', mode='r')
course_soup = open('courselinksoup.txt', mode='r')
registered_courses = []
courses_list = []


class Course:

    def time_conversion(self, timed):
        hours, minutes = map(int, (timed.split(':')[0], timed.split(':')[1]))
        if hours < 8:
            hours += 12
        joined_time = (hours * 60) + minutes
        return joined_time

    def __init__(self, name, sections, start_time1, end_time1, room1, day1, start_time2='00:00', end_time2='00:00', room2='0', day2='0'):
        self.name = name
        self.sections = sections
        self.start_time1 = start_time1
        self.start_time2 = start_time2
        self.end_time1 = end_time1
        self.end_time2 = end_time2
        self.room1 = room1
        self.room2 = room2
        self.day1 = day1
        self.day2 = day2
        self.start_time1_universal = self.time_conversion(start_time1)
        self.start_time2_universal = self.time_conversion(start_time2)
        self.end_time1_universal = self.time_conversion(end_time1)
        self.end_time2_universal = self.time_conversion(end_time2)


with requests.session() as s:
    r = s.post(login_url, data=payload)
    soup = BeautifulSoup(r.text, 'lxml')
    # soup = BeautifulSoup(thesoup, 'lxml')  #
    res = soup.select(".btn.btn-default.form-control option")
    for we in res:
        if we.text == "2022-2023, Spring":
            courses_url += str(we["value"])
            break
    courses_url = courses_url.replace("/Home/CourseList", "/Registration")
    r2 = s.get(courses_url)
    soup2 = BeautifulSoup(r2.text, 'lxml')
    # soup2 = BeautifulSoup(course_soup, 'lxml')  #
    rows = soup2.select(".table.table-details tr")

    for trow in rows[1:]:
        tupy = (str(trow.select("a")[0].text))
        for item in trow.select("span"):
            tupy += (str(item.text))
        registered_courses.append(tupy)

no_of_courses_registered = len(registered_courses)

for course in registered_courses:

    # extracting the course name and section
    main_course = course
    course_name_pattern = r'((?:\S+\s+)+\bTime)'
    for x in range(0, 2):
        course_name = re.search(course_name_pattern, course)
        try:
            len(course_name.group())
        except AttributeError:
            break
        size = len(course_name.group())
        course = course_name.group()[:size - 5]
    section_pattern = r'\[\w{1,2}\]'
    section = re.search(section_pattern, main_course)

    if section is None:
        section_pattern = r'\[\w\d{1,2}\]'
        section = re.search(section_pattern, main_course)
        section = section.group()
    course = course[6:]

    # extracting time and room
    time_and_room = main_course.split(f"{course + ' '}")[1]

    # extracting time
    time_pattern = r'\d+:\d+'
    times = re.findall(time_pattern, time_and_room)
    times_and_rooms = []
    for time in times:
        ######################################
        # joined_time = ''.join(time.split(':'))
        # if len(joined_time) == 2:
        #     joined_time = joined_time+'0'
        # joined_time = int(joined_time)
        # if joined_time < 800:
        #     joined_time += 1200
        # times_and_rooms.append(joined_time)
        times_and_rooms.append(time)

    # extracting day
    days_pattern = r'\s\w{3}\s'
    days = re.findall(days_pattern, time_and_room)
    days = list(OrderedDict.fromkeys(days))
    if len(days) == 1:
        days.append("0")

    # extracting room
    room_pattern = r'Room:\S*(?:\s\S+)?'
    rooms = re.findall(room_pattern, time_and_room)
    for i, room in enumerate(rooms):
        rooms[i] = room.replace("Room: ", '')

    if len(times_and_rooms) == 4:
        times_and_rooms.insert(2, rooms[0])
        times_and_rooms.append(rooms[1])
    elif len(times_and_rooms) == 2:
        times_and_rooms.insert(2, rooms[0])
        times_and_rooms.extend(['00:00', '00:00', '00:00'])

    print(course)
    print(times_and_rooms)
    print(main_course)
    print("\n")

    obj = Course(course, section, times_and_rooms[0], times_and_rooms[1], times_and_rooms[2], days[0], times_and_rooms[3],
                 times_and_rooms[4], times_and_rooms[5], days[1])
    courses_list.append(obj)


f = open("SSF.html", 'w')
f.write('''<!DOCTYPE html>
<html>
   <head>
      <title>SSF - Student Schedule Form</title>
      <link href="cass.css" rel="stylesheet">
   </head>
   <body>
      <div id="calendar1" style="width: 98%; margin-left: 1%;">
         <div id="cal1" class="calendar ng-isolate-scope ng-pristine ng-valid fc fc-ltr fc-unthemed" ng-model="eventSource" calendar="myCalendar1" ui-calendar="uiConfig.calendar">
            <div class="fc-view-container" style="">
               <div class="fc-view fc-agendaWeek-view fc-agenda-view" style="">
                  <table>
                     <thead>
                        <tr>
                           <td class="fc-widget-header">
                              <div class="fc-row fc-widget-header" style="border-right-width: 1px; margin-right: 13px;">
                                 <table>
                                    <thead>
                                       <tr>
                                          <th class="fc-axis fc-widget-header" style="width: 34px;"></th>
                                          <th class="fc-day-header fc-widget-header fc-sun">Sun</th>
                                          <th class="fc-day-header fc-widget-header fc-mon">Mon</th>
                                          <th class="fc-day-header fc-widget-header fc-tue">Tue</th>
                                          <th class="fc-day-header fc-widget-header fc-wed">Wed</th>
                                          <th class="fc-day-header fc-widget-header fc-thu">Thu</th>
                                          <th class="fc-day-header fc-widget-header fc-fri">Fri</th>
                                          <th class="fc-day-header fc-widget-header fc-sat">Sat</th>
                                       </tr>
                                    </thead>
                                 </table>
                              </div>
                           </td>
                        </tr>
                     </thead>
                     <tbody>
                        <tr>
                           <td class="fc-widget-content">
                              <div class="fc-time-grid-container fc-scroller" style="height: 567px;">
                                 <div class="fc-time-grid">
                                    <div class="fc-bg">
                                       <table>
                                          <tbody>
                                             <tr>
                                                <td class="fc-axis fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-day fc-widget-content fc-sun fc-past" data-date="2023-01-15"></td>
                                                <td class="fc-day fc-widget-content fc-mon fc-past" data-date="2023-01-16"></td>
                                                <td class="fc-day fc-widget-content fc-tue fc-past" data-date="2023-01-17"></td>
                                                <td class="fc-day fc-widget-content fc-wed fc-past" data-date="2023-01-18"></td>
                                                <td class="fc-day fc-widget-content fc-thu fc-past" data-date="2023-01-19"></td>
                                                <td class="fc-day fc-widget-content fc-fri fc-today fc-state-highlight" data-date="2023-01-20"></td>
                                                <td class="fc-day fc-widget-content fc-sat fc-future" data-date="2023-01-21"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </div>
                                    <div class="fc-slats">
                                       <table>
                                          <tbody>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>8am</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>9am</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>10am</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>11am</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>12pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>1pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>2pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>3pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>4pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>5pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>6pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>7pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>8pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>9pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr>
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"><span>10pm</span></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                             <tr class="fc-minor">
                                                <td class="fc-axis fc-time fc-widget-content" style="width: 34px;"></td>
                                                <td class="fc-widget-content"></td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </div>
                                    <hr class="fc-widget-header" style="display: none;">
                                    <div class="fc-content-skeleton">
                                       <table>
                                          <tbody>
                                             <tr>
                                                <td class="fc-axis" style="width: 34px;"></td>
                                                <td>
                                                   <div class="fc-event-container">''')

sun = " Sun "
mon = " Mon "
tue = " Tue "
wed = " Wed "

for course in courses_list:
    if course.day1 == sun:
        f.write(f'''<a class="fc-time-grid-event fc-event fc-start fc-end  ng-scope" style="inset: {(course.start_time1_universal-480)*0.72133}px 0% -{(course.end_time1_universal-480)*0.72133}px; z-index: 1;">
                                                         <div class="fc-content">
                                                            <div class="fc-title"><span>{course.start_time1} - {course.end_time1} {course.sections}</span></div>
                                                            <div class="fc-title"><span>Room: {course.room1}</span></div>
                                                            <div class="fc-title">{course.name}</div>
                                                         </div>
                                                         <div class="fc-bg"></div>
                                                      </a>''')

f.write('''</div></td><td><div class="fc-event-container">''')

for course in courses_list:
    if course.day1 == mon:
        f.write(
            f'''<a class="fc-time-grid-event fc-event fc-start fc-end  ng-scope" style="inset: {(course.start_time1_universal - 480) * 0.72133}px 0% -{(course.end_time1_universal - 480) * 0.72133}px; z-index: 1;">
                                                                 <div class="fc-content">
                                                                    <div class="fc-title"><span>{course.start_time1} - {course.end_time1} {course.sections}</span></div>
                                                                    <div class="fc-title"><span>Room: {course.room1}</span></div>
                                                                    <div class="fc-title">{course.name}</div>
                                                                 </div>
                                                                 <div class="fc-bg"></div>
                                                              </a>''')

f.write('''</div></td><td><div class="fc-event-container">''')

for course in courses_list:
    if course.day1 == tue:
        f.write(
            f'''<a class="fc-time-grid-event fc-event fc-start fc-end  ng-scope" style="inset: {(course.start_time1_universal - 480) * 0.72133}px 0% -{(course.end_time1_universal - 480) * 0.72133}px; z-index: 1;">
                                                                 <div class="fc-content">
                                                                    <div class="fc-title"><span>{course.start_time1} - {course.end_time1} {course.sections}</span></div>
                                                                    <div class="fc-title"><span>Room: {course.room1}</span></div>
                                                                    <div class="fc-title">{course.name}</div>
                                                                 </div>
                                                                 <div class="fc-bg"></div>
                                                              </a>''')

    if course.day2 == tue:
        f.write(
            f'''<a class="fc-time-grid-event fc-event fc-start fc-end  ng-scope" style="inset: {(course.start_time2_universal - 480) * 0.72133}px 0% -{(course.end_time2_universal - 480) * 0.72133}px; z-index: 1;">
                                                                 <div class="fc-content">
                                                                    <div class="fc-title"><span>{course.start_time2} - {course.end_time2} {course.sections}</span></div>
                                                                    <div class="fc-title"><span>Room: {course.room2}</span></div>
                                                                    <div class="fc-title">{course.name}</div>
                                                                 </div>
                                                                 <div class="fc-bg"></div>
                                                              </a>''')

f.write('''</div></td><td><div class="fc-event-container">''')

for course in courses_list:
    if course.day1 == wed:
        f.write(
            f'''<a class="fc-time-grid-event fc-event fc-start fc-end  ng-scope" style="inset: {(course.start_time1_universal - 480) * 0.72133}px 0% -{(course.end_time1_universal - 480) * 0.72133}px; z-index: 1;">
                                                                 <div class="fc-content">
                                                                    <div class="fc-title"><span>{course.start_time1} - {course.end_time1} {course.sections}</span></div>
                                                                    <div class="fc-title"><span>Room: {course.room1}</span></div>
                                                                    <div class="fc-title">{course.name}</div>
                                                                 </div>
                                                                 <div class="fc-bg"></div>
                                                              </a>''')

    if course.day2 == wed:
        f.write(
            f'''<a class="fc-time-grid-event fc-event fc-start fc-end  ng-scope" style="inset: {(course.start_time2_universal - 480) * 0.72133}px 0% -{(course.end_time2_universal - 480) * 0.72133}px; z-index: 1;">
                                                                 <div class="fc-content">
                                                                    <div class="fc-title"><span>{course.start_time2} - {course.end_time2} {course.sections}</span></div>
                                                                    <div class="fc-title"><span>Room: {course.room2}</span></div>
                                                                    <div class="fc-title">{course.name}</div>
                                                                 </div>
                                                                 <div class="fc-bg"></div>
                                                              </a>''')

f.write('''</div>
                                                </td>
                                                <td>
                                                   <div class="fc-event-container"></div>
                                                </td>
                                                <td>
                                                   <div class="fc-event-container"></div>
                                                </td>
                                                <td>
                                                   <div class="fc-event-container"></div>
                                                </td>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </div>
                                 </div>
                              </div>
                           </td>
                        </tr>
                     </tbody>
                  </table>
               </div>
            </div>
         </div>
      </div>
   </body>
   </body>
</html>''')

f.close()
webbrowser.open_new_tab('SSF.html')