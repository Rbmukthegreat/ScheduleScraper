import json
from pprint import pprint

count = 0

def sort_by(dict_object):
    return len(dict_object["ITEMS"])

def print_schedule(li):
    for CLASS, SECTION in li:
        print(CLASS + " " + SECTION + " ", end="")
    print()

def f(l, n, curr_list):
    if n == len(l):
        global count
        count += 1
        print_schedule(curr_list)
        return

    for i in range(len(l[n]["ITEMS"])):
        temp_list = curr_list.copy()
        temp_list.append((l[n]["CLASS"], l[n]["ITEMS"][i]["SECTION_ID"]))
        f(l, n+1, temp_list)
        temp_list = curr_list.copy()

def remove_unnecessary_sections(all_sections, curr_list):
    le = len(all_sections)
    for i in range(len(all_sections)):
        if len(all_sections[le - i - 1]["ITEMS"]) == 1:
            curr_list.append((all_sections[le - i - 1]["CLASS"], all_sections[le - i - 1]["ITEMS"][0]["SECTION_ID"])) 
            all_sections.pop(le - i - 1)
        else:
            return

if __name__=="__main__":
    with open('classes.json') as json_file:
        all_sections = json.load(json_file)
        all_sections.sort(reverse=True, key=sort_by)
        curr_list = []
        remove_unnecessary_sections(all_sections, curr_list)
        f(all_sections, 0, curr_list)
        print(count)
