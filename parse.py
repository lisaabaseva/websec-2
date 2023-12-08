from bs4 import BeautifulSoup
import requests
import pprint

import re
import json


def parseGroups():
    groups_information = {}
    count = 0
    for course in range(1, 6):
        soup = BeautifulSoup(requests.get(f'https://ssau.ru/rasp/faculty/492430598?course={course}').text, "html.parser")
        all = soup.findAll('a', class_="btn-text group-catalog__group")

        groups = []
        for data in all:
            groups.append([data.text.strip(), data.get("href").strip()])
            count += 1
        groups_information[course] = groups
    # print(count)
    # pprint.pprint(groups_information)
    with open('groups.json', 'w') as outfile:
        json.dump(groups_information, outfile)

def parseTeachers():
    teachers_information = []
    # schedule__teacher
    for page in range(1, 121):
        soup = BeautifulSoup(requests.get(f'https://ssau.ru/staff?page={page}').text, "html.parser")
        # print(soup)
        all = BeautifulSoup(str(soup.findAll('li', class_="list-group-item list-group-item-action")), "html.parser")
        # all = soup.findAll('li', attrs={"class": "list-group-item list-group-item-action", "a"})

        all_teachers = all.findAll('a', href=re.compile('https://ssau.ru/staff/'))
        # print(all_teachers)

        for data in all_teachers:
            # print(data.text)
            teachers_information.append([data.text.strip(), data.get("href")])

    # pprint.pprint(teachers_information)
    with open('teachers.json', 'w') as outfile:
        json.dump(teachers_information, outfile)


def getCurrentWeek() -> int:
    soup = BeautifulSoup(requests.get(f'https://ssau.ru/rasp?groupId=531873998').text, "html.parser")
    week = BeautifulSoup(str(soup.findAll('div', class_="week-nav-current")), "html.parser")
    return week.text[3:5].strip()


def parseWeekFromGroup(group_link) -> list:
    schedule = {'понедельник': [], 'вторник': [], 'среда': [], 'четверг': [], 'пятница': [], 'суббота': []}
    soup = BeautifulSoup(requests.get(f'https://ssau.ru{group_link}').text, "html.parser")
    # items = soup.findAll('div', class_="schedule__item")
    all_day_info = soup.findAll('div', class_="schedule__item")
    # all_day_info = BeautifulSoup(str(soup.findAll('div', class_="schedule__item")), "html.parser")

    all_time = BeautifulSoup(str(soup.findAll('div', class_="schedule__time-item")), "html.parser")
    times = []
    for i, time in enumerate(all_time):
        if i%2!=0:
            times.append(time.text.strip())

    time_intervals = [f'{times[i]}-{times[i+1]}' for i in range(0, len(times), 2)]

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
        if i%6==6:
            day = 'суббота'

        try:
            schedule__discipline = info.find('div', class_="schedule__discipline").text.strip()
            schedule__place = info.find('div', class_="schedule__place").text.strip()
            schedule__teacher = info.find('div', class_="schedule__teacher").text.strip()
            groups = [elem.text.strip() for elem in info.findAll('a', class_="caption-text schedule__group")]
            # print(info.text)
        except:
            schedule__discipline = ''
            schedule__place = ''
            schedule__teacher = ''
            groups = []

        for j in range(1, len(time_intervals)+1):
            if i>6*j and i<=6*j+6:
                time = f'{time_intervals[j-1]}'
        # print(time)

        schedule[day].append([schedule__discipline, schedule__place, schedule__teacher, groups, time])
        # print(info)
            # soup.findAll('div', class_="schedule__time-item")
            
            # print('schedule__discipline')

    # print(all_time.text, '\n')

    # for data in all:
    #     # print(data.text)
    #     pass
    pprint.pprint(schedule)
    return schedule


# getCurrentWeek()
parseWeekFromGroup('/rasp?groupId=531030143')

# parseGroups()
# parseTeachers()