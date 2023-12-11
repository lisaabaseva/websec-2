import traceback
from bs4 import BeautifulSoup
import requests
import pprint

import re
import json


def parseGroups():
    groups_information = {'groups':[]}
    count = 0
    for course in range(1, 6):
        soup = BeautifulSoup(requests.get(f'https://ssau.ru/rasp/faculty/492430598?course={course}').text, "html.parser")
        all = soup.findAll('a', class_="btn-text group-catalog__group")
        for data in all:
            groups_information['groups'].append({'group': data.text.strip(), 'link': data.get("href").strip()})
            count +=1

    with open('server/groups.json', 'w', encoding="utf-8") as outfile:
        json.dump(groups_information, outfile)
    # pprint.pprint(groups_information)


def parseTeachers():
    teachers_information = {'teachers': []}
    for page in range(1, 121):
        soup = BeautifulSoup(requests.get(f'https://ssau.ru/staff?page={page}').text, "html.parser")
        all = BeautifulSoup(str(soup.findAll('li', class_="list-group-item list-group-item-action")), "html.parser")
        all_teachers = all.findAll('a', href=re.compile('https://ssau.ru/staff/'))
        
        for data in all_teachers:
            href = data.get("href")
            num = re.findall(r'\d+', href)
            teachers_information['teachers'].append({'name': data.text.strip(), 'link': f'/rasp?staffId={num[0]}'})

    with open('server/teachers.json', 'w', encoding="utf-8") as outfile:
        json.dump(teachers_information, outfile)
    # pprint.pprint(teachers_information)


def timeIntervals(group_link, selected_week):
    soup = BeautifulSoup(requests.get(f'https://ssau.ru{group_link}&selectedWeek={selected_week}').text, "html.parser")
    all_time = BeautifulSoup(str(soup.findAll('div', class_="schedule__time-item")), "html.parser")
    time = []
    for i, t in enumerate(all_time):
        if i%2!=0:
            time.append(t.text.strip())
    time_intervals = [f'{time[i]}-{time[i+1]}' for i in range(0, len(time), 2)]
    return time_intervals
    

def parseSchedule(group_link, selected_week) -> list:
    time_intervals = timeIntervals(group_link, selected_week)
    
    schedule = {'понедельник': [], 'вторник': [], 'среда': [], 'четверг': [], 'пятница': [], 'суббота': []}

    soup = BeautifulSoup(requests.get(f'https://ssau.ru{group_link}&selectedWeek={selected_week}').text, "html.parser")
  
    all_day_info = soup.findAll('div', class_="schedule__item")

    for i, info in enumerate(all_day_info):
        if i<=6:
            continue

        if i%6==1:
            day = 'понедельник'
        if i%6==2:
            day = 'вторник'
        if i%6==3:
            day = 'среда'
        if i%6==4:
            day = 'четверг'
        if i%6==5:
            day = 'пятница'
        if i%6==0:
            day = 'суббота'
 
        groups = ''
        try:
            schedule__discipline = info.find('div', class_="schedule__discipline").text.strip()
            schedule__place = info.find('div', class_="schedule__place").text.strip()
            for elem in info.findAll('a', class_="schedule__group"):
                groups = groups + elem.text.strip()
        except:
            # print("исключение")
            # traceback.print_exc()
            schedule__discipline = ''
            schedule__place = ''
            groups = ''

        try:
            schedule__teacher = info.find('div', class_="schedule__teacher").text.strip()
        except:
            schedule__teacher = ''

        
        for j in range(1, len(time_intervals)+1):
            if i>6*j and i<=6*j+6:
                time = f'{time_intervals[j-1]}'

        schedule[day].append({'time': time, 
                         'discipline': schedule__discipline, 
                         'place': schedule__place, 
                         'teacher': schedule__teacher, 
                         'groups': groups})
        
    with open('server/schedule.json', 'w', encoding="utf-8") as outfile:
        json.dump(schedule, outfile, ensure_ascii=False)
    return schedule


def currentWeek():
    ret = {}
    soup = BeautifulSoup(requests.get(f'https://ssau.ru/rasp?groupId=531873998').text, "html.parser")
    week = BeautifulSoup(str(soup.findAll('div', class_="week-nav-current")), "html.parser")
    ret["week"] = week.text[3:5]
    # print(ret)
    return ret

# currentWeek()

# parseGroups()
# getCurrentWeek()
# parseSchedule('/rasp?groupId=531030143')

# parseSchedule('/rasp?groupId=531873998')
# parseSchedule('/rasp?staffId=304968307')
# parseGroups()
# parseTeachers()

parseSchedule("/rasp?staffId=123278664","16")