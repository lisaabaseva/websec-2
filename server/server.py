
from flask import Flask, request, render_template
import json
import pprint
from parse import parseSchedule, currentWeek, parseGroups, parseTeachers
from flask_cors import CORS, cross_origin


 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
 
@app.route('/')
def hello():
    return "Hello, World!"


@app.route('/groups', methods=['GET'])
@cross_origin()
def getGroups():

    with open('server/groups.json', 'r', encoding="utf-8") as outfile:
        data = json.load(outfile)

    # pprint.pprint(data)

    return data['groups']

@app.route('/entrys', methods=['POST'])
@cross_origin()
def entrys():

    with open('server/groups.json', 'r', encoding="utf-8") as outfile:
        data = json.load(outfile)
    with open('server/teachers.json', 'r', encoding="utf-8") as outfile2:
        data2 = json.load(outfile2)

    elem = str(request.json['elem']).strip().lower()
    pprint.pprint(elem)
    if elem == "":
        return []

    ret = []
    for group in data["groups"]:
        # if group["group"].find(elem):
        #     ret.append(group)
        if str(group["group"]).lower().startswith(elem):
            ret.append(group)

    for teacher in data2["teachers"]:
        # if group["group"].find(elem):
        #     ret.append(group)
        if str(teacher["name"]).lower().startswith(elem):
            ret.append(teacher)

    pprint.pprint(ret)
    print(len(ret))
    if len(ret) > 20:
        return ret[0:20]
    else:
        return ret


@app.route('/teachers', methods=['GET'])
def getTeachers():

    with open('server/teachers.json', 'r', encoding="utf-8") as outfile:
        data = json.load(outfile)

    # pprint.pprint(data)

    return data['teachers']

@app.route('/schedule', methods=['GET'])
@cross_origin()
def getSchedule():

    group_link = request.args.get('group_link', type=str)
    selected_week = request.args.get('selectedWeek', type=str)
    schedule = parseSchedule(group_link, selected_week)

    # with open('schedule.json', 'r', encoding="utf-8") as outfile:
    #     data = json.load(outfile)

    # pprint.pprint(data)

    return schedule




@app.route('/currweek', methods=['GET'])
@cross_origin()
def getCurrentWeek():
    cW = currentWeek()
    print(cW)
    return cW


 
if __name__ == '__main__':
    # если захочится спарсить в реальном времени
    # parseGroups()
    # parseTeachers()
    
    app.run()