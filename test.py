import json
from pprint import pprint
from draw_schedule import draw_schedule
import random

def time_to_tuple(time: str) -> (float, float):
    first = float(time[0:2]) + float(time[3:5])/60
    second = float(time[6:8]) + float(time[9:11])/60
    return (first, second)

count = 0
TIME_BETWEEN_CLASSES=0 # This number is in hours
CONSTRAINTS = ["18:30-23:59", "08:30-09:30"]
LUNCH = time_to_tuple("10:30-13:30")
LEN_LUNCH = 40.0/60

def print_schedule(li):
    for CLASS, SECTION, TYPE in li:
        print(CLASS + " (" + TYPE + ") " + SECTION["SECTION_ID"] + " ", end="")
    print()

def is_conflict(tup1, tup2):
    return tup1[0] < tup2[1] and tup2[0] < tup1[1]

def constrained(clazz):
    for st in CONSTRAINTS:
        for i in range(5):
            if is_conflict(clazz["TIMES"][i], time_to_tuple(st)):
                return True
    return False

def is_conflict_class(class1, class2) -> bool:
    for i in range(5):
        if is_conflict(class1["TIMES"][i], class2["TIMES"][i]):
            return True
    if TIME_BETWEEN_CLASSES != 0:
        for i in range(5):
            if is_conflict((class1["TIMES"][i][0] + TIME_BETWEEN_CLASSES, class1["TIMES"][i][1] + TIME_BETWEEN_CLASSES), class2["TIMES"][i]):
                return True
            if is_conflict((class1["TIMES"][i][0] - TIME_BETWEEN_CLASSES, class1["TIMES"][i][1] - TIME_BETWEEN_CLASSES), class2["TIMES"][i]):
                return True
    return False

all_schedules = []
def get_schedules(l, n, curr_list):
    if n == len(l):
        global count
        count += 1
        global all_schedules
        all_schedules.append(curr_list)
        return

    for i in range(len(l[n]["ITEMS"])):
        temp_list = curr_list.copy()
        flag = False
        for classname, clazz, typ in curr_list:
            if is_conflict_class(l[n]["ITEMS"][i], clazz):
                flag = True
                break
        if constrained((l[n]["ITEMS"][i])):
            flag = True
        if flag:
            continue
        temp_list.append((l[n]["CLASS"], l[n]["ITEMS"][i], l[n]["TYPE"]))
        get_schedules(l, n+1, temp_list)
        temp_list = curr_list.copy()

def key(e):
    return e[1]

def lunch_check(schedule):
    num_to_day = { 0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday" }
    for i in range(5):
        classes_in_lunchtime = []
        for classname, clazz, typ in schedule:
                if is_conflict(clazz["TIMES"][i], LUNCH):
                    classes_in_lunchtime.append(clazz["TIMES"][i])
        classes_in_lunchtime.sort(key=key)
        before_lunch = classes_in_lunchtime[0][0] - LUNCH[0]
        after_lunch = LUNCH[1] - classes_in_lunchtime[len(classes_in_lunchtime) - 1][1]
        if after_lunch >= LEN_LUNCH or before_lunch >= LEN_LUNCH:
            continue
        times_between = []
        for i in range(len(classes_in_lunchtime) - 1):
             times_between.append(classes_in_lunchtime[i+1][0] - classes_in_lunchtime[i][1])
        if len(times_between) == 0 or not max(times_between) >= LEN_LUNCH:
            return False
    return True
    
def main():
    with open('classes.json') as json_file:
        all_sections = json.load(json_file)
        for classes in all_sections:
            for section in classes["ITEMS"]:
                for i in range(len(section["TIMES"])):
                        section["TIMES"][i] = time_to_tuple(section["TIMES"][i])

    get_schedules(all_sections, 0, [])
    correct_schedules = [ schedule for schedule in all_schedules if lunch_check(schedule) ]
    print(len(all_schedules))
    print("len of correct schedules: " + str(len(correct_schedules)))
    if len(all_schedules) == 0:
        print("Oh no! There are no possibilities!")
        quit()
    choice = random.choice(correct_schedules)
    draw_schedule(choice)
    print("\n\n\n\n\n\n\n\n")
    print(lunch_check(choice))
    with open('classes_out.txt', 'w') as file:
        SLNS = '\n'.join([ clazz[1]["SLN"] for clazz in choice ])
        file.write(SLNS)

main()
