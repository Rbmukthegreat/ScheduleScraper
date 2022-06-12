from selenium import webdriver
from time import sleep
from classes import ClassList, Class
from multiprocessing import Process, Manager
import json
from termcolor import colored

URL_BASE = "https://myplan.uw.edu/course/#/courses/"
QUARTER = "Autumn" # Summer, Autumn, Winter, Spring

CLASSES = [("MATH334", ""), ("ENGL182", ""), ("PHYS121", "LECTURE"), ("PHYS121", "QUIZ"), ("PHYS121", "LABORATORY"), ("CSE143", "LECTURE"), ("CSE143", "QUIZ")]
#CLASSES=[("MATH207", ""), ("MATH208", ""), ("MATH126", ""), ("PHYS121", "LECTURE"), ("PHYS121", "QUIZ"), ("PHYS121", "LABORATORY")]

def search_classes(CLASS, l):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(URL_BASE + CLASS[0])
 
    sleep(6)
  
    quarters = driver.find_elements_by_xpath("//*[@class=\"mb-0 table table-borderless\"]")
    
    quarter = None
    for i in range(len(quarters)):
        if QUARTER in quarters[i].find_element_by_xpath('.//caption').text:
            quarter = quarters[i].find_elements_by_xpath(".//tbody")
  
    if quarter is None or len(quarter) == 0:
        print(colored(CLASS[0] + " " + CLASS[1] + " course isn't offered this quarter!", "red"))
        return
  
    c = ClassList(CLASS[0], quarter, CLASS[1]) 
    if len(c.classlist) == 0:
        print(colored("Given the constraints " + CLASS[0] + " " + CLASS[1] + " doesn't work!", "red"))
        return
 
    l.append(c)

    driver.close()

def main():
    num_processes = len(CLASSES)
    with Manager() as manager:
        l = manager.list()
        processes = []
        for i in range(num_processes):
           p = Process(target=search_classes, args=(CLASSES[i], l)) 
           processes.append(p)
           p.start()
        for i in range(num_processes):
            processes[i].join()
        for i in range(num_processes):
            processes[i].close()
        with open("classes.json", "w") as outfile:
            output_list = []
            for classlist in l:
                output_list.append(classlist.to_dict_entry())
            json.dump(output_list, outfile, indent=4)

if __name__ == "__main__":
    main()
