import json
from pprint import pprint

count = 0

def sort_by(dict_object):
    return len(dict_object["ITEMS"])

def print_schedule(li):
    for CLASS, SECTION in li:
        print(CLASS + " " + SECTION["SECTION_ID"] + " ", end="")
    print()

def time_to_tuple(time: str) -> (float, float):
    first = float(time[0:2]) + float(time[3:5])/60
    second = float(time[6:8]) + float(time[9:11])/60
    return (first, second)

def is_conflict(tup1, tup2):
    return tup1[0] < tup2[1] and tup2[0] < tup1[1]

def is_conflict_class(class1, class2) -> bool:
    for i in range(5):
        if is_conflict(class1["TIMES"][i], class2["TIMES"][i]):
            return True
    return False

def f(l, n, curr_list):
    if n == len(l):
        global count
        count += 1
        print_schedule(curr_list)
        return

    for i in range(len(l[n]["ITEMS"])):
        temp_list = curr_list.copy()
        flag = False
        for classname, clazz in curr_list:
            if is_conflict_class(l[n]["ITEMS"][i], clazz):
                flag = True
                break
        if flag:
            continue
        temp_list.append((l[n]["CLASS"], l[n]["ITEMS"][i]))
        f(l, n+1, temp_list)
        temp_list = curr_list.copy()

def remove_unnecessary_sections(all_sections, curr_list):
    le = len(all_sections)
    for i in range(len(all_sections)):
        if len(all_sections[le - i - 1]["ITEMS"]) == 1:
            curr_list.append((all_sections[le - i - 1]["CLASS"], all_sections[le - i - 1]["ITEMS"][0])) 
            all_sections.pop(le - i - 1)
        else:
            return

if __name__=="__main__":
    with open('classes.json') as json_file:
        all_sections = json.load(json_file)
        all_sections.sort(reverse=True, key=sort_by)
        for classes in all_sections:
            for section in classes["ITEMS"]:
                for i in range(len(section["TIMES"])):
                        section["TIMES"][i] = time_to_tuple(section["TIMES"][i])

        curr_list = []
        remove_unnecessary_sections(all_sections, curr_list)
        f(all_sections, 0, curr_list)
        print(count)
